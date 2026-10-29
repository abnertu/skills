#!/usr/bin/env python3
"""List English Markdown sentences over the ASD-STE100 length limits for review.

Usage: check-sentences.py FILE...

Prints `file:line: N words: sentence` for each sentence over 20 words; the
writer decides whether it is an instruction (limit 20) or a description
(limit 25). Code blocks, front matter, headings and badge rows are skipped;
inline code and link targets count as one word. Exits 0: the output is a
review list, not a verdict.
"""
import re
import sys

LIMIT = 20
SENTENCE_END = re.compile(r"[.!?](?:\*\*|\*|_)?\s+(?=\S)")
ABBREVIATIONS = ("e.g.", "i.e.", "etc.", "vs.", "cf.")
FENCE = re.compile(r"(`{3,}|~{3,})(.*)")


def sentences(text):
    start = 0
    for match in SENTENCE_END.finditer(text):
        if text[: match.start() + 1].lower().endswith(ABBREVIATIONS):
            continue
        yield text[start : match.end()]
        start = match.end()
    yield text[start:]


def words(text):
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"`[^`]*`", "X", text)
    text = re.sub(r"<[^>]+>", " ", text)
    return [w for w in text.split() if re.search(r"\w", w)]


def check(path):
    fence = None
    in_front = False
    with open(path, encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            text = line.strip()
            if number == 1 and text == "---":
                in_front = True
                continue
            if in_front:
                in_front = text != "---"
                continue
            match = FENCE.match(text)
            if match:
                marker, info = match.groups()
                if fence is not None:
                    if (
                        marker[0] == fence[0]
                        and len(marker) >= len(fence)
                        and not info.strip()
                    ):
                        fence = None
                    continue
                if marker[0] != "`" or "`" not in info:
                    fence = marker
                    continue
            if fence is not None or not text or text.startswith(("#", "[![", "<!--")):
                continue
            cells = text.strip("|").split("|") if text.startswith("|") else [text]
            for cell in cells:
                cell = re.sub(r"^(?:[-*+]|\d+\.)\s+", "", cell.strip())
                for sentence in sentences(cell):
                    count = len(words(sentence))
                    if count > LIMIT:
                        print(f"{path}:{number}: {count} words: {sentence.strip()}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for name in sys.argv[1:]:
        check(name)
