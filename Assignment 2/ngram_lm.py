"""N-gram LMs (n=1..3) over BPE token ids with add-k smoothing, NLL and perplexity."""

import math
from collections import Counter


class NGramLM:
    """Add-k model: P(w|h) = (c(h,w) + k) / (c(h) + k*V), logs are natural (nats)."""

    def __init__(self, n, vocab_size, bos_id, eos_id, k=1.0):
        if n not in (1, 2, 3):
            raise ValueError("n must be 1, 2 or 3")
        self.n = n
        self.V = vocab_size
        self.bos_id = bos_id
        self.eos_id = eos_id
        self.k = k
        # counts[m][(id, ..., id)] = count of that m-gram, keyed by vocab indices.
        self.counts = {1: Counter(), 2: Counter(), 3: Counter()}
        # hist[m][history] = times that (m-1)-gram history was followed by a token.
        self.hist = {1: Counter(), 2: Counter(), 3: Counter()}
        self.n_train_tokens = 0

    def _pad(self, ids, order):
        """Add (order-1) <s> tokens before a sentence and one </s> after it."""
        return [self.bos_id] * (order - 1) + list(ids) + [self.eos_id]

    def train(self, sentences):
        """Collect unigram, bigram and trigram counts from lists of token ids."""
        for ids in sentences:
            for m in (1, 2, 3):
                seq = self._pad(ids, m)
                for i in range(m - 1, len(seq)):
                    gram = tuple(seq[i - m + 1: i + 1])
                    self.counts[m][gram] += 1
                    self.hist[m][gram[:-1]] += 1
            self.n_train_tokens += len(ids) + 1  # +1 for </s>
        return self

    def logprob(self, word, history):
        """log P(word | history) with add-k smoothing at this model's order."""
        m = self.n
        h = tuple(history[-(m - 1):]) if m > 1 else ()
        num = self.counts[m][h + (word,)] + self.k
        den = self.hist[m][h] + self.k * self.V
        return math.log(num / den)

    def sequence_nll(self, ids):
        """Negative log prob of one sentence incl. </s>; returns (nll, n_predictions)."""
        seq = self._pad(ids, self.n)
        nll = 0.0
        for i in range(self.n - 1, len(seq)):
            nll -= self.logprob(seq[i], seq[max(0, i - self.n + 1):i])
        return nll, len(seq) - (self.n - 1)

    def corpus_nll(self, sentences):
        """Total NLL and total prediction count over many sentences."""
        total, count = 0.0, 0
        for ids in sentences:
            nll, c = self.sequence_nll(ids)
            total += nll
            count += c
        return total, count

    @staticmethod
    def _as_sentences(data):
        """Accept either one id sequence or a list of id sequences."""
        data = list(data)
        return [data] if data and isinstance(data[0], int) else data

    def neg_log_prob(self, ids):
        """Negative log probability (nats) of a token-id sequence, as a float."""
        return self.corpus_nll(self._as_sentences(ids))[0]

    def perplexity(self, sentences, n_words=None):
        """Assignment definition: per-word average NLL = total NLL / N (N = tokens, or n_words if given)."""
        total, count = self.corpus_nll(self._as_sentences(sentences))
        return total / (n_words if n_words else count)

    def exp_perplexity(self, sentences, n_words=None):
        """Textbook exp(average NLL), reported for reference only."""
        return math.exp(self.perplexity(sentences, n_words))

    def set_k(self, k):
        """Change smoothing without retraining (counts do not depend on k)."""
        self.k = k
        return self

    def set_order(self, n):
        """Reuse the same counts as a unigram, bigram or trigram model."""
        self.n = n
        return self
