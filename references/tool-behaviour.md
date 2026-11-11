# Tool behaviour and helper scripts

Read this at session start, together with SKILL.md.

## ATLAS.ti MCP tools: behaviour worth knowing

- **create_quotation's end index behaves as exclusive.** Passing the index of the last character returns text one character short. Pass last index + 1 and compare the returned content to your target before moving on; if a word is cut, create the corrected quotation first, verify it, then delete the short one.
- **list_quotations and get_quotation truncate quotation content** to roughly 120 characters. They are for inventory, IDs, codes and comments, not for reading passages. To read a span on any document, fetch get_document_content for that document and slice by offset. A long document's content exceeds the tool output limit and is saved to a file; that is where you want it — parse it from disk, do not read it in the chat.
- **create_quotation is idempotent** at an identical location, so a write whose result was lost to a disconnect is safe to retry after re-verifying.
- **set_comment with overwrite replaces the whole comment**; paste the full text, not the changed sentence. The same applies to a code's definition.
- **Parent codes cannot code quotations**; use the child. get_code is exact-match; list_codes takes a substring filter.
- **Offsets are counted by a JavaScript server**, in UTF-16 units. Hebrew, Arabic and Latin text count the same as Python characters; emoji and some rare symbols count as two. `find_span.py` warns when this applies and gives both numbers.

## Helper scripts

The skill's `scripts/` folder holds four small Python scripts (standard library only). Use them whenever the session can run code: they do the mechanical work exactly and leave every decision where it was. Where code cannot run, the rules in SKILL.md still apply and you do the same work by hand.

Keep a working folder per document (for example `work/<document>/`) with `doc.txt` (the document content from get_document_content, saved once), `log.jsonl` (the session log) and `quotes.json` (the latest saved quotation list).

**quotes.json format**: a JSON list of `{"id", "start", "end", "codes": [...], "comment"}`, one entry per quotation on the document, built from list_quotations. Rebuild it whenever you re-pull the list.

- `find_span.py doc.txt "full span text"` or `find_span.py doc.txt "first words" --to "last words"` — the offsets for a span (end exclusive, ready for create_quotation), the context before and after, and the span's position (paragraph n of N, percent in). Fails on zero or several matches; lengthen the anchor or pass `--after N`. This is the string search the skill requires before any offset reaches the researcher or a write.
- `session_log.py add log.jsonl --rec suggest|skip|anchor --decision use|modify|skip|decline [--label …] [--codes "A;B"] [--new-codes "C"] [--final-codes "A"] [--start N --end N] [--qid ID] [--comment] [--pass main|contrary] [--note "…"]` — one line per item, once decided. `session_log.py lapse log.jsonl --note "…"` records a process lapse. `session_log.py codebook log.jsonl --action create|define|group|rename|delete --code "…" [--id …]` records a codebook change made in the project. `session_log.py compare log.jsonl quotes.json` compares the log with the live list row for row.
- `uncoded.py doc.txt quotes.json [--min 40]` — every stretch with no quotation, for the contrary-reading pass.
- `figures.py log.jsonl` — the fixed session figures for the close-out summary. `figures.py --pool work/*/log.jsonl` gives one row per document plus a total, for reporting across a study.
