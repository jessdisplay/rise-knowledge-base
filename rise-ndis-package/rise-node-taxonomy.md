# Rise Node Taxonomy

**Version 0.1 — 2026-07-05.** Companion to `rise-relationship-taxonomy.md` v0.3 (the edge
taxonomy). That document governs *how things connect*; this one governs *what the things
are* and what every node must carry so the graph can be rendered as audit-ready documents.

**Changelog** — v0.1: initial release. Node set derived from the vision-document chain,
the v0.3 edge domain/range rules, and the July 2026 NDIS regulatory state (SIL module,
mandatory SIL/platform registration).

---

## 1. Design principles

1. **Node metadata is the document header.** Every attribute defined here either renders
   directly into the Compliance Header of a Word/Markdown document (see
   `rise-document-architecture.md` §4) or exists to answer an auditor's question. No
   ornamental fields.
2. **Shared vs tenant is a node property, not an afterthought.** Instruments, frameworks,
   modules, standards and quality indicators are `layer: shared` (one copy, maintained
   centrally, versioned). Documents, risks, evidence, audits, findings and roles are
   `layer: tenant` (private to one provider). No edge may silently move data across that
   boundary; cross-layer edges (`IMPLEMENTS`, `PUBLISHED_IN`, etc.) are read-only from the
   tenant side.
3. **Every node is bitemporal.** `effective_from` / `effective_to` state when the thing
   was true in the world; `recorded_at` / `superseded_at` state when the database believed
   it. This is what makes "compliance state as at 30 June 2026" answerable — carried over
   unchanged from the v0.3 decision.
4. **Verification is a dimension, not a node type.** Shared nodes carry
   `assertion_source` (human / import / rule / AI) and `verification_status`, exactly as
   edges do in v0.3. A Standard imported from a scraped compilation is not the same
   epistemic object as one checked against the Federal Register of Legislation.
5. **Identifiers are preserved, never invented.** Legislative nodes keep their native
   citations (Part/Division/Section numbers, FRL register IDs). Rise IDs (`CORE-2.6`,
   `POL-INC-01`) are stable handles layered on top, and the mapping between the two is
   itself data.

---

## 2. Common attributes (all nodes)

| Attribute | Req. | Notes |
|---|---|---|
| `id` | yes | Stable handle. Shared nodes: framework-derived (`CORE-2.6`, `SIL-1`). Tenant documents: `TYPE-DOMAIN-NN` (`POL-INC-01`). |
| `node_type` | yes | One of §3–§4. |
| `title` | yes | Plain-English name. |
| `status` | yes | `draft / in_review / approved / superseded / retired` (documents); `in_force / amended / repealed` (instruments). |
| `effective_from`, `effective_to` | yes | Valid time. Open-ended `effective_to` = currently in force. |
| `recorded_at`, `superseded_at` | yes | Transaction time (system-set). |
| `assertion_source` | yes | `human / import / rule / ai_proposed` — v0.3 semantics. |
| `verification_status` | yes | `verified / corroborated / unverified / draft_source` — see register legend. |
| `layer` | yes | `shared / tenant`. |
| `note` | no | Free text; required where this taxonomy says so. |

---

## 3. Shared reference nodes

| Node type | What it is | Type-specific required attributes |
|---|---|---|
| **Instrument** | An Act, Rules, Rule, Guidelines or amending instrument. | `kind` (Act / Rules / Guidelines / Amending Act / Amending Rules), `jurisdiction`, `frl_id` (Federal Register of Legislation series/compilation ID, when known), `compilation_no`. |
| **Provision** | A Part, Division, Section, Schedule or clause *inside* an Instrument. | `citation` (native numbering, e.g. "Sch 2, Pt 4"), `provision_kind`. Linked upward with `PART_OF`; never renumbered. |
| **Framework** | A named quality framework as a whole — "NDIS Practice Standards". Exists so multi-framework tenants (NDIS + Aged Care Strengthened Standards + ISO 9001) hang off parallel roots. | `regulator`, `audit_scheme` (e.g. approved-quality-auditor certification/verification). |
| **Module** | Core, Verification, Modules 1–5, SIL. Determines applicability. | `applies_when` (plain-English applicability), `commencement`. |
| **Standard** | The auditable requirement unit ("Incident management", "Supported decision-making"). The domain/range target of `IMPLEMENTS`. | `division`, `outcome_statement_ref` (pointer to source text, not a copy), `participant_statement_ref` (SIL-style, where the instrument provides one). |
| **QualityIndicator** | An indicator auditors assess under a Standard (from the Quality Indicators Guidelines 2018 as amended). | `indicator_ref`, `PART_OF → Standard`. |

**Why Standards point to source text rather than embedding it:** the outcome statements
are legislative text that gets amended; storing a pointer plus a retrieved-on date keeps
the copyright surface small and makes staleness detectable. (Design decision, my
recommendation.)

---

## 4. Tenant nodes

