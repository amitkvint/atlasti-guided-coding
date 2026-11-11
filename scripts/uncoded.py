#!/usr/bin/env python3
"""List the stretches of a document that carry no quotation.

Usage:
  uncoded.py DOC.txt QUOTES.json [--min 40]

QUOTES.json is the live quotation list for the document, as a JSON list of
{"id", "start", "end", ...} (the same format session_log.py uses). Stretches
shorter than --min characters after trimming whitespace are left out. Prints
each stretch with its offsets and its full text, for the contrary-reading pass.
"""
import argparse
import json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc")
    ap.add_argument("quotes")
    ap.add_argument("--min", type=int, default=40)
    a = ap.parse_args()
    with open(a.doc, encoding="utf-8") as f:
        text = f.read()
    with open(a.quotes, encoding="utf-8") as f:
        spans = sorted((q["start"], q["end"]) for q in json.load(f))

    gaps, pos = [], 0
    for s, e in spans:
        if s > pos:
            gaps.append((pos, s))
        pos = max(pos, e)
    if pos < len(text):
        gaps.append((pos, len(text)))

    out = []
    for s, e in gaps:
        chunk = text[s:e]
        lead = len(chunk) - len(chunk.lstrip())
        trail = len(chunk) - len(chunk.rstrip())
        s, e = s + lead, e - trail
        if e - s >= a.min:
            out.append({"start": s, "end": e, "length": e - s, "text": text[s:e]})
    print(json.dumps({"stretches": len(out),
                      "uncoded_characters": sum(g["length"] for g in out),
                      "document_characters": len(text),
                      "quotations": len(spans),
                      "items": out}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
