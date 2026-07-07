# Rise Collection Manifest & Assembly Plan
**Version 0.1 — 6 July 2026**

The single map of every known Rise artefact across all sessions: what it is, where it lives now, and how to assemble the collection into one working structure.

---

## 0. Honesty statement about this inventory itself

This manifest was compiled from (a) files verified on disk **this session** and (b) prior-session records retrieved **today** via conversation search. That means:

- **"In this pack"** entries are verified present — I listed the directory before writing this.
- **"Your downloads only"** entries are artefact names and descriptions as recorded in prior session summaries and handoff text. I have **not** seen those files this session and cannot verify their current existence, integrity, or exact contents. The descriptions are faithful reproductions of the prior records, not fresh inspections.
- The inventory **may be incomplete** — conversation search returns excerpts, not exhaustive listings. Your downloads folder is the authoritative census. If an artefact you remember isn't listed here, the omission is a retrieval limit, not a judgement.
- Confidence: **high** that the listed artefacts were produced (multiple consistent records); **not verifiable from here** that you still hold them.

---

## 1. Full inventory by session

### Session A — 6 Jul 2026 (this session): auditor deep-research & indexed checklist
| Artefact | Status | Role |
|---|---|---|
| `how-ndis-auditors-check-practice-standards.md` | **In this pack** (`01-guide/`) | Method: how AQAs test provider artefacts against the standards; real-report anatomy; 2026 changes. |
| `rise-ndis-audit-checklist-indexed.md` | **In this pack** (`02-checklist/`) | Application: per-standard auditor test + evidence, keyed to Rise IDs and dual addresses. 48 full / 6 partial / 16 gap. |
| `ndis-standards-coverage-map.html` | **In this pack** (`03-visuals/`) | State: standalone visual of indexing completeness across all 70 standards. |
| Coverage-map chat widget | Chat-only (superseded by the HTML above) | Same data; the HTML file is the durable version. |

### Session B — 5–6 Jul 2026: NDIS compliance build (developer handoff)
*All items below: **your downloads only** — primarily inside `rise-ndis-package.zip`. Descriptions from the session's own handoff records.*

| Artefact | Role |
|---|---|
| `rise-developer-handoff.md` | The package's own index — start-here for Session B contents. |
| `rise-document-register.xlsx` | Master register: READ ME, Documents (~121–123), **Standards (70, clause-cited)**, Legislation (17–21 instruments), Edges (~515–528). Itself document `REG-GOV-03`. **One of the two files that closes this pack's gaps.** |
| `rise-nodes-and-edges.json` | Machine-readable seed graph (~218–224 nodes, ~515–528 edges). |
| `rise-node-examples.json` | One fully-attributed example per node type (bitemporal fields, enums, MAPS_TO dimensions). |
| `rise-node-map.mermaid` | Meta-model diagram: node types, core typed edges, both layers. |
| `rise-node-taxonomy.md` v0.1 | Node-type schema (companion to edge taxonomy v0.3). |
| `rise-document-architecture.md` v0.1 | Compliance Header spec, document ID scheme, traceability views, accessibility rules. |
| Templates: `TPL-POL / PRO / WIN / FRM / REG` (.md + .docx) | The five document templates; incident chain as worked example. |
| ~123 drafted documents (Markdown, by type folder) | The full provider suite drafts. |
| `rise_build.py`, `rise_docs.py`, `rise_dossier.py` | Generators — single source of truth → xlsx + JSON + docs + dossier. |
| Interactive HTML dossier | Graph explorer, document reader, type tabs, chain bar. |
| Auditor focus map (QI-section-cited) | Per-module "what auditors open first" — partially reproduced into this pack's checklist. |
| Plain-English compliance guide; tiered source register; methodology doc | Supporting references. |
| **Note:** counts vary across records (121 vs 123 docs; 218/515 vs 224/528 nodes/edges) — likely snapshots at different build points within the session. The register's own READ ME sheet is authoritative. |

### Session C — 6 Jul 2026: standards mapping & navigator
*Your downloads only.*

| Artefact | Role |
|---|---|
| `ndis-standards-quality-indicators-plain-english-map.md` | **All 66 pre-SIL standards with exact Rules + Guidelines addresses from the eleven statutory mapping tables.** The other gap-closing file. |
| `rise-standards-navigator.html` | Interactive navigator: search, module chips, expandable cards, dual-title flags (8 standards), cross-module family links, copy-citation. |
| Seven-tier compliance pyramid + progressive visual explainers | Teaching visuals, four-box model → single-indicator testing flow. |
| Source manifest (for Claude Code ingestion) | Governs authorised-copy ingestion from the register. |

