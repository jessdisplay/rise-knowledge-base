# Rise Audit Pack — 6 July 2026
### Master index for this session's deliverables, and the assembly map for the whole Rise collection

**Prepared for:** Rise Development
**Session:** NDIS auditor deep-research → indexed checklist → coverage visual (6 Jul 2026)

---

## 1. What this pack IS and IS NOT — read first

**This pack contains only what was produced in the 6 July audit-research session.** It does **not** contain the earlier Rise deliverables — the interactive dossier, the 123 drafted documents, the register workbook, the seed graph JSON, the templates, the generator scripts, the standards navigator, or the progressive explainers. Those were built in *previous sessions*, and Claude's file environment does not persist between conversations. They exist **only in your downloads** (chiefly `rise-ndis-package.zip` and the individually delivered files).

Nothing in this pack was reconstructed from memory. Where prior-session content was needed (the indexing scheme, the placement map), it was retrieved via conversation search and reproduced with `[V-prior]` labels; where it could not be retrieved, it is marked `[GAP]` and left blank. This is deliberate — reconstructing clause citations or node data from memory is the failure mode the Rise source-discipline exists to prevent.

`04-manifest/rise-collection-manifest.md` is the piece that "organises everything": it inventories the full cross-session collection, states where each artefact lives, and proposes the unified folder structure to assemble once you re-upload the prior files.

---

## 2. Contents of this pack

| Path | What it is | Status |
|---|---|---|
| `01-guide/how-ndis-auditors-check-practice-standards.md` | The layered deep-research guide: age-5 → plain English → regulatory stack → auditor mechanics → anatomy of a **real 2022 certification audit report** → best-practice checklist → 2026 changes. Full V/C/T/D labelling. | Produced this session. Research verified against NDIS Commission guidance + one real audit report read in full. |
| `02-checklist/rise-ndis-audit-checklist-indexed.md` | The per-standard checklist keyed to the Rise ID scheme and dual statutory address (Rules clause + QI section). 48 full rows, 6 partial, 16 explicit gaps. | Produced this session. Addresses `[V-prior]` — reproduced from prior verified work, **not re-verified today**. |
| `03-visuals/ndis-standards-coverage-map.html` | Standalone, offline, print-safe version of the coverage map shown in chat: all 70 standards, colour + symbol coded by indexing completeness, counts computed from the cell data at render time. | Produced this session. Same data as the checklist — single source of truth. |
| `04-manifest/rise-collection-manifest.md` | The cross-session inventory and assembly plan: every known Rise artefact, where it lives, what's missing, and the proposed unified repo tree. | Produced this session. Inventory derived from conversation-search retrieval — see its own honesty section for limits. |
| `README.md` | This index. | — |

**How the three content pieces relate:** the *guide* explains how auditors work (method); the *checklist* applies that method per standard using your indexing (application); the *coverage map* shows at a glance where the indexing is solid vs gapped (state). One dataset underlies the checklist tables and the map cells.

---

## 3. Known limits of this pack

- **`[V-prior]` ≠ re-verified.** Every statutory address was verified in a *prior* session against the fetched instruments; none were re-fetched today. The 2026 SIL amendment inserted sections — re-validate against the current compilations (PRPS Rules `F2018L00631`; QI Guidelines `F2018N00041` → C03 `F2026C00528`) before anything enters the graph or reaches a provider.
- **16 gaps are real gaps** (Module 2 beyond M2-2, all of Module 2A, most of Module 3, SIL names/Rules clauses). They close with zero guessing once you re-upload `ndis-standards-quality-indicators-plain-english-map.md` or the register workbook.
- **The real audit report** analysed in the guide is one provider, one AQA, 2022 — a genuine and rich exemplar, but a sample of one. No public register of NDIS audit reports was found (recorded as a `[T]` negative finding).

---

## 4. Immediate next steps

1. **Download and retain this pack** — it will not survive this session.
2. **Re-upload the two source files** (`ndis-standards-quality-indicators-plain-english-map.md` and/or `rise-document-register.xlsx`) → all 16 gaps + 6 partials get filled from your own verified data.
3. **Assemble the unified collection** per the manifest's proposed tree, placing this pack's contents alongside the prior package.
4. Optional integrations once sources are re-uploaded: merge the checklist + coverage map into the dossier as new tabs (matching your single-source generator pattern), and/or emit the checklist as machine-readable seed JSON keyed by Rise ID.

---
## Changelog
- **v2 (6 Jul 2026, later same day):** Added `00-source/` containing the uploaded NDIS Commission booklet (Nov 2021, v4) — the pack is now self-contained for name-level verification. Added `02-checklist/rise-reconciliation-2021v4-booklet.md` recording the mapping of that booklet against the checklist: 16 hard gaps → 0 (all names now verified; 18 QI-section pairings are labelled inference, not verification). Coverage map v1 replaced by `03-visuals/ndis-standards-coverage-map-v2.html`. Remaining opens: Rules clauses for M2-3..7 / M2A / M3-1..4, SIL names + clauses, and [I]→[V] conversion — all still require the register or an FRL fetch.
