"""Load and clean the training books, split sentences, make the dev split, read test passages."""

import csv
import os
import re

# Sentence end: . ! ? (+ optional closing quote) then space, next word not lowercase.
_SENT_END = re.compile(r'(?<=[.!?])\s+(?![a-z])|(?<=[.!?]["\')\]])\s+(?![a-z])')
# Abbreviations whose period does not end a sentence ("Mr. Malone").
_ABBREV = re.compile(r"\b(Mr|Mrs|Ms|Dr|St|Prof|Col|Capt|Lt|Gen|Rev|Sr|Jr|Mt|No|vs|etc|i\.e|e\.g)\.$")
_CHAPTER_LINE = re.compile(r"^chapter\s+[ivxlc\d]+\.?$", re.IGNORECASE)


def read_text(path):
    """Read a file safely (drops a BOM, never fails on bad bytes, unifies line endings)."""
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        return f.read().replace("\r\n", "\n").replace("\r", "\n")


def normalize_typography(text):
    """Map curly quotes, unicode dashes and ellipses to ASCII so typography can't reveal the book."""
    text = re.sub(r"[\u201c\u201d\u201e\u00ab\u00bb]", '"', text)
    text = re.sub(r"[\u2018\u2019\u201a]", "'", text)
    text = text.replace("\u2026", "...")
    text = re.sub(r"[\u2014\u2013\u2015]", "--", text)
    text = re.sub(r"[ \t]*-{2,}[ \t]*", " -- ", text)
    return re.sub(r"[ \t]+", " ", text)


def strip_gutenberg(text):
    """Keep only the text between Project Gutenberg START/END markers, if present."""
    start = re.search(r"\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG.*?\*\*\*", text)
    end = re.search(r"\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG", text)
    if start:
        text = text[start.end():end.start() if end else None]
    return text


def split_paragraphs(text):
    """Split on blank lines and join wrapped lines inside each paragraph."""
    paras = re.split(r"\n\s*\n", text)
    return [re.sub(r"\s+", " ", p).strip() for p in paras if p.strip()]


def is_heading(para):
    """True for titles/contents (no lowercase letters) or bare 'Chapter IV' lines."""
    return not re.search(r"[a-z]", para) or bool(_CHAPTER_LINE.match(para))


def clean_book(text):
    """Strip boilerplate, normalize typography, drop headings, rejoin PDF page breaks."""
    text = normalize_typography(strip_gutenberg(text))
    paras = [p for p in split_paragraphs(text) if not is_heading(p)]
    merged = []
    for p in paras:
        if merged and p[0].islower():  # lowercase start = sentence cut by a page break
            merged[-1] += " " + p
        else:
            merged.append(p)
    return merged


def _sentences_from_paragraphs(paras):
    """Split each paragraph into sentences, re-gluing splits made after abbreviations."""
    sents = []
    for para in paras:
        for piece in (s.strip() for s in _SENT_END.split(para) if s.strip()):
            if sents and sents[-1] is not None and _ABBREV.search(sents[-1]):
                sents[-1] += " " + piece
            else:
                sents.append(piece)
        sents.append(None)  # paragraph boundary marker, never glue across it
    return [s for s in sents if s is not None]


def split_sentences(text, book=False, normalize=True):
    """Sentences from text; book=True applies clean_book, normalize=False only for the ablation."""
    if book and normalize:
        paras = clean_book(text)
    elif book:
        paras = [p for p in split_paragraphs(strip_gutenberg(text)) if not is_heading(p)]
    else:
        paras = split_paragraphs(normalize_typography(text) if normalize else text)
    return _sentences_from_paragraphs(paras)


def count_words(sentences):
    """Whitespace word count, for per-word perplexity."""
    return sum(len(s.split()) for s in sentences)


def make_dev_split(sentences, passage_len=3, dev_every=10):
    """Every dev_every-th group of passage_len sentences goes to dev; returns (train_sents, dev_passages)."""
    train, dev = [], []
    for j, start in enumerate(range(0, len(sentences), passage_len)):
        chunk = sentences[start:start + passage_len]
        if j % dev_every == dev_every - 1:
            dev.append(" ".join(chunk))
        else:
            train.extend(chunk)
    return train, dev


def _read_table(path, delimiter):
    """CSV/TSV rows: use a text/passage/content/sentence/excerpt column, else the last column."""
    with open(path, encoding="utf-8-sig", errors="replace", newline="") as f:
        rows = [r for r in csv.reader(f, delimiter=delimiter) if any(c.strip() for c in r)]
    if not rows:
        return []
    header = [c.strip().lower() for c in rows[0]]
    for name in ("text", "passage", "content", "sentence", "excerpt"):
        if name in header:
            col = header.index(name)
            return [r[col].strip() for r in rows[1:] if len(r) > col]
    return [r[-1].strip() for r in rows]


def read_passages(path):
    """Test passages from a folder of .txt, a .csv/.tsv, or a .txt (blank-line or line separated)."""
    if os.path.isdir(path):
        names = sorted(n for n in os.listdir(path) if n.endswith(".txt"))
        return [(n, re.sub(r"\s+", " ", read_text(os.path.join(path, n))).strip())
                for n in names]
    ext = os.path.splitext(path)[1].lower()
    if ext in (".csv", ".tsv"):
        texts = _read_table(path, "," if ext == ".csv" else "\t")
    else:
        text = read_text(path)
        if re.search(r"\n\s*\n", text.strip()):
            texts = split_paragraphs(text)
        else:
            texts = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return [(str(i), t) for i, t in enumerate(texts, 1)]