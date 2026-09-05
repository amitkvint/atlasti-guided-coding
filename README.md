# atlasti-guided-coding

A Claude Skill for guided qualitative coding in ATLAS.ti through its MCP (Model Context Protocol) integration.

The write-up of how it came about and why the division of labor is fixed the way it is: [I Taught Claude to Code My Interviews With Me, Not For Me](https://amitkvint.com/writing/ai-assisted-qualitative-coding-atlas-ti-claude/).

## What it does

The skill turns Claude into a disciplined coding assistant inside a live ATLAS.ti project. The division of labor is fixed by design:

- **Claude suggests** — codes verified against the live codebook at the moment of suggestion, each with the code's actual definition, an honest fit assessment (including the argument against), and the best existing fallback.
- **The researcher decides** — use, skip, modify, or reframe. Every analytic decision stays human.
- **Claude executes** — only approved quotations are written, at exact character offsets computed by string search, and every write is confirmed.

Two working modes are supported: a walk-through (one suggestion, one decision, one write, repeat) and a section-pass (a full section's suggestion list delivered for the researcher to code themselves, followed by a compact matched/missed comparison).

## The three-layer architecture

The skill deliberately contains no study-specific knowledge. It expects two companion documents per study, attached at the start of every session:

| Layer | Holds | Changes |
|---|---|---|
| This skill | The method: verification protocol, suggestion loop, write discipline | Rarely — only when the method itself improves |
| Coding brief | The study: scope decisions, density norms, segmentation conventions | Every few interviews, as rulings accumulate |
| Case-status file | The data trail: per-interview progress, pending decisions, deliberately-uncoded passages with offsets | After every coded interview |

The brief outranks the skill wherever they conflict. At the end of every fully coded document, the skill requires Claude to deliver an updated case-status file and an explicit brief-check verdict — the two files are the skill's outputs as much as its inputs.

## Requirements

- ATLAS.ti Desktop with an active subscription, MCP Server enabled in its settings (Settings → Model Context Protocol Server — a per-machine toggle, off by default)
- Claude Desktop with the ATLAS.ti extension installed, started while ATLAS.ti is running
- This skill saved to your Claude profile

## Installation

Copy the contents of [`SKILL.md`](SKILL.md) into a new skill in your Claude profile (Settings → Capabilities → Skills), or ask Claude to create the skill from this file.

## Beyond academic research

Nothing in the method is specific to academic work. The same suggest–decide–write contract applies to any qualitative corpus with a maintained taxonomy: customer discovery and user research interviews, churn and win-loss analysis, open-ended survey responses, free-text feedback from A/B tests. The "coding brief" becomes your team's research playbook; the "case-status file" becomes your audit trail.

## Provenance

Developed by [Amit Kvint](https://amitkvint.com) during a qualitative interview study, iterating on real coding sessions with Claude connected to a live ATLAS.ti project of ~390 codes and 50+ interview documents. Every rule in the skill exists because its absence produced a real error in a real session.

## License

[MIT](LICENSE)
