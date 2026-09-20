"""Hugging Face BPE, always trained from scratch (no pre-trained tokenizers)."""

import json

from tokenizers import (
    Tokenizer,
    decoders,
    models,
    normalizers,
    pre_tokenizers,
    trainers,
)

UNK, BOS, EOS = "<unk>", "<s>", "</s>"
SPECIAL_TOKENS = [UNK, BOS, EOS]

# Pre-tokenizers explored: split off punctuation / whitespace only / GPT-2 byte level.

PRETOKENIZERS = {
    "whitespace": lambda: pre_tokenizers.Whitespace(),
    "ws_only": lambda: pre_tokenizers.WhitespaceSplit(),
    "bytelevel": lambda: pre_tokenizers.ByteLevel(add_prefix_space=True),
}

# save() writes the constructor arguments next to the tokenizer under this suffix.
CONFIG_SUFFIX = ".config.json"


class BPETokenizer:
    """Train, save/load and apply a BPE vocabulary via Hugging Face tokenizers."""

    def __init__(
        self,
        vocab_size=5000,
        pretokenizer="whitespace",
        lowercase=False,
        min_frequency=2,
    ):
        if pretokenizer not in PRETOKENIZERS:
            raise ValueError(f"pretokenizer must be one of {list(PRETOKENIZERS)}")
        self.vocab_size = vocab_size
        self.pretokenizer = pretokenizer
        self.lowercase = lowercase
        self.min_frequency = min_frequency
        self._tok = None

    def _require(self):
        """Return the underlying HF tokenizer, or say that there is not one yet."""
        if self._tok is None:
            raise RuntimeError("call train(), train_from_texts() or load() first")
        return self._tok

    def build_empty(self):
        """Untrained HF pipeline: NFKC (+ lowercase) -> pre-tokenizer -> BPE model."""
        tok = Tokenizer(models.BPE(unk_token=UNK))
        norms = [normalizers.NFKC()]
        if self.lowercase:
            norms.append(normalizers.Lowercase())
        tok.normalizer = normalizers.Sequence(norms)
        tok.pre_tokenizer = PRETOKENIZERS[self.pretokenizer]()
        if self.pretokenizer == "bytelevel":
            tok.decoder = decoders.ByteLevel()
        return tok

    def make_trainer(self):
        """HF BpeTrainer with our vocab size and special tokens."""
        kwargs = dict(
            vocab_size=self.vocab_size,
            min_frequency=self.min_frequency,
            special_tokens=SPECIAL_TOKENS,
            show_progress=False,
        )
        if self.pretokenizer == "bytelevel":
            kwargs["initial_alphabet"] = pre_tokenizers.ByteLevel.alphabet()
        return trainers.BpeTrainer(**kwargs)

    def train(self, files):
        """Learn the vocabulary from one or more plain-text files."""
        if isinstance(files, str):
            files = [files]
        self._tok = self.build_empty()
        self._tok.train(files, self.make_trainer())
        return self

    def train_from_texts(self, texts):
        """Learn the vocabulary from an in-memory list of strings."""
        self._tok = self.build_empty()
        self._tok.train_from_iterator(texts, self.make_trainer())
        return self

    def config(self):
        """The constructor arguments needed to rebuild this tokenizer."""
        return {
            "vocab_size": self.vocab_size,
            "pretokenizer": self.pretokenizer,
            "lowercase": self.lowercase,
            "min_frequency": self.min_frequency,
        }

    def save(self, path):
        """Write the tokenizer to path and its config to path + CONFIG_SUFFIX."""
        self._require().save(str(path))
        with open(f"{path}{CONFIG_SUFFIX}", "w", encoding="utf-8") as fh:
            json.dump(self.config(), fh, indent=2)

    @classmethod
    def load(cls, path):
        """Rebuild from path and its sidecar config, keeping the requested size."""
        with open(f"{path}{CONFIG_SUFFIX}", encoding="utf-8") as fh:
            cfg = json.load(fh)
        obj = cls(**cfg)
        obj._tok = Tokenizer.from_file(str(path))
        return obj

    def encode(self, text):
        """Text -> list of vocabulary ids (the LM adds <s>/</s> itself)."""
        return self._require().encode(text).ids

    def encode_tokens(self, text):
        """Text -> list of token strings, for inspecting segmentations."""
        return self._require().encode(text).tokens

    def encode_batch(self, texts):
        """List of texts -> list of lists of vocabulary ids."""
        return [e.ids for e in self._require().encode_batch(texts)]

    def decode(self, ids):
        """Vocabulary ids -> text, using the byte-level decoder when one is set."""
        return self._require().decode(ids)

    def __len__(self):
        """The learned vocabulary size, which may be below the requested vocab_size."""
        return self._require().get_vocab_size()

    def token_to_id(self, token):
        """Look up one token string, returning None when it is not in the vocabulary."""
        return self._require().token_to_id(token)

    @property
    def bos_id(self):
        """Id of the <s> token."""
        return self._require().token_to_id(BOS)

    @property
    def eos_id(self):
        """Id of the </s> token."""
        return self._require().token_to_id(EOS)
