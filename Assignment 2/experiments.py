"""Runs all explorations (typography, tokenizer, perplexity, author-ID grid) and writes results.md."""

import argparse
import math
import time

from author_id import AuthorClassifier, _default_path, dev_split, load_authors
from bpe_tokenizer import BPETokenizer
from data_utils import count_words, normalize_typography
from ngram_lm import NGramLM

PRETOKS = ["whitespace", "ws_only", "bytelevel"]
VOCABS = [500, 1000, 2000, 5000, 10000]
ORDERS = [1, 2, 3]
KS = [1.0, 0.1, 0.01, 0.001]


def md_table(header, rows):
    """Render rows as a markdown table."""
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def to_curly(text):
    """Re-typeset a passage in Hobbit-file style (curly quotes, em-dashes)."""
    out, open_q = [], True
    for ch in text:
        if ch == '"':
            out.append("\u201c" if open_q else "\u201d")
            open_q = not open_q
        elif ch == "'":
            out.append("\u2019")
        else:
            out.append(ch)
    return "".join(out).replace(" -- ", "\u2014").replace("--", "\u2014")


def to_straight(text):
    """Re-typeset a passage in Lost-World-file style (straight quotes, --)."""
    return normalize_typography(text).replace(" -- ", "--")


def part0_typography(data_raw, data_clean, cfg):
    """Raw vs normalized training, tested on dev passages as-is and with typography swapped."""
    rows = []
    for name, data, norm in (("raw", data_raw, False), ("normalized", data_clean, True)):
        train, dev = dev_split(data)
        clf = AuthorClassifier(normalize=norm, **cfg).fit(train)
        swapped = [(to_straight(p) if y == "tolkien" else to_curly(p), y) for p, y in dev]
        rows.append([name, f"{clf.accuracy(dev):.4f}", f"{clf.accuracy(swapped):.4f}"])
    return ("## Part 0: Typography confound\n\n"
            "The Hobbit file uses curly quotes/em-dashes; The Lost World file uses straight "
            "quotes and '--'. 'Swapped' re-typesets each dev passage in the OTHER book's style. "
            f"Config: {cfg}\n\n"
            + md_table(["training text", "dev acc (as-is)", "dev acc (typography swapped)"], rows)
            + "\n")


def part1_tokenizer(train, dev_sents, sample):
    """Learned vocab size, tokens/word and example segmentations per pre-tokenizer and V."""
    rows, examples = [], []
    all_train = [s for v in train.values() for s in v]
    n_words = count_words(dev_sents)
    for pt in PRETOKS:
        for V in VOCABS:
            tok = BPETokenizer(V, pt).train_from_texts(all_train)
            n_tok = sum(len(x) for x in tok.encode_batch(dev_sents))
            unk = sum(x.count(tok.token_to_id("<unk>")) for x in tok.encode_batch(dev_sents))
            rows.append([pt, V, len(tok), f"{n_tok / n_words:.3f}", unk])
            if V in (500, 5000):
                examples.append(f"- **{pt}, V={V}**: `{' '.join(tok.encode_tokens(sample))}`")
    return ("## Part 1: Tokenizer\n\n"
            "Tokens/word is measured on the held-out dev text (lower = longer merges).\n\n"
            + md_table(["pre-tokenizer", "requested V", "learned V", "tokens/word", "<unk> on dev"], rows)
            + "\n\nExample segmentations:\n\n" + "\n".join(examples) + "\n")


def part2_perplexity(train, dev_sents_by_author, V_req=5000, pt="whitespace"):
    """Held-out perplexity (avg NLL per word) for each order and k, same- and cross-author."""
    all_train = [s for v in train.values() for s in v]
    tok = BPETokenizer(V_req, pt).train_from_texts(all_train)
    V = len(tok)
    out = [f"## Part 2: N-gram perplexity\n\nShared tokenizer: {pt}, V={V}. "
           "Rows are the author the LM was trained on; 'eval on' is held-out text. "
           "Perplexity = per-word average negative log probability in nats "
           "(assignment definition; lower is better). 'per token' averages over "
           "predicted BPE tokens; 'per ws-word' over whitespace words, which is "
           "comparable across vocab sizes. exp(.) shown for reference only.\n"]
    for author, sents in train.items():
        lm = NGramLM(3, V, tok.bos_id, tok.eos_id).train(tok.encode_batch(sents))
        rows = []
        for eval_author, dsents in dev_sents_by_author.items():
            ids = tok.encode_batch(dsents)
            nw = count_words(dsents)
            for n in ORDERS:
                for k in KS:
                    lm.set_order(n).set_k(k)
                    ppl_t = lm.perplexity(ids)
                    ppl_w = lm.perplexity(ids, n_words=nw)
                    rows.append([author, eval_author, n, k, f"{ppl_t:.3f}", f"{ppl_w:.3f}",
                                 f"{math.exp(ppl_t):.1f}"])
        out.append(md_table(["LM trained on", "eval on", "n", "k", "perplexity (per token)",
                             "perplexity (per ws-word)", "exp(per token)"], rows))
    return "\n\n".join(out) + "\n"


