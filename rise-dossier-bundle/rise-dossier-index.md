# RISE DOSSIER — master index

**What this is.** Everything produced in the Rise design sessions of 5–7 July 2026,
organised for handover. Eleven documents: two implementation briefs, four reference
models, three working HTML prototypes, one visual atlas, and one source manifest.

**Handling note (important):** Claude's working files do not persist between
conversations. This zip is the canonical copy — commit it to the repository today.
Anything reconstructed later "from memory" of these sessions should be treated as
unverified.

---

## 1. Artifact inventory

| File | What it is | Primary audience | Epistemic standing |
|---|---|---|---|
| `rise-claude-code-brief.md` | **Milestone 1**: graph schema, seed data, gap views, tests. Taxonomy v0.3 embedded verbatim as Appendix A. | Claude Code | Verified register IDs in seed rules; stack choice and scope are stated opinions |
| `rise-milestone-2-gap-engine.md` | **Milestone 2**: indicator ingestion, demand-type classification, applicability gates (Rules s 20(3) as data), four-state gap model | Claude Code | Legislated inputs verified; demand types and gap model are analysis |
| `rise-source-manifest.md` | Every instrument in scope with register IDs, verification status, and hard ingestion rules (download-only, provenance, no invented F-numbers) | Claude Code | Status column is the point: fetched-and-verified vs ID-sighted vs not-sighted |
| `rise-relationship-taxonomy.md` | v0.3 — 25 typed edges, three-dimension confidence model, MAPS_TO per NIST OLIR (verified), IP risk note (UCF/IBM) | Claude Code + developer | All previously-flagged unknowns resolved against primary sources; remaining unknowns listed in §10 |
| `rise-compliance-pyramid-model.md` | The seven-tier presentation model + complete placement map: all 66 standards with exact coordinates | Developer + team | Tiers 1–4 and every address verified; pyramid-as-view is design opinion |
| `ndis-standards-quality-indicators-plain-english-map.md` | All 66 standards mapped to their indicator sections with one-line plain-English summaries; the "seven recurring demands" | Board, pilot provider, team | Pairings verified from the eleven statutory tables; plain-English lines are labelled paraphrase |
| `rise-standards-navigator.html` | Interactive navigator: search, module filters, dual titles, cross-links, citations, authorised-download links | Everyone | Data verified; SIL absence declared in-app |
| `rise-bounce-prototype.html` | The golden-thread interaction: one indicator traced through policy → procedure → form → register with working bounce chips | Developer | Addresses and indicator substance verified; all provider content labelled invented example |
| `rise-ui-interaction-notes.md` | Analysis of the five-panel book system from the screen recording; seven design recommendations incl. pin-and-swap | Developer | Frame-verified observations separated from inference; method stated |
| `rise-visual-atlas.html` | All twelve session diagrams preserved as one page — explainers, mapping ladders, pyramid, audit series, gap engine — each captioned with its evidence status | Everyone | Diagram data matches the verified documents; captions state each figure's standing |
| `rise-graph-explorer.html` | Drill-down tree of the whole graph: Act → instruments → modules → all 66 standards, with verified content, ingestion slots for authorised text, and one worked example provider chain | Everyone | Three content grades chipped on every node: verified / slot / example |

## 2. Reading paths

- **Claude Code:** brief → source manifest → Milestone 2 → (taxonomy is inside the
  brief) → pyramid model for the address scheme. The two HTML files are reference
  implementations of the target UX, not code to reuse.
- **Developer:** this index → pyramid model → navigator → bounce prototype → UI
  interaction notes → both briefs.
- **Board / pilot provider:** plain-English map → navigator → visual atlas. Nothing else needed.

## 3. Consolidated open-questions register

| # | Question | Resolved by |
|---|---|---|
| 1 | Taxonomy §9.2–9.4: evidence at indicator vs outcome level; does OPERATIONALISES survive; do USES/RECORDS_TO generalise | Pilot provider documents + real audit reports |
| 2 | SIL standards: schedule, clauses, Guidelines sections, and whether 66 + SIL = the build's 70 | **Recorded as resolved** in the 6 Jul session "NDIS compliance policies and procedures research" (C03 = F2026C00528; SIL at ss 72B–72E; register carries 70 clause-cited standards) — retrieve that session's register, or fetch C03 to re-verify independently |
| 3 | Exact indicator count (currently "low hundreds", estimate) | Milestone 2 Step 1 parser |
| 4 | Non-adjacent spreads in the book UI (pin-and-swap recommended) | Product decision + pilot demo |
| 5 | UCF patents: AU status of the *other* families; whether any claim reads on Rise | Patent counsel + AusPat search (schema family verified US+PCT only, no AU) |
| 6 | 2026 amending instruments' register IDs | Locate on legislation.gov.au — never invent |
| 7 | Whether the register offers reliable section-level anchors for deep links | Developer test; navigator currently links document-level only |

## 4. Session verification log (what actually passed through Claude's hands)

- **Quality Indicators Guidelines 2018**, Compilation No. 1 — fetched in full twice;
  all eleven statutory mapping tables extracted; s 181D(2) authority confirmed.
- **Provider Registration and Practice Standards Rules 2018**, Compilation No. 4
  authorised PDF — fetched in full; s 20(3) applicability table, s 24 ambulatory
  reference ("as existing from time to time"), skipped-clause structure, dual
  titles, Module 6 = Verification all confirmed.
- **NIST IR 8278Ar1** — fetched; OLIR rationale enum (syntactic/semantic/functional)
  and 0–10 strength scale verified (corrected an earlier 1–9 error).
- **US8661059B1 family page** — fetched; UCF schema family = 10 US + 1 PCT, no AU
  entry; active 2024 continuations; Oregon litigation; adjacent IBM patents sighted.
- **Audit process** — Commission audit-types page + auditor guides: two-stage
  certification, participant opt-out, corrective action plans, mid-term audits.
- **UI recording** — frame-sampled (16 + 72 + 16 frames); findings in the UI notes.

Everything above is dated 5–7 July 2026 and ages from that moment. The framework
amended twice in 2026 already; re-verify against the register before load-bearing use.

## 5. One instruction for Claude Code

Read `rise-claude-code-brief.md` as the task. Before writing any seed data, execute
`rise-source-manifest.md`. Build Milestone 1, report back per the brief's §7 —
especially anything in the taxonomy that fights the implementation — then proceed
to `rise-milestone-2-gap-engine.md`. Do not resolve items in the open-questions
register silently; leave the TODOs.
