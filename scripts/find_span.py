#!/usr/bin/env python3
"""Find the exact character offsets of a span in a document's text.

Usage:
  find_span.py DOC.txt "full span text"
  find_span.py DOC.txt "first words of span" --to "last words of span"
  options: --after N   only search from offset N on (to step past an earlier match)
           --context N characters of context to show before and after (default 300)

Prints JSON: start, end (exclusive, the value create_quotation expects), the span
text, the context before and after, and the span's position in the document.
Exits with an error when the anchor matches zero times or more than once, so an
offset is never guessed.
"""
import argparse
import json
import sys


def find_all(text, needle, start=0):
    hits, i = [], text.find(needle, start)
    while i != -1:
        hits.append(i)
        i = text.find(needle, i + 1)
    return hits


def fail(msg):
    print(json.dumps({"error": msg}, ensure_ascii=False, indent=1))
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc")
    ap.add_argument("anchor")
    ap.add_argument("--to", dest="end_anchor")
    ap.add_argument("--after", type=int, default=0)
    ap.add_argument("--context", type=int, default=300)
    a = ap.parse_args()

    with open(a.doc, encoding="utf-8") as f:
        text = f.read()

    hits = find_all(text, a.anchor, a.after)
    if not hits:
        fail("start anchor not found: check spelling, quotes, spaces and line breaks")
    if len(hits) > 1:
        fail(f"start anchor found {len(hits)} times, at {hits[:10]}: "
             "lengthen the anchor or pass --after")
    start = hits[0]

    if a.end_anchor:
        ends = find_all(text, a.end_anchor, start)
        if not ends:
            fail("end anchor not found after the start anchor")
        end = ends[0] + len(a.end_anchor)
    else:
        end = start + len(a.anchor)

    span = text[start:end]
    lines = [i for i, line in enumerate(text.split("\n")) if line.strip()]
    line_no = text.count("\n", 0, start)
    para = sum(1 for i in lines if i <= line_no)

    out = {
        "start": start,
        "end": end,
        "length": end - start,
        "span": span,
        "before": text[max(0, start - a.context):start],
        "after": text[end:end + a.context],
        "paragraph": para,
        "paragraphs": len(lines),
        "percent_in": round(100 * start / max(1, len(text))),
    }
    # The ATLAS.ti server is JavaScript, which counts UTF-16 units. Hebrew and
    # Latin text count the same either way; emoji and some rare symbols do not.
    if any(ord(c) > 0xFFFF for c in text[:end]):
        u16 = lambda s: len(s.encode("utf-16-le")) // 2
        out["warning"] = ("text before this span contains characters outside the "
                          "Basic Multilingual Plane; offsets may differ in ATLAS.ti")
        out["start_utf16"] = u16(text[:start])
        out["end_utf16"] = u16(text[:end])
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
