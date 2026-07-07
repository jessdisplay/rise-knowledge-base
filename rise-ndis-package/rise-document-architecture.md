# Rise Document Architecture

**Version 0.1 — 2026-07-05.** How a provider's documents make the compliance graph
visible on the page. Read with: `rise-node-taxonomy.md` v0.1, `rise-relationship-taxonomy.md`
v0.3, and the master workbook `rise-document-register.xlsx` (which is itself document
REG-GOV-03 in the suite).

**Audiences, in priority order:** (1) the support worker or manager who has to *use* the
document, (2) the auditor who has to *trace* it, (3) the participant who has a right to
*understand* it. Every design choice below is tested against those three.

---

## 1. Where each document type sits

```
  LAW            NDIS Act 2013 ── amended by Integrity & Safeguarding Act 2026
                      │  MADE_UNDER
  RULES          Provider Registration & Practice Standards Rules 2018
                 (+ 2026 Amendment Rules) · Incident Rules · Complaints Rules ·
                 Restrictive Practices Rules · Worker Screening Rules · Code of Conduct
                      │  PUBLISHED_IN
  STANDARDS      NDIS Practice Standards
                 Core │ Verification │ M1 HIDPA │ M2/2A │ M3 │ M4 │ M5 SDA │ SIL (new)
                      │  quality indicators guide the audit of each standard
                      ▲  IMPLEMENTS
  ┌───────────────────┴────────────────────────────────────────────────┐
  │ POLICY        why we do it, and the commitments we make            │
  │   ▲ OPERATIONALISES                                                │
  │ PROCEDURE     how, who, when — step by step                        │
  │   ▲ OPERATIONALISES              │ USES                            │
  │ WORK          the frontline      ▼                                 │
  │ INSTRUCTION   one-task version   FORM  what we capture, each time  │
  │                                    │ RECORDS_TO                    │
  │                                  REGISTER  the running log         │
  └────────────────────────────────────┬───────────────────────────────┘
                                       │ GENERATED_BY / EVIDENCES
  EVIDENCE       completed forms, register extracts, training records
                      │ CITES / CONCERNS
  AUDIT          findings → improvement actions → closed loop
```

The chain is the *most common* path, not an enforced one (v0.3 §5). A register can
satisfy a standard with no form in between; gap rules decide per module whether that is
acceptable. Plans, agreements and handbooks are typed documents that slot in at the
procedure/form level.

**One page, on the wall.** This diagram, plus the plain-English edge glossary from the
register's READ ME sheet, is the whole mental model a new staff member needs.

---

## 2. Document identity

`TYPE-DOMAIN-NN` — e.g. `POL-INC-01`, `PRO-INC-02`, `FRM-INC-01`, `REG-INC-01`.

- **TYPE:** POL, PRO, WIN, FRM, REG, PLN, AGR, STA (handbook/statement).
- **DOMAIN:** a stable three-letter cluster code (GOV, RSK, QMS, INF, FBK, INC, HRM,
  COS, EDM, RGT, SGD, SUP, ENV, MNY, MED, MTM, WST, HID, BSP, ECS, SCO, SDA, SIL, WHS).
  Full list = the Cluster column of the register.
- **NN:** sequence within TYPE-DOMAIN. IDs are never reused; a retired ID stays retired.

Versioning lives in metadata, not the ID: `POL-INC-01` v1.0 → v2.0 with a `SUPERSEDES`
edge between versions. File names carry both: `POL-INC-01_v1.0_Incident-Management-Policy`.

---

## 3. Reading order inside every document

Same skeleton in every template, in this order, so anyone can navigate any document:

1. **Title + one-sentence purpose** — plain English, states who the document is for.
2. **Document Control table** — ID, version, status, owner, approver, dates.
3. **Compliance Links table** — the graph, rendered (§4).
4. **Body** — type-specific (§5).
5. **Related documents** — every remaining edge, with its type.
6. **Definitions** — only terms actually used; defined once, then used consistently.
7. **Review triggers + version history.**

---

## 4. The Compliance Header (the design centrepiece)

Two small tables at the top of every document. The second one *is* the graph: each row
is literally one typed edge, shown with its plain-English gloss so it reads naturally
while staying machine-extractable.

**Document Control**

| Field | Entry |
|---|---|
| Document ID / Type | POL-INC-01 · Policy |
| Version / Status | 1.0 · Approved |
| Owner (role) / Approved by | Quality Manager / CEO |
| Effective from / Review due | 01 Aug 2026 / 01 Aug 2028, or earlier on any legislative change |
| Easy Read version | Not required (internal document) — participant-facing summary in STA-RGT-01 |

**Compliance Links** *(worked example: POL-INC-01)*

| Link type | Plain English | Linked to |
|---|---|---|
| IMPLEMENTS | This policy exists to meet | CORE-2.6 Incident management; VER-2 Incident management |
| SET OUT IN → MADE UNDER | Those standards are set out in / made under | NDIS (Provider Registration and Practice Standards) Rules 2018 → NDIS Act 2013 |
| REFERENCES* | Other law this policy must follow | NDIS (Incident Management and Reportable Incidents) Rules 2018 |
| OPERATIONALISED BY | Put into day-to-day practice by | PRO-INC-01 Incident Management Procedure; PRO-INC-02 Reportable Incidents Notification Procedure |
| RECORDS END UP IN | Incidents are logged in | REG-INC-01 Incident Register |
| EVIDENCED BY | Proof it works | Completed FRM-INC-01 forms; REG-INC-01 extracts; training records in REG-HRM-02 |

*\*Rendered as `RELATES_TO (statutory reference)` until the proposed `REFERENCES` (v0.4 candidate)
edge type is adopted — see node taxonomy §6.*

**Round-trip rule:** header ↔ graph must agree; the graph is authoritative and headers
regenerate from it. A header edited by hand without a graph update is a defect.

---

## 5. What goes in each body (summary — details in the templates)

| Type | Answers | Body spine |
|---|---|---|
| Policy | *Why, and what we commit to* | Purpose · Scope · Policy statements (numbered, one idea each) · Responsibilities by role |
| Procedure | *How, who, when* | Trigger · Step table (Step / Who / What / Record created) · Escalation · Timeframes with statutory deadlines flagged |
| Work instruction | *Exactly what I do right now* | One task, one page, numbered actions, "stop and escalate if…" box |
| Form | *What we capture, every time* | Fields grouped by section · privacy notice · where the completed form goes |
| Register | *The running log* | Column specification · who maintains it · review rhythm · retention |

Statutory timeframes are always shown **with their source** in the step where they bite
(e.g. reportable-incident notification windows cite the Incident Rules provision), so an
auditor never has to ask "where does that number come from" — and neither does a new
coordinator at 2 a.m.

---

## 6. The three traceability views

1. **Micro — any single document.** The Compliance Header answers "why does this exist
   and what depends on it" in one glance. This is the auditor's opening move: pick a
   standard, ask for the documents, check currency and fit.
2. **Suite — the master register (the workbook).** Filter the Documents sheet by a
   standard ID and you have the certification-audit sampling map: every document claiming
   to implement that standard, its status, owner, review date, and its typed links both
   directions. Filter by `Applies to = Verification` and you have the verification-audit
   pack. Filter `Priority = P1` and you have the build order.
3. **Matrix — requirement → documents → evidence.** Generated from the graph per audit:
   for each in-scope standard (per RegistrationScope), the implementing documents, the
   registers/evidence that prove operation, and any open findings. This is the artefact
   you hand the approved quality auditor on day one; it is also exactly the gap-detection
   query ("standards in scope with no surviving IMPLEMENTS edge").
```
Standard        Documents (IMPLEMENTS)          Operating proof            Gaps/Findings
CORE-2.6        POL-INC-01, PRO-INC-01/02,      REG-INC-01 extract,        —
Incident mgmt   WIN-INC-01, FRM-INC-01          notification records
SIL-3           POL-SIL-03, PRO-SIL-03          house training records     evidence not yet
Practice gov.                                    (REG-HRM-02 filtered)      frozen — new module
```

---

## 7. Accessibility standard ("usable for anyone")

Rules, in force for every document in the suite:

1. **Plain English first.** Short sentences (target ≤ 20 words), active voice, "we/you"
   address. Aim around a Year 8–9 reading level for policies and procedures; work
   instructions lower. (Reading-level targets are my recommendation; the regulator does
   not mandate one.)
2. **One idea per policy statement**, numbered, so statements can be cited ("Policy
   POL-SGD-01, statement 4").
3. **Jargon quarantine.** Legal citations live in the Compliance Links table and
   reference columns — the body text stays readable. Terms defined once, in Definitions.
4. **Easy Read companions** for participant-facing documents (marked in the register:
   handbook, complaints form, service agreements, decision-support records, SIL tenancy
   material, and others). Precedent: the Commission itself publishes Easy Read versions
   of the SIL Practice Standards material, so auditors already recognise the pattern.
5. **Participant statements.** The new SIL standards pair a provider statement with a
   participant statement ("I am supported to make decisions about my home…"). The policy
   template carries an optional "What this means for participants" box adopting that
   voice — my recommendation, aligned with the reform's direction rather than required
   by the current Core Module.
6. **Never a wall of text.** Tables for steps, boxes for escalation, white space.

---

## 8. Review, change and fan-out

- Review cycles per the register (policies 2-yearly, operational documents annually —
  recommended defaults, not regulatory numbers), **plus** event-driven review on: any
  amendment to a linked instrument, a major audit finding, a serious incident, or a
  change in registration scope.
- **Legislative-change fan-out** is a graph traversal: amendment lands on an Instrument
  node → follow `PUBLISHED_IN`/`REFERENCES` edges inward → every affected document gets a
  review task. The 2026 Amendment Rules are the live example: they touch every document
  whose header cites the 2018 Rules, and they created the SIL cluster outright.
- Superseded versions are retained (SUPERSEDES chain) — auditors ask for "the policy as
  it stood when the incident happened", and bitemporal nodes make that answerable.

---

## 9. Design rationale and trade-offs (opinions, marked as such)

- **Typed-edge labels visible in documents** trades a little visual austerity for
  machine-readability and staff literacy in the model. Alternative considered: prose
  cross-references only — friendlier-looking, but they rot silently and can't be
  ingested. The gloss column is the compromise.
- **One register workbook** rather than per-cluster registers: single source of truth
  and trivially filterable; the cost is a big sheet, mitigated by filters and the
  Priority column.
- **Word + Markdown dual format:** Word for how providers and auditors actually work;
  Markdown as the canonical, diffable source the graph generates from. Risk: drift
  between the two — mitigated by treating Markdown as source and exporting, never
  editing the docx directly as master.

## 10. Epistemic status

Verified (Jul 2026): module set incl. SIL commencement and mandatory SIL/platform
registration; verification-module contents; the 2026 instruments named in the register.
Corroborated: certification vs verification audit pathways; auditor sampling behaviour.
My design: everything in §§2–9 not attributed to an instrument — including all review
cycles, the ID scheme, reading-level targets and the header layout.
