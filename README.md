# atlasti-guided-coding

A Claude Skill for guided qualitative coding in ATLAS.ti through its MCP (Model Context Protocol) integration.

The write-up of how it came about and why the division of labor is fixed the way it is: [I Taught Claude to Code My Interviews With Me, Not For Me](https://amitkvint.com/writing/ai-assisted-qualitative-coding-atlas-ti-claude/).

## What it does

The skill turns Claude into a disciplined coding assistant inside a live ATLAS.ti project. The division of labor is fixed by design:

- **Claude suggests** — codes verified against the live codebook at the moment of suggestion, each with the quoted passage itself, the code's actual definition and how established the code already is, a confidence label (strong, arguable, or stretch — with skip as the default under doubt), the best existing fallback, and a drafted quotation comment.
- **The researcher decides** — use, skip, modify, or reframe. Every analytic decision stays human, and so does coverage: Claude never pre-sorts the transcript. Every passage reaches the researcher in transcript order, as a suggestion, a recommended skip, or an uncoded anchor, so nothing is left out by Claude's silence.
- **Claude executes** — only approved quotations are written, at exact character offsets computed by string search in the same turn, each write is checked against the returned text and logged on disk, and the log is compared against the live project after every reconnect.

Two working modes are supported: a walk-through (one suggestion, one decision, one write, repeat) and a section-pass (a full section's suggestion list delivered for the researcher to code themselves, followed by a compact matched/missed comparison).

## The three-layer architecture

The skill deliberately contains no study-specific knowledge. It expects two companion documents per study, attached at the start of every session:

| Layer | Holds | Changes |
|---|---|---|
| This skill | The method: verification protocol, suggestion loop, write discipline | Rarely — only when the method itself improves |
| Coding brief | The study: research question and analytic frame, scope decisions, density norms, segmentation conventions | Every few interviews, as rulings accumulate |
| Case-status file | The data trail: per-interview progress, pending decisions, deliberately-uncoded passages with offsets | After every coded interview |

The brief outranks the skill wherever they conflict. If the brief does not state what the study asks and through what lens, Claude asks once before the first suggestion — coding without the frame produces plausible codes for the wrong study.

At the end of every fully coded document, the skill requires a close-out, in order:

1. **Verify** the live quotation list against Claude's on-disk log.
2. **A contrary-reading pass** over every stretch left uncoded, looking for the reading not taken the first time — the uncoded remainder is where an assistant's first reading hides its bias.
3. **A compact summary** ending in a fixed set of session figures (quotations, code applications, skip ratio, confidence distribution, process lapses), so sessions can be compared and reported in a methods section.
4. **An updated case-status file**, edited in place in the study's own document.
5. **An explicit brief-check verdict**, with a drafted next version of the brief when anything codebook-level emerged.
6. **A skill check** — whether anything learned is study-independent and belongs in this skill instead.

The companion files are the skill's outputs as much as its inputs.

## Requirements

- ATLAS.ti Desktop with an active subscription, MCP Server enabled in its settings (Settings → Model Context Protocol Server — a per-machine toggle, off by default)
- Claude Desktop with the ATLAS.ti extension installed, started while ATLAS.ti is running
- This skill saved to your Claude profile

## Installation

Copy the contents of [`SKILL.md`](SKILL.md) into a new skill in your Claude profile (Settings → Capabilities → Skills), or ask Claude to create the skill from this file.

## Beyond academic research

Nothing in the method is specific to academic work. The same suggest–decide–write contract applies to any qualitative corpus with a maintained taxonomy: customer discovery and user research interviews, churn and win-loss analysis, open-ended survey responses, free-text feedback from A/B tests. The "coding brief" becomes your team's research playbook; the "case-status file" becomes your audit trail.

## Provenance

Developed by [Amit Kvint](https://amitkvint.com) during a qualitative interview study, iterating on real coding sessions with Claude connected to a live ATLAS.ti project of ~390 codes and 50+ interview documents. Most rules in the skill exist because their absence produced a real error in a real session; the rest came from methods discussions about what makes an assistant's involvement defensible in a study.

## How to cite

If the skill informs published work — a methods section, a course, a tool — please cite it:

> Kvint, A. (2026). *atlasti-guided-coding: a Claude skill for guided qualitative coding in ATLAS.ti* (Version 1.1.0) [Computer software]. https://github.com/amitkvint/atlasti-guided-coding

GitHub's "Cite this repository" button gives the same reference in APA and BibTeX, from [`CITATION.cff`](CITATION.cff).

## License

[MIT](LICENSE). Need different terms, for example to include this in a GPL or LGPL project? Ask; I am the sole copyright holder.
