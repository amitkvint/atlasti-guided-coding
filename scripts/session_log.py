#!/usr/bin/env python3
"""Keep the session log on disk and compare it with the live project.

One JSON line per item presented to the researcher, written once the item is
decided. The log is the source for figures.py and for the close-out check.

Add an item:
  session_log.py add LOG.jsonl --rec suggest|skip|anchor --decision use|modify|skip|decline
      [--label strong|arguable|stretch] [--codes "A;B"] [--new-codes "C"]
      [--final-codes "A"] [--start N --end N] [--qid ID] [--comment]
      [--pass main|contrary] [--note "..."]
Record a process lapse (an error in how the work was done, even a harmless one):
  session_log.py lapse LOG.jsonl --note "what happened"
Record a codebook change made in the project (on the researcher's decision):
  session_log.py codebook LOG.jsonl --action create|define|group|rename|delete
      --code "Code name" [--id ID] [--note "..."]
Compare the log with the live quotation list (saved as JSON, see quotes format below):
  session_log.py compare LOG.jsonl QUOTES.json

Quotes format: a JSON list of {"id", "start", "end", "codes": [...], "comment"}.
Build it from list_quotations for the document before comparing.
"""
import argparse
import datetime
import json
import sys


def split(s):
    return [c.strip() for c in s.split(";") if c.strip()] if s else []


def read_log(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def add(a, kind):
    rec = {"time": datetime.datetime.now().isoformat(timespec="seconds"), "kind": kind}
    if kind == "item":
        try:
            n = sum(1 for r in read_log(a.log) if r["kind"] == "item")
        except FileNotFoundError:
            n = 0
        rec.update({
            "item": n + 1, "pass": a.pass_, "rec": a.rec, "label": a.label,
            "codes": split(a.codes), "new_codes": split(a.new_codes),
            "decision": a.decision, "final_codes": split(a.final_codes),
            "start": a.start, "end": a.end, "qid": a.qid, "comment": a.comment,
        })
    if kind == "codebook":
        rec.update({"action": a.action, "code": a.code, "id": a.id})
    rec["note"] = a.note
    with open(a.log, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(json.dumps(rec, ensure_ascii=False))


def written_by_id(written, qid):
    return next(r for k, r in written.items() if str(k) == str(qid))


def compare(a):
    written = {r["qid"]: r for r in read_log(a.log)
               if r["kind"] == "item" and r.get("qid")}
    with open(a.quotes, encoding="utf-8") as f:
        live = {str(q["id"]): q for q in json.load(f)}
    problems, notes = [], []
    for qid, r in written.items():
        q = live.get(str(qid))
        if not q:
            problems.append(f"item {r['item']}: quotation {qid} is in the log but not in the project")
            continue
        if (q["start"], q["end"]) != (r["start"], r["end"]):
            problems.append(f"item {r['item']}: span in project {q['start']}-{q['end']}, "
                            f"log {r['start']}-{r['end']}")
        if sorted(q.get("codes", [])) != sorted(r["final_codes"]):
            problems.append(f"item {r['item']}: codes in project {q.get('codes')}, log {r['final_codes']}")
        if r["comment"] and not q.get("comment"):
            problems.append(f"item {r['item']}: comment agreed but missing in project")
    for qid, q in live.items():
        if qid not in {str(k) for k in written}:
            notes.append(f"quotation {qid} ({q['start']}-{q['end']}) is in the project but not "
                         "in this log: earlier coding or the researcher's own")
        elif not q.get("comment") and not written_by_id(written, qid)["comment"]:
            notes.append(f"quotation {qid} has no comment (none was agreed)")
    print(json.dumps({"written_in_log": len(written), "in_project": len(live),
                      "problems": problems, "notes": notes}, ensure_ascii=False, indent=1))
    sys.exit(1 if problems else 0)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("add")
    p.add_argument("log")
    p.add_argument("--rec", required=True, choices=["suggest", "skip", "anchor"])
    p.add_argument("--decision", required=True, choices=["use", "modify", "skip", "decline"])
    p.add_argument("--label", choices=["strong", "arguable", "stretch"])
    p.add_argument("--codes", default="")
    p.add_argument("--new-codes", default="")
    p.add_argument("--final-codes", default="")
    p.add_argument("--start", type=int)
    p.add_argument("--end", type=int)
    p.add_argument("--qid")
    p.add_argument("--comment", action="store_true")
    p.add_argument("--pass", dest="pass_", default="main", choices=["main", "contrary"])
    p.add_argument("--note", default="")
    p = sub.add_parser("lapse")
    p.add_argument("log")
    p.add_argument("--note", required=True)
    p = sub.add_parser("codebook")
    p.add_argument("log")
    p.add_argument("--action", required=True, choices=["create", "define", "group", "rename", "delete"])
    p.add_argument("--code", required=True)
    p.add_argument("--id")
    p.add_argument("--note", default="")
    p = sub.add_parser("compare")
    p.add_argument("log")
    p.add_argument("quotes")
    a = ap.parse_args()
    if a.cmd == "add":
        add(a, "item")
    elif a.cmd in ("lapse", "codebook"):
        add(a, a.cmd)
    else:
        compare(a)


if __name__ == "__main__":
    main()