### Session D (earlier): edge taxonomy
*Your downloads only.*

| Artefact | Role |
|---|---|
| `rise-relationship-taxonomy.md` **v0.3** | The authoritative 25-type edge taxonomy, five groups. Session B's handoff explicitly says to place it beside the package files. v0.4 (REFERENCES/AMENDS) is queued. |
| Claude Code implementation brief (v0.3 appendix) | Build brief with honesty rules and TODOs. |

### Session E: IBM OpenPages research
*Chat-record only (no file deliverable recorded).* Findings: RCM Mandate→Sub-Mandate→Requirement parallel; IBM licenses UCF (FTO signal); demo/documentation links.

---

## 2. Proposed unified structure (assembly target)

**Design opinion** — consistent with Session B's handoff and the single-source generator pattern:

```
rise/
├── README.md                        ← promote Session B's rise-developer-handoff.md, add pointers to research/
├── taxonomy/
│   ├── rise-relationship-taxonomy.md        (v0.3 — Session D)
│   ├── rise-node-taxonomy.md                (v0.1 — Session B)
│   └── rise-document-architecture.md        (v0.1 — Session B)
├── data/
│   ├── rise-document-register.xlsx          (Session B — authoritative counts)
│   ├── rise-nodes-and-edges.json
│   ├── rise-node-examples.json
│   └── rise-node-map.mermaid
├── scripts/
│   ├── rise_build.py │ rise_docs.py │ rise_dossier.py
├── templates/
│   └── TPL-POL / PRO / WIN / FRM / REG (.md + .docx)
├── documents/                        (the ~123 drafts, by type folder)
├── site/
│   ├── rise-dossier.html                    (Session B)
│   ├── rise-standards-navigator.html        (Session C)
│   └── ndis-standards-coverage-map.html     (THIS PACK)
├── reference/
│   ├── ndis-standards-quality-indicators-plain-english-map.md   (Session C)
│   ├── auditor-focus-map + plain-english guide + source register (Session B)
│   └── source-manifest (Session C)
└── research/                         (THIS PACK, 6 Jul)
    ├── how-ndis-auditors-check-practice-standards.md
    └── rise-ndis-audit-checklist-indexed.md
```

Trade-off noted: this tree hand-places generator *outputs* (documents/, site/) beside sources; your generators treat outputs as disposable. Alternative: keep only sources + scripts in the repo and regenerate outputs — cleaner, but requires the scripts to run in your environment first. Either is defensible; the register + scripts + taxonomies are the non-negotiable core.

---

## 3. Gap-closure map

| Gap (in this pack's checklist/map) | Closed by | How |
|---|---|---|
| M2-3…M2-7 names/addresses | Plain-English map **or** register Standards sheet | Direct row copy — no inference. |
| M2A-1…M2A-8 (all) | Same | Same. |
| M3-1…M3-4 names/addresses; M3-5 name | Same | Same. |
| SIL-1…4 standard names + Rules clauses | Register (Session B verified SIL from C03) **or** fresh C03 fetch | Prefer the register; fetch as currency check. |
| Ordinal reconciliation (M4/M5/VER Rise IDs marked `[D]`) | Register Standards sheet | Confirm my QI-section ordering matches your assigned IDs. |
| Currency of all `[V-prior]` addresses | Fresh fetch of PRPS Rules + QI C03 | A *check*, not a source — diff against register, don't re-derive. |

---

## 4. Standing risks to carry forward

1. **Session-scoped files** (established, repeatedly validated): download everything, every session. This manifest included.
2. **Compilation drift**: the 2026 amendments mean any address not checked against the in-force compilation is provisional. Bitemporal discipline in the graph is the mitigation — the manifest just reminds you the *inputs* need the same discipline.
3. **Count discrepancies across records** (121/123, 218/224, 515/528): treat the register's READ ME as authoritative; if it disagrees with the JSON, the generator scripts are the arbiter (regenerate and compare).
4. **This inventory's completeness**: bounded by conversation-search retrieval. Reconcile against your actual downloads once, then this manifest becomes the living index (version it like everything else — v0.2 after reconciliation).
