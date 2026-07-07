# Rise — Developer Handoff: NDIS Document & Graph Import Package

**v0.1 — 2026-07-05.** Everything needed to start importing legislation, standards,
policies, procedures, forms and registers into the Rise platform. Read this file first;
it indexes the rest.

---

## 1. What this package is

A complete, internally consistent seed for the Rise compliance graph and its document
layer, for the NDIS framework as at July 2026 (including the SIL module that commenced
1 July 2026). It contains the **schema** (node + edge taxonomies), the **seed data**
(224 nodes, 528 edges), the **human-readable register** (the workbook), the **document
templates** the content will be authored into, and the **canonical examples** a developer
implements against. The generator script is included so the dataset can be regenerated
from one source of truth.

One file referenced throughout is **not** in this package because it was delivered in an
earlier session: `rise-relationship-taxonomy.md` **v0.3** — the authoritative edge
taxonomy (25 typed edges, five groups). Put it in the repo beside these files.

## 2. File manifest

| File | What it is | Role tomorrow |
|---|---|---|
| `rise-developer-handoff.md` | This index | Start here |
| `rise-document-register.xlsx` | Master register: READ ME, Documents (123), Standards (70, clause-cited), Legislation (21), Edges (528) | Human-readable mirror of the seed data; the suite build plan; itself document REG-GOV-03 |
| `rise-nodes-and-edges.json` | Machine-readable seed: 224 nodes, 528 edges | The import payload |
| `rise-node-examples.json` | One fully-attributed example per node type + representative edges | The shapes to implement (bitemporal fields, enums, MAPS_TO dimensions) |
| `rise-node-map.mermaid` | Meta-model diagram: every node type, core typed edges, both layers | The picture for the wall / repo README |
| `rise-dossier.html` | Live-linked dossier: the whole dataset browsable in any browser, with verification stamps and FRL/Commission links | Share/view online; regenerate via `rise_dossier.py` |
| `rise-plain-english-guide.md` | The whole system explained for anyone | Onboarding; participant-facing tone reference |
| `rise-document-suite-v0.1.zip` | All 123 documents as Markdown drafts — full compliance headers generated from the graph; incident chain fully drafted; other bodies are marked scaffolds | The authoring baseline; also embedded, clickable, in the dossier's Reader |
| `rise-auditor-focus-map.md` | Plain-English map of every area auditors examine, with QI Guidelines section numbers (C03) and the Rise documents that answer each | The retrieval patterns the platform must serve |
| `rise-sources.md` | Tiered source register: every claim traced, access-dated, incl. negative findings | Provenance; also rendered in the dossier's Sources section |
| `rise-methodology.md` | The build logic in plain English: verification ladder, gap sweeps, conflict rules | How to challenge or extend the dataset |
| `rise-node-taxonomy.md` v0.1 | Node-type schema (companion to edge taxonomy v0.3) | Schema reference |
| `rise-document-architecture.md` v0.1 | How documents render the graph: Compliance Header spec, ID scheme, traceability views, accessibility rules | Governs document generation and the header round-trip |
| `TPL-POL / PRO / WIN / FRM / REG` (.md + .docx) | The five document templates, incident chain as worked example | Authoring targets for the 121 planned documents |
| `rise_build.py` + `rise_docs.py` + `rise_dossier.py` | Generators: one dataset → xlsx + JSON + 123 documents + HTML dossier, with a dangling-edge assertion | Regeneration and future edits |

## 3. The data model on one page

Two layers. **Shared** (one copy, centrally maintained): Instrument → Provision;
Framework → Module → Standard → Quality Indicator. **Tenant** (per provider):
Organisation, Registration Scope, Site, Document (8 doc_types), Role, Person, Training,
Risk, Control, Evidence, Audit, Finding, Improvement Action. Edges cross the layer
boundary read-only from the tenant side (`IMPLEMENTS`, `EVIDENCES`, `ASSESSES`,
`MAPS_TO`).