def part3_author_id(data, passage_lens=(3, 1)):
    """Dev-accuracy grid; best config = highest accuracy averaged over passage lengths."""
    rows, acc_by_cfg = [], {}
    for plen in passage_lens:
        train, dev = dev_split(data, passage_len=plen)
        for pt in PRETOKS:
            for lower in (False, True):
                if pt != "whitespace" and lower:
                    continue  # lowercasing tested on one pre-tokenizer only
                for V in VOCABS:
                    clf = AuthorClassifier(V, pt, lower, 3, 1.0).fit(train)
                    for n in ORDERS:
                        for k in KS:
                            acc = clf.set_lm_params(n=n, k=k).accuracy(dev)
                            rows.append([plen, pt, lower, V, n, k, f"{acc:.4f}"])
                            acc_by_cfg.setdefault((pt, lower, V, n, k), []).append(acc)
        print(f"  finished passage_len={plen}")
    rows.sort(key=lambda r: (-r[0], -float(r[-1])))
    ranked = sorted(acc_by_cfg.items(), key=lambda kv: -sum(kv[1]) / len(kv[1]))
    top = [[*cfg, *(f"{a:.4f}" for a in accs), f"{sum(accs) / len(accs):.4f}"]
           for cfg, accs in ranked[:10]]
    (pt, lower, V, n, k), accs = ranked[0]
    best = (sum(accs) / len(accs), dict(pretokenizer=pt, lowercase=lower, vocab_size=V, n=n, k=k))
    return ("## Part 3: Author identification (dev accuracy)\n\n"
            "Passages = consecutive sentences held out from each book.\n\n"
            "Top 10 configs by accuracy averaged over passage lengths:\n\n"
            + md_table(["pre-tok", "lower", "V", "n", "k",
                        *(f"acc {p}-sent" for p in passage_lens), "mean"], top)
            + f"\n\nChosen: {best[1]} (mean acc {best[0]:.4f})\n\nFull grid:\n\n"
            + md_table(["sents/passage", "pre-tok", "lower", "V", "n", "k", "accuracy"], rows)
            + "\n"), best


def main():
    ap = argparse.ArgumentParser(description="Run all experiments and write results.md.")
    ap.add_argument("--tolkien", default=_default_path("hobbit.txt"))
    ap.add_argument("--doyle", default=_default_path("lostworld.txt"))
    ap.add_argument("--out", default="results.md")
    args = ap.parse_args()

    t0 = time.time()
    data = load_authors(args.tolkien, args.doyle)
    train, dev = dev_split(data, passage_len=3)
    dev_by_author = {a: [p for p, y in dev if y == a] for a in data}
    dev_sents = [p for p, _ in dev]
    sample = dev_sents[0][:120]

    raw = load_authors(args.tolkien, args.doyle, normalize=False)
    print("Part 0 ...")
    p0 = part0_typography(raw, data, dict(vocab_size=5000, pretokenizer="whitespace",
                                         lowercase=False, n=2, k=0.01))

    sections = [f"# Experiment results\n\nTraining sentences: "
                f"{ {a: len(s) for a, s in train.items()} }, dev passages: {len(dev)}\n"]
    sections.append(p0)
    print("Part 1 ...")
    sections.append(part1_tokenizer(train, dev_sents, sample))
    print("Part 2 ...")
    sections.append(part2_perplexity(train, dev_by_author))
    print("Part 3 ...")
    p3, best = part3_author_id(data)
    sections.append(p3)

    with open(args.out, "w") as f:
        f.write("\n".join(sections))
    print(f"Best author-ID config: {best[1]}  acc={best[0]:.4f}")
    print(f"Wrote {args.out} in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()