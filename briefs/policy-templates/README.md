# Rise policy templates: one policy, three layers
**Version 0.1, 14 September 2026.** Built this session on Harmony Care Support Services' own Risk Management Policy, rendered on their locked letterhead. Complements the five `TPL-*` skeletons in `rise-ndis-package/` and the production standard in `rise-authoring-research/`; it does not replace either. It delivers the "Easy Read companion" that the collection flags as undrafted, as a plain-language summary with picture slots, awaiting illustrations.

Labels: **[V-now]** verified this session against the cited source · **[C]** corroborated across secondary sources · **[D]** design decision.

## What is here

| Path | What it is |
|---|---|
| `pdf/templates/` | The three blank templates. Every slot is in brackets and says what goes in it. |
| `pdf/worked-example/` | The same three layers filled with the Risk Management Policy: reference (14 pp), worker card (1 p), participant summary (3 pp). |
| `renderer/` | `hcpdf.py` and `layout.py` (the letterhead renderer), the four band images, and `templates/` with the two source files, four JSON configs, `layers.py` (worker card and participant page) and `build_template.py` (turns a provider policy into the marked-up source). |

## The three layers **[D]**, after Waller, Passera and Haapio's layered-contract model **[V-now]**

| Layer | Reader | Rule |
|---|---|---|
| Reference | Provider, auditor | Every word as approved. 11 pt Helvetica, 62 characters a line (was 101 at full measure). Compliance links page first. Marginal column carries the standard, quality indicators, law, records and review date beside the clause. Section 4 as numbered steps, obligation words in bold. |
| Worker card | Support worker | The procedure as a checklist: tick box, step in the policy's own words, who, record. One page on the compact letterhead. |
| Participant summary | Participant, family | 16 pt, 1.5 line spacing, one idea per sentence, hard words in bold, a picture slot per idea, a word list. Marked as a summary. New words: the policy stays the document that applies. |

## Sources **[V-now]**, all accessed 14 Sep 2026
Round Table Guidelines for Producing Clear Print 2022 (12 pt minimum, sans, left aligned, bold not italic, 1.2 spacing, 1.5 above 14 pt) · Australian Government Style Manual: Easy Read; sentence length (average 15 words, never over 25); headings (under 70 characters, sentence case) · Vision Australia typography guidance · NDIS Commission participant information pack (Easy Read) · Waller, Passera and Haapio, *Layered Contracts*, Springer 2022 · W3C, *Making Content Usable for People with Cognitive and Learning Disabilities* · ISO 24495-1:2023 · Federal Plain Language Guidelines and ACUS on must / must not / should / may · Gawande, *The Checklist Manifesto* (WHO checklist: 19 items, 36% fewer complications, eight hospitals) **[C]** · FDA Physician Labeling Rule 2006 (the half-page Highlights section).

## To make a new policy
1. Copy `renderer/templates/src/TEMPLATE Policy and Procedure.md`, fill every `[slot]`. Markup: `# 1. Section`, `## 1.1 Sub`, `%% (a) clause`, `@standard note` (marginal column), `!! sentence` (key commitment), `>> Step | Who | Record` then `- action` lines, `| table |`.
2. Copy `spec_TEMPLATE.json` (title, control data, six `links` rows; `"base": 11` is the type size) and `layers_TEMPLATE.json` (participant items of fifteen words or fewer, and the word list).
3. From `renderer/`: `python3 hcpdf.py templates/spec_<name>.json` and `python3 templates/layers.py templates/layers_<name>.json`. Needs `reportlab`.

## Known limits
Word output does not carry the new markup; PDF is the artefact. `build_template.py` reads the provider's full document set, which is not in this repository; the generated source it produced is included. The two findings it surfaced in the provider's own paper (a review-date conflict between the policy's 5.3 and the Policy Register; a Related Documentation clause that names no document) belong to the provider and are recorded on the worked example's links page.