**Terminology mapping (important):** what the node taxonomy and this package call a
**Standard** is what the edge taxonomy v0.3 calls a **Requirement** (its hierarchy reads
Framework → Module → Outcome → Requirement → Indicator; we collapsed Outcome into the
`division` attribute). Same object, two names — pick one in code (recommendation:
`Standard`, matching NDIS language) and note the alias.

**Everything is bitemporal** (`effective_from/to` + `recorded_at/superseded_at`) and
everything carries `assertion_source` + `verification_status` as independent dimensions.
Edge direction points **toward authority**. `RELATES_TO` always requires a note.

The one non-negotiable product behaviour this enables: **legislative-change fan-out** —
an amendment lands on an Instrument, and a graph traversal produces the review list of
every affected document.

## 4. Import plan (recommended order)

1. **Shared instruments** — `nodes` where `node_type=Instrument` (17). Then the
   legislative edges (`MADE_UNDER`, the `RELATES_TO` amendment edges).
2. **Framework layer** — Framework, 9 Modules, 70 Standards (with `citation`), then
   `PART_OF` / `PUBLISHED_IN` edges.
3. **Tenant document nodes** — the 121 Documents (all `status: Planned`), expanding each
   to the full shape in `rise-node-examples.json` (defaults: `recorded_at=now`,
   `assertion_source=human`).
4. **Document edges** — `IMPLEMENTS`, `OPERATIONALISES`, `USES`, `RECORDS_TO`, and the
   noted `RELATES_TO` set.
5. **Validation gates** (fail the import on any): no dangling endpoints (the generator
   already asserts this); domain/range legality per taxonomy v0.3; every `RELATES_TO`
   has a note; every node has both temporal pairs; every Document has ≥1 `IMPLEMENTS`
   or an explicit exemption.
6. **Smoke queries** — "all documents implementing CORE-2.6", "all documents citing the
   PRPS Rules" (fan-out dry run), "standards in scope with no IMPLEMENTS edge" (gap
   detection; needs a RegistrationScope row — see the ExampleCare sample).

The workbook's Documents sheet is the same data with filters — use it to eyeball what
the queries should return.

## 5. Verification state — what to trust

Legend (workbook READ ME): **V** verified against regulator/FRL sources on 5 Jul 2026 ·
**C** corroborated training knowledge · **T** confirm against the current compilation ·
**D** draft-source (SIL wording). Current spread: 66 of 70 standards verified **to schedule and clause** against the FRL compilation table of contents (fetched 5 Jul 2026); the 4 SIL standards remain draft-source. 21 instruments, all V or C, with FRL series IDs verified where published (F2018L00631 PRPS,
F2018N00114 AQA Guidelines, F2018L00632 RP Rules, F2018L00629 Code of Conduct,
F2018L00887 Worker Screening, F2018N00041 QI Guidelines, plus the new **Approved Quality Auditors Rules 2025, F2025L01383**, and the NDIS Act itself at C2013A00020). The three 2021 insertions now cite cleanly (emergency & disaster management Sch 1 cl 16A; mealtime management cl 26A; severe dysphagia Sch 2 cl 4A), and standard titles align to the official clause headings.

Known soft spots, in order of priority: (a) **SIL standards final wording** — commenced
1 Jul 2026; register carries draft-derived names, confirm against the made Amendment
Rules; (b) the latest **published compilation is C04 (15 Nov 2021)** — the 2026 amendments are law but not yet consolidated at the FRL 'latest' URL, so SIL clause locations stay TBC; (c) **quality indicators** — the QI
Guidelines' indicator text is *not yet imported* (placeholder shape only; never invent
indicator text); (d) two Commission guidelines (Notice of Changes and Events 2019; Behaviour Support Practitioner Application 2020) still need their FRL ids pulled. UPDATE 6 Jul: quality-indicator references are now verified for all 70 standards against QI Guidelines compilation C03 (F2026C00528, 1 Jul 2026), which also consolidates Module 5A (SIL) — SIL standard names upgraded to Verified; only their PRPS clause pinpoints remain TBC. Indicator TEXT stays pointer-only by design (copyright and never-invent rules); full-text ingestion is the platform task.

Suite composition, IDs, priorities, owners and review cycles are **design
recommendations**, not regulatory requirements.

