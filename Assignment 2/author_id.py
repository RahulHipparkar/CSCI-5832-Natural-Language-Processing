"""Author ID: shared BPE tokenizer, one N-gram LM per author, predict the author with lower NLL."""

import argparse
import os
import sys

from bpe_tokenizer import BPETokenizer
from data_utils import make_dev_split, read_passages, read_text, split_sentences
from ngram_lm import NGramLM

# Final settings from experiments.py (dev acc 0.985 on 3-sentence, 0.909 on 1-sentence passages).
DEFAULTS = dict(vocab_size=10000, pretokenizer="whitespace", lowercase=True, n=1, k=1.0)


class AuthorClassifier:
    """Trains one LM per author on a shared vocabulary and labels passages by lowest NLL."""

    def __init__(self, vocab_size, pretokenizer, lowercase, n, k, normalize=True):
        self.cfg = dict(vocab_size=vocab_size, pretokenizer=pretokenizer,
                        lowercase=lowercase, n=n, k=k)
        self.normalize = normalize  # False only for the typography ablation
        self.tokenizer = None
        self.models = {}

    def fit(self, sentences_by_author):
        """Train the shared tokenizer on all text, then one LM per author."""
        all_sents = [s for sents in sentences_by_author.values() for s in sents]
        self.tokenizer = BPETokenizer(self.cfg["vocab_size"], self.cfg["pretokenizer"],
                                      self.cfg["lowercase"]).train_from_texts(all_sents)
        V = len(self.tokenizer)
        for author, sents in sentences_by_author.items():
            lm = NGramLM(self.cfg["n"], V, self.tokenizer.bos_id,
                         self.tokenizer.eos_id, k=self.cfg["k"])
            lm.train(self.tokenizer.encode_batch(sents))
            self.models[author] = lm
        return self

    def set_lm_params(self, n=None, k=None):
        """Change order and/or k without retraining."""
        for lm in self.models.values():
            if n is not None:
                lm.set_order(n)
            if k is not None:
                lm.set_k(k)
        if n is not None:
            self.cfg["n"] = n
        if k is not None:
            self.cfg["k"] = k
        return self

    def scores(self, passage):
        """NLL of the passage under each author's LM."""
        sents = split_sentences(passage, normalize=self.normalize) or [passage]
        ids = self.tokenizer.encode_batch(sents)
        return {a: lm.corpus_nll(ids)[0] for a, lm in self.models.items()}

    def predict(self, passage):
        """Author whose LM gives the lowest NLL (same tokens, so also lowest perplexity)."""
        s = self.scores(passage)
        return min(s, key=s.get)

    def predict_batch(self, passages):
        return [self.predict(p) for p in passages]

    def accuracy(self, labelled):
        """Fraction correct over a list of (passage, true_author)."""
        return sum(self.predict(p) == y for p, y in labelled) / len(labelled)


def load_authors(tolkien_path, doyle_path, normalize=True):
    """Clean both books and split them into sentences."""
    return {"tolkien": split_sentences(read_text(tolkien_path), book=True, normalize=normalize),
            "doyle": split_sentences(read_text(doyle_path), book=True, normalize=normalize)}


def train_final(tolkien_path, doyle_path, **overrides):
    """Train the final classifier (DEFAULTS) on all training text."""
    return AuthorClassifier(**{**DEFAULTS, **overrides}).fit(load_authors(tolkien_path, doyle_path))


def predict(clf, passages):
    """List of passage strings -> list of 'tolkien' / 'doyle' labels."""
    return clf.predict_batch(passages)


def _default_path(name):
    """Look for a training book next to this script, else in the current directory."""
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
    return here if os.path.exists(here) else name


def dev_split(sentences_by_author, passage_len=3):
    """Hold out interleaved passages from each author as a labelled dev set."""
    train, dev = {}, []
    for author, sents in sentences_by_author.items():
        train[author], passages = make_dev_split(sents, passage_len)
        dev.extend((p, author) for p in passages)
    return train, dev


def main():
    ap = argparse.ArgumentParser(description="Label test passages as tolkien or doyle.")
    ap.add_argument("--tolkien", default=_default_path("hobbit.txt"))
    ap.add_argument("--doyle", default=_default_path("lostworld.txt"))
    ap.add_argument("--test", help="test .txt/.csv/.tsv file or folder of .txt files")
    ap.add_argument("--out", default="predictions.txt")
    ap.add_argument("--dev", action="store_true", help="report held-out dev accuracy")
    ap.add_argument("--vocab", type=int, default=DEFAULTS["vocab_size"])
    ap.add_argument("--pretok", default=DEFAULTS["pretokenizer"])
    ap.add_argument("--lowercase", action=argparse.BooleanOptionalAction, default=DEFAULTS["lowercase"])
    ap.add_argument("--n", type=int, default=DEFAULTS["n"])
    ap.add_argument("--k", type=float, default=DEFAULTS["k"])
    args = ap.parse_args()
    for path in (args.tolkien, args.doyle):
        if not os.path.exists(path):
            sys.exit(f"Training file not found: {path} (pass --tolkien / --doyle)")
    if not (args.dev or args.test):
        ap.error("nothing to do: pass --test <file> and/or --dev")

    data = load_authors(args.tolkien, args.doyle)
    params = dict(vocab_size=args.vocab, pretokenizer=args.pretok,
                  lowercase=args.lowercase, n=args.n, k=args.k)

    if args.dev:
        train, dev = dev_split(data)
        clf = AuthorClassifier(**params).fit(train)
        print(f"{params}  dev accuracy = {clf.accuracy(dev):.4f}  ({len(dev)} passages)")

    if args.test:
        clf = AuthorClassifier(**params).fit(data)  # final model uses all training text
        passages = read_passages(args.test)
        labels = clf.predict_batch([text for _, text in passages])
        with open(args.out, "w") as f:
            for (pid, _), label in zip(passages, labels):
                f.write(f"{pid}\t{label}\n")
        counts = {a: labels.count(a) for a in clf.models}
        print(f"Wrote {len(passages)} predictions to {args.out}  {counts}")


if __name__ == "__main__":
    main()