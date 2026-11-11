#!/usr/bin/env python3
"""The fixed session figures, from the session log.

Usage:
  figures.py LOG.jsonl                       figures for one document
  figures.py --pool LOG1.jsonl LOG2.jsonl …  one row per document plus a total,
                                             as a Markdown table (for a methods note)

The figures are the same every time so sessions can be compared and reported:
items presented, quotations written, code applications, codes used, NEW codes
proposed / created / declined, uncoded anchors, skip recommendations and the skip
ratio, confidence labels of items presented and accepted, how often the
researcher changed or overruled a recommendation, contrary-reading results, and
process lapses.
"""
import argparse
import json
import os
from collections import Counter

LABELS = ("strong", "arguable", "stretch")


def read_log(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def figures(rows):
    items = [r for r in rows if r["kind"] == "item"]
    main = [r for r in items if r.get("pass") == "main"]
    contrary = [r for r in items if r.get("pass") == "contrary"]
    written = [r for r in items if r.get("qid")]
    accepted = [r for r in items if r["decision"] in ("use", "modify")]
    suggested = [r for r in items if r["rec"] == "suggest"]
    proposed_new = {c for r in items for c in r.get("new_codes", [])}
    created_new = ({c for r in written for c in r.get("new_codes", []) if c in r["final_codes"]} |
                   {r["code"] for r in rows if r["kind"] == "codebook" and r["action"] == "create"})
    applications = [c for r in written for c in r["final_codes"]]
    proposed_new |= created_new  # a code created was necessarily proposed
    # overruled: the researcher's decision went against the recommendation
    overruled = [r for r in items if
                 (r["rec"] == "suggest" and r["decision"] in ("skip", "decline")) or
                 (r["rec"] in ("skip",) and r["decision"] in ("use", "modify"))]
    modified = [r for r in items if r["decision"] == "modify"]
    return {
        "items presented": len(items),
        "quotations written": len(written),
        "code applications": len(applications),
        "codes used": len(set(applications)),
        "NEW codes proposed": len(proposed_new),
        "NEW codes created": len(created_new),
        "NEW codes declined": len(proposed_new - created_new),
        "NEW codes created, not yet applied": len(created_new - set(applications)),
        "uncoded anchors": sum(1 for r in written if not r["final_codes"]),
        "skip recommendations": sum(1 for r in items if r["rec"] == "skip"),
        "skip ratio": round(sum(1 for r in items if r["rec"] == "skip") / max(1, len(items)), 2),
        "presented strong/arguable/stretch": "/".join(
            str(sum(1 for r in suggested if r.get("label") == l)) for l in LABELS),
        "accepted strong/arguable/stretch": "/".join(
            str(sum(1 for r in accepted if r["rec"] == "suggest" and r.get("label") == l))
            for l in LABELS),
        "modified by researcher": len(modified),
        "overruled": len(overruled),
        "overrule rate": round(len(overruled) / max(1, len(items)), 2),
        "contrary-reading items": len(contrary),
        "contrary-reading items accepted": sum(1 for r in contrary if r["decision"] in ("use", "modify")),
        "codebook changes (definitions, groups, renames, deletions)": sum(
            1 for r in rows if r["kind"] == "codebook" and r["action"] != "create"),
        "process lapses": sum(1 for r in rows if r["kind"] == "lapse"),
        "_main_items": len(main),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logs", nargs="+")
    ap.add_argument("--pool", action="store_true")
    a = ap.parse_args()
    if not a.pool:
        f = figures(read_log(a.logs[0]))
        f.pop("_main_items")
        print(json.dumps(f, ensure_ascii=False, indent=1))
        return
    all_rows, table = [], []
    for path in a.logs:
        rows = read_log(path)
        all_rows += rows
        table.append((os.path.basename(os.path.dirname(os.path.abspath(path))) or path, figures(rows)))
    table.append(("TOTAL", figures(all_rows)))
    keys = [k for k in table[0][1] if not k.startswith("_")]
    print("| document | " + " | ".join(keys) + " |")
    print("|---" * (len(keys) + 1) + "|")
    for name, f in table:
        print(f"| {name} | " + " | ".join(str(f[k]) for k in keys) + " |")


if __name__ == "__main__":
    main()