| Node type | What it is | Type-specific required attributes |
|---|---|---|
| **Organisation** | The provider (tenant root). | `registration_no`, `registration_groups`, `audit_pathway` (certification / verification). |
| **RegistrationScope** | What the provider is registered to deliver → which Modules apply. **This node drives gap detection**: a gap only exists for standards inside scope. | `modules_in_scope[]`, `effective dates` (scope changes over time — SIL registration from 1 Jul 2026 is exactly such a change). |
| **Site / Home** | A physical service setting (an SIL house, an office). SIL practice-governance evidence is house-level. | `site_kind`, `address_ref`. |
| **Document** | Any governed document. `doc_type`: `policy / procedure / work_instruction / form / register / plan / agreement / handbook`. | `doc_type`, `owner_role → OWNED_BY`, `review_cycle_months`, `easy_read_available` (bool), `easy_read_of` (link when this node *is* the Easy Read companion), `format[]` (docx / md / xlsx). |
| **Role** | Accountable or performing role ("Quality Manager"). People are assigned to roles separately — audits survive staff turnover. | `role_kind`. |
| **Person** | Optional; only where worker-level evidence is needed (screening, competency). Store the minimum. | `screening_check_ref`, `screening_expiry`. |
| **TrainingCourse / Qualification** | Competency targets of `REQUIRES`. | `delivered_by_kind` (e.g. "appropriately qualified health practitioner" for HIDPA). |
| **Risk** | Entry in the risk register. | `category`, `rating_current`, `rating_target`. |
| **Control** | A mitigation (often *is* a Document or a practice). | `control_kind`. |
| **Evidence** | An artefact proving something happened (a completed form, a register extract, a training record). Immutable once frozen for audit (v0.3). | `evidence_kind`, `source → GENERATED_BY`, `frozen_at`. |
| **Audit** | A certification, verification, mid-term or internal audit event. | `audit_kind`, `auditor`, `scope → ASSESSES`. |
| **Finding** | Conformity / minor NC / major NC / observation. | `severity`, `RAISED_IN → Audit`, `CONCERNS → node`. |
| **ImprovementAction** | Remediation; closes the loop via `ADDRESSES`. | `due_date`, `closed_at`. |

**Deliberately excluded for now:** Participant as a first-class node. Participant-linked
records (support plans, decision-support records) are Documents/Evidence keyed to an
external participant identifier held in the provider's CRM. Reason: keeping NDIS
participant PII out of the graph reduces the privacy blast radius and keeps the Privacy
Act / APP surface in one system. This is a design opinion with a real trade-off
(per-participant traversals get harder); revisit if per-participant gap views become a
core feature.

---

## 5. How node attributes render into documents

The Compliance Header (architecture doc §4) is a deterministic projection:

| Header field | Comes from |
|---|---|
| Document ID / Title / Type / Version / Status | Document node attributes |
| Effective from / Review due | `effective_from`, `effective_from + review_cycle_months` |
| Owner / Approved by | `OWNED_BY` edge; approval event |
| "This document implements" | `IMPLEMENTS → Standard` edges (ID + title) |
| "Set out in / made under" | Follow `Standard PART_OF Module PART_OF Framework PUBLISHED_IN Instrument MADE_UNDER Act` |
| "Put into practice by" | Incoming `OPERATIONALISES` |
| "Carried out using / recorded in" | `USES`, `RECORDS_TO` |
| "Other laws referenced" | `RELATES_TO(note: statutory reference)` — pending `REFERENCES` |
| Easy Read available | `easy_read_available` |

Round-trip rule: everything in a header must be reconstructible from the graph, and every
graph edge touching a document must be visible in its header or its Related Documents
table. If the two can disagree, one of them is wrong — the graph wins and the document
regenerates.

---

## 6. Proposed edge-taxonomy extensions (for v0.4 of the edge doc)

Two patterns kept landing in `RELATES_TO` while building the 121-document suite, which is
the "modelling smell" signal v0.3 says to watch for:

1. **`REFERENCES`** — Document → Instrument/Provision. A statutory citation that is
   neither `IMPLEMENTS` (wrong domain: that targets Standards) nor `MADE_UNDER`. Example:
   the Information Management Policy citing the Privacy Act 1988. Currently 100+
   `RELATES_TO` edges carry this note in the register — easily the biggest smell.
2. **`AMENDS`** — Instrument → Instrument. The 2026 Amendment Rules amend the 2018 Rules;
   the Integrity and Safeguarding Act 2026 amends the NDIS Act. `SUPERSEDES` is wrong
   (nothing is replaced; the target keeps existing as an amended compilation). Amendments
   are also the trigger events for legislative-change fan-out, so they deserve first-class
   typing.

Both are proposals, not decisions — v0.3's governance says extensions need a rationale
and a review, and this is the rationale.

---

## 7. Epistemic status

- **Established practice:** bitemporal valid/transaction time pairing; shared-vs-tenant
  multi-tenancy split; role-based accountability.
- **Verified (Jul 2026):** module list including the SIL module and Verification module
  contents; the 2026 instruments named in the register's Legislation sheet.
- **My design / recommendation:** the specific node set, attribute lists, the
  Participant-exclusion decision, ID scheme, and the §6 extension proposals.
- **Not yet done:** validation against a real provider's documents and a real audit
  report — same caveat as the edge taxonomy, and the same prediction: the first thing to
  bend will be `Document.doc_type` granularity (plans and agreements may deserve richer
  typing once real content exists).