## 6. What's worth taking from the IBM OpenPages review (5 Jul session)

1. **Structural parallel, verified:** OpenPages RCM models a Mandate → Sub-Mandate →
   Requirement hierarchy with regulatory-feed connectors, retains past and future
   versions of regulatory text on Requirements, and auto-generates workflows from
   regulatory events. Independent commercial validation of two Rise day-one choices:
   versioned requirement nodes and change fan-out. Worth mirroring: keep dated text
   versions retrievable *on the Standard/Provision node*, not only in documents.
2. **Freedom-to-operate signal, verified:** even IBM licenses UCF content via a
   connector rather than replicating UCF's model. Rise should keep doing the same —
   build no UCF-shaped harmonised-control layer without an FTO review. Related caution
   from the earlier patent search: IBM holds an adjacent patent on live compliance
   crosswalks responding to regulatory change — proximate to our fan-out feature;
   flag for FTO review alongside UCF.
3. **AI-agent direction, verified:** OpenPages now ships an MCP Server for agents to
   create/query/update GRC objects. Rise's `ai_proposed` + `unverified` pipeline is the
   same trajectory; an MCP interface over the graph is a natural roadmap item.
4. **Differentiation, inference (not verified):** OpenPages appears to be an
   object-association relational model — no evidence found of typed-edge semantics,
   set-theoretic crosswalks, or bitemporal snapshots. That gap is plausibly Rise's
   moat; treat as open until someone gets hands-on with the trial.
5. **Useful further reading** (from that session, links in the chat): the OpenPages
   Solutions Guide object-model PDF (v7.4 — concepts, not current state) and the RCM
   demo video.

Other standing references from the taxonomy work: NIST OSCAL (mapping model as prior
art), NIST IR 8278Ar1/OLIR (source of the verified MAPS_TO dimensions), W3C SKOS, and —
noted but not re-verified — Akoma Ntoso / OASIS LegalDocML as the XML standard worth
following when full legislative text is imported into Instrument/Provision nodes.

## 7. Open decisions (need answers, none block tomorrow's import)

1. **Version modelling** — separate node per document version sharing a `logical_id`,
   vs one node + history table. The `SUPERSEDES` example in `rise-node-examples.json`
   shows the question concretely. My lean: separate nodes (auditors ask for "the policy
   as it stood on date X", and `SUPERSEDES` edges then do the work), at the cost of
   more nodes.
2. **Edge taxonomy v0.4** — adopt `REFERENCES` (Document → Instrument/Provision) and
   `AMENDS` (Instrument → Instrument). Today ~130 `RELATES_TO` edges carry these as
   notes; that's the escape-hatch smell the taxonomy says to refactor.
3. **Participant node** — deliberately excluded (privacy blast radius); participant
   records key to the CRM. Revisit only if per-participant compliance views become core.
4. **QI Guidelines import** — the next shared-data task after tomorrow.
5. **Registration-group → module applicability table** — the dataset that lets
   RegistrationScope auto-derive which modules apply (the Commission's 'initial scope
   of audit' mechanism). Needed before gap detection can run for a real tenant.
6. **Standing watch list** — tracked in the dossier's Watch section: the Securing the
   NDIS for Future Generations Bill 2026, mandatory-registration phasing to 2030
   (support-coordination timing unresolved), the Practice Standards Review, the AQA
   Rules 2025 / 2018 Guidelines relationship, QI import, jurisdictional overlays, the Akoma Ntoso/LegalDocML revision due late Jul 2026 (structure future legislative-text imports on it), and FRL programmatic-access status — no public API found for legislation.gov.au; the UK register's open API is the integration benchmark.
7. Two fragments from your earlier voice note I still can't resolve: something about
   "the financial" (no financial document exists in any Rise chat I can search) and
   "going into that country". If either matters for the import, clarify and I'll fold
   it in.

## 8. Regenerating the dataset

Edit the data blocks in `rise_build.py` (LEG / MODULES / STD / DOCS / edge lists), run
`python3 rise_build.py`, then recalculate the workbook. The script asserts referential
integrity before writing anything. Markdown is canonical for documents; docx is an
export — never edit the docx as master.
