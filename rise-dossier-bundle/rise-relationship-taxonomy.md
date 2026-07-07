# Rise Relationship Taxonomy — v0.3 (research-validated draft)

Defines the controlled vocabulary of relationship (edge) types for the Rise compliance
knowledge graph, the metadata every edge carries, and the rules for extending the
vocabulary. All claims previously flagged unverified have now been checked against
primary sources; remaining unknowns are listed in §10.

## Changelog

- **v0.3 (2026-07-05):** OLIR specification verified from the primary source (NIST
  IR 8278Ar1): `rationale` enum locked to syntactic/semantic/functional;
  `strength_score` **corrected** from "1–9" to the full 0–10 scale with fixed
  endpoint values and an N/A case. §8.1 expanded with patent-family findings: the
  UCF schema family is US + PCT only with no Australian entry, continuations active
  into 2024, litigation confirmed; adjacent IBM patents flagged. §9.2 gains OLIR's
  lowest-abstraction guidance as supporting practice.
- **v0.2 (2026-07-05):** §9.1 resolved — NDIS Practice Standards housing verified.
  Added `PUBLISHED_IN` (25th type); narrowed `INTERPRETS`. Extended `MAPS_TO` with
  `rationale` and `strength_score`. Added reviewed non-mappings recommendation,
  OSCAL Mapping model citation, UCF patent risk note. Rewrote §9–10.
- **v0.1:** initial draft; two claims flagged unverified.

---

## 1. What this replaces

The vision document's single list — *Exact Match / Related / Partial Match / Inferred /
Needs Review* — conflates three independent dimensions. This taxonomy separates them:

| Dimension | Question it answers | Where it lives |
|---|---|---|
| **Semantic type** | What *kind* of link is this? | `type` (§4) |
| **Assertion source** | Who or what claimed it? | `assertion_source` (§3) |
| **Verification status** | Has a human confirmed it? | `verification_status` (§3) |

Mapping of the old values: *Exact Match* → `MAPS_TO strength=equal` (or any verified
edge) · *Partial Match* → `MAPS_TO strength=subset|superset|intersects` · *Related* →
`CITES` or `RELATES_TO` · *Inferred* → `assertion_source=ai|rule` · *Needs Review* →
`verification_status=needs_review`.

---

## 2. Design principles

1. **Edges are first-class objects** — own identity, metadata, history. Never bare
   foreign keys.
2. **Type ≠ confidence.** Never encode certainty in a type name
   (`IMPLEMENTS_PARTIALLY` is an anti-pattern).
3. **Small, governed vocabulary.** 25 types below. New types must clear the bar in §8.
4. **One stored direction, two display labels.** Every type has a canonical direction
   and a named inverse; store once, render both ways.
5. **Direction convention:** edges point *from the dependent artefact toward its source
   of authority or subject*. Outbound traversal answers "why does this exist?";
   inbound answers "what depends on this?".
6. **Everything effective-dated.** Edges carry real-world validity dates *and* a
   record-keeping timestamp (bitemporal), so "compliance state as at 30 June 2025"
   is a query and audit snapshots are reconstructable. Adopt OSCAL's change
   discipline (verified NIST practice): any content change to a versioned node or
   document produces a new version identifier plus an updated last-modified stamp,
   so tools can detect change without diffing.

---

## 3. Universal edge properties

| Property | Values | Notes |
|---|---|---|
| `id` | UUID | Stable edge identity |
| `type` | one of §4 | Controlled vocabulary, validated |
| `from` / `to` | node refs | Validated against the type's domain/range |
| `valid_from` / `valid_to` | dates | Real-world effectivity |
| `recorded_at` / `recorded_by` | timestamp, actor | Audit-trail axis; edges are never silently mutated — supersede instead |
| `assertion_source` | `human` \| `import` \| `rule` \| `ai` | AI/rule edges default to `needs_review` |
| `verification_status` | `verified` \| `needs_review` \| `rejected` | Workflow state |
| `confidence` | 0.00–1.00 | AI-asserted edges only |
| `strength` | `equal` \| `subset` \| `superset` \| `intersects` \| `not_related` | `MAPS_TO` only (§6) |
| `rationale` | `syntactic` \| `semantic` \| `functional` | `MAPS_TO` only; how the judgement was made. Verified enum (NIST IR 8278Ar1 §3.2.5) |
| `strength_score` | integer 0–10, or N/A | `MAPS_TO` only. Fixed values: `equal`→10, `not_related`→0. Judged 1–9 for the three partial types (1–3 mostly dissimilar, 4–6 balanced, 7–9 mostly similar). N/A when elements sit at very different abstraction levels (non-lateral). Verified (IR 8278Ar1 §3.2.12) |
| `note` | text | **Required** for `RELATES_TO` |

Cardinality is many-to-many for every type at the storage level. *Expected*
cardinalities (e.g. "every Requirement should have ≥1 inbound `IMPLEMENTS`") are
gap-detection rules (§7), configured per framework — not schema constraints.

---

## 4. Core taxonomy (25 types)

### 4.1 Structure & authority — mostly shared/reference content

| Type | From → To | Inverse | Meaning |
|---|---|---|---|
| `PART_OF` | Section/Clause → Act/Rule; Indicator → Outcome → Module → Framework | `CONTAINS` | Hierarchical decomposition within one published source. Original numbering (1.1, 2.3, 4.7) is preserved as node attributes — never renumbered. |
| `MADE_UNDER` | Rules/Regulation/Instrument → Act or Rules | `EMPOWERS` | Delegated legislation or instrument created under an enabling provision. **Capture the actual enabling provision per instrument during ingestion — do not assume it.** |
| `AMENDS` | Amending instrument → Principal instrument | `AMENDED_BY` | Legislative change; the trigger for impact fan-out. Live examples (verified): the Provider Registration Amendment (Mandatory Registration and Other Matters) Rules 2026 amend the 2018 Rules; the Quality Indicators Amendment (Supported Independent Living) Guidelines 2026 amend the 2018 Guidelines. |
| `PUBLISHED_IN` | Framework/Module/Outcome/Requirement/Indicator → Act/Rules/Notifiable Instrument | `PUBLISHES` | The framework element's authoritative text lives in this instrument. Used when a framework **is** delegated legislation or official guidance — verified for both flagship frameworks (§9.1). Implies the node-type list needs a notifiable-instrument/guideline type distinct from legislative rules, since legal weight differs. |
| `INTERPRETS` | Requirement/Outcome → Section/Rule | `INTERPRETED_BY` | Reserved for frameworks **external** to the legislation they address (e.g. ISO 27001 controls relative to Privacy Act obligations). For frameworks housed in delegated legislation — the norm in Australian human-services regulation — use `PUBLISHED_IN` + `MADE_UNDER` instead. |
| `CITES` | any → any | `CITED_BY` | Explicit textual reference; no stronger claim implied. Also used for Finding → Evidence. |

### 4.2 Implementation — tenant content

| Type | From → To | Inverse | Meaning |
|---|---|---|---|
| `IMPLEMENTS` | Policy/Procedure/Control/Training → Requirement/Indicator/Section | `IMPLEMENTED_BY` | **The compliance claim**: "this artefact exists to satisfy that obligation." Core edge for gap detection and impact analysis. |
| `OPERATIONALISES` | Procedure → Policy; Work Instruction → Procedure | `OPERATIONALISED_BY` | Internal cascade from intent to method. |
| `USES` | Procedure/Work Instruction → Form/Asset/System | `USED_BY` | Tooling employed while executing. |
| `RECORDS_TO` | Form → Register | `CAPTURES` | Where completed form data lands. |

### 4.3 Evidence & assurance

| Type | From → To | Inverse | Meaning |
|---|---|---|---|
| `EVIDENCES` | Evidence → Requirement/Indicator/Control/Policy/Procedure | `EVIDENCED_BY` | **The assurance claim.** Frozen into immutable snapshots at audit time. |
| `GENERATED_BY` | Evidence → Register/Form/Procedure/System/Training | `GENERATES` | Provenance: where the evidence artefact came from. |
| `ASSESSES` | Audit → Framework/Module/Requirement | `ASSESSED_BY` | Audit scope. |
| `RAISED_IN` | Finding → Audit | `RAISED` | Origin of a finding. |
| `CONCERNS` | Finding/Risk → any governed object | `SUBJECT_OF` | What a finding or risk is *about*. |
| `ADDRESSES` | Improvement Action → Finding/Risk | `ADDRESSED_BY` | Remediation link; closes the loop. |

### 4.4 Risk & governance

| Type | From → To | Inverse | Meaning |
|---|---|---|---|
| `MITIGATES` | Control → Risk | `MITIGATED_BY` | Standard GRC semantics. |
| `OWNED_BY` | any governed object → Role | `OWNS` | Single accountable **role**; people are assigned to roles separately. |
| `PERFORMED_BY` | Procedure/Control/Training → Role | `PERFORMS` | Who executes. |
| `REQUIRES` | Role → Training/Qualification | `REQUIRED_BY` | Competency prerequisites. |

### 4.5 Versioning & cross-framework

| Type | From → To | Inverse | Meaning |
|---|---|---|---|
| `SUPERSEDES` | new version → prior version | `SUPERSEDED_BY` | Any versioned node: legislation compilations, framework editions, policy versions. The 2026 NDIS amendments make framework-edition versioning a day-one need (§9.5). |
| `MAPS_TO` | Requirement ↔ Requirement (cross-framework) | *symmetric* | Crosswalk edge with three dimensions: `strength`, `rationale`, `strength_score` (§6). Powers "comply once, satisfy many frameworks." |
| `CONFLICTS_WITH` | Policy ↔ Policy; Requirement ↔ Requirement | *symmetric* | Contradictory obligations or instructions; feeds a review queue. |
| `DUPLICATES` | same-type ↔ same-type | *symmetric* | Redundancy detection. |
| `RELATES_TO` | any ↔ any | *symmetric* | **Escape hatch.** Requires a `note`. Reported as a modelling smell to be refined. |

---

## 5. The vision document's chain, retyped

| Original arrow | Stored edge |
|---|---|
| Legislation → Act → Regulation → Rule | `PART_OF` hierarchy + `MADE_UNDER` |
| Rule → Section → Reference number | `PART_OF` (numbering preserved as attributes) |
| Legislation → Framework | `PUBLISHED_IN` + `MADE_UNDER` (NDIS, Aged Care) **or** `INTERPRETS` (external frameworks like ISO) |
| Framework → Module → Outcome → Requirement → Indicator | `PART_OF` |
| Requirement → Policy | Policy `IMPLEMENTS` Requirement |
| Policy → Procedure | Procedure `OPERATIONALISES` Policy |
| Procedure → Work Instruction | Work Instruction `OPERATIONALISES` Procedure |
| Procedure → Form | Procedure `USES` Form |
| Form → Register | Form `RECORDS_TO` Register |
| Register → Evidence | Evidence `GENERATED_BY` Register |
| Evidence → Audit Finding | Finding `CITES` Evidence |
| Audit Finding → Improvement Action | Action `ADDRESSES` Finding |

The chain is the *most common* path, not an enforced one. The schema permits skipping
layers; gap rules decide per framework whether that is acceptable.

---

## 6. Cross-framework mapping (`MAPS_TO`) — three dimensions (all now verified)

1. **`strength`** (set relation): `equal` / `subset` / `superset` / `intersects` /
   `not_related` — the five OLIR set-theory values, verified from IR 8278Ar1.
2. **`rationale`**: how the judgement was made. Verified enum with a strictness
   ordering: **syntactic** (word-for-word, no interpretation — strictest, typical
   when one document quotes another), **semantic** (some interpretation of the
   language), **functional** (outcomes compared rather than words — least strict).
   NIST guidance: select the strictest *provable* rationale. The same pair can map
   differently under different rationales, so allow multiple `MAPS_TO` edges per
   pair, differing by rationale.
3. **`strength_score`**: verified 0–10 integer scale. `equal` is always 10 and
   `not_related` is always 0 — so Rise should auto-fill those and prompt reviewers
   only for the three partial types (1–3 / 4–6 / 7–9 buckets). Score is N/A when the
   two elements sit at very different levels of abstraction (non-lateral pairs).

**Recording reviewed non-mappings (recommendation):** OLIR stores "not related to"
as an explicit assertion. Distinguishing "no one has reviewed this pair" from
"reviewed and confirmed unrelated" matters for gap detection and audit
defensibility. Default: `MAPS_TO strength=not_related` edges (review state lives in
the graph). Alternative: a separate review-log table (no negative edges, but a split
audit trail).

**Prior art (all verified):** W3C SKOS mapping vocabulary; NIST OLIR / IR 8477 set
theory relationship mapping; OSCAL's Mapping model for cross-framework control
relationships. **Possible future extension** (IR 8278Ar1): OLIR's third style,
"supportive relationship mapping" — supports / is supported by / identical /
equivalent / contrary — with relationship properties (example of, integral to,
precedes), relevant if Rise later maps controls to requirements rather than
requirements to requirements.

---

## 7. Gap detection = typed-edge queries (examples)

- **Unimplemented requirement:** Requirement with zero inbound `IMPLEMENTS` where
  `verification_status=verified` and the edge is valid today (per-framework config).
- **Unevidenced claim:** object with inbound `IMPLEMENTS` but zero inbound
  `EVIDENCES` within the last N months.
- **Orphan evidence:** Evidence node with zero outbound `EVIDENCES`.
- **Ownerless object:** governed object with zero `OWNED_BY`.
- **Stale AI suggestions:** `assertion_source=ai` and `needs_review` older than X days.
- **Unreviewed framework pairs:** requirements in overlapping frameworks with neither
  a `MAPS_TO` (any strength) nor a review-log entry.
- **Legislative impact fan-out:** from an amended Section, traverse inbound
  `PUBLISHED_IN`/`INTERPRETS` → inbound `IMPLEMENTS` → inbound `EVIDENCES`. The July
  2026 NDIS amendments are a ready-made test case.

---

## 8. Extension governance & anti-patterns

Adding a new type requires: a written definition, domain/range, an inverse label, at
least ~5 real instances that no existing type can express, and sign-off. Any type with
fewer than ~5 instances after NDIS ingestion is a merge candidate.

Anti-patterns: encoding confidence in type names; bespoke types per node-pair;
free-text relationship labels; using `RELATES_TO` to avoid modelling decisions.

### 8.1 IP risk note (updated in v0.3 — not legal advice)

**Verified from patent records:** Unified Compliance (Network Frontiers) holds
granted, active US patents on compliance-framework database schemas and mapping
methodology. The core "Compliance framework database schema" family (family ID
50115163, priority 2012) comprises **10 US applications and 1 PCT application
(WO2014071318A1) — no Australian national-phase entry appears in this family**.
Continuations remain active, with 2024-filed members granted (US12530383B2,
US12541539B2); the original grant's anticipated expiration is 2032. Litigation is
confirmed: a US case in the Oregon District Court (3:19-cv-00771) plus a family-level
litigation flag in Darts-ip data.

**Caveats:** (a) that is one family — UCF holds others not individually checked for
AU entries (e.g. automatic compliance tools US10769379B1 / US10824817B1 /
US11120227B1, structured dictionary US10606945B2, multi-word expressions
US11386270B2, retrieval interface US11928531B1); (b) Google Patents itself states
its legal-status data is an assumption, not a legal conclusion.

**Adjacent third-party IP (existence verified, relevance unknown):** IBM holds
US10922621B2 (facilitating mapping of control policies to regulatory documents) and
US11537602B2 (computer-implemented **live crosswalks in compliance mappings in
response to regulatory changes**) — the latter is conceptually close to Rise's
legislative-change fan-out feature.

**Technical observation, not a legal opinion:** the UCF schema family's claims centre
on extracting noun-verb pairs from citations and harmonising them into deduplicated
common controls (with SNED editorial statuses and checksum change-detection). Rise's
design as specified does not use that mechanism. Whether that distinction matters
legally is strictly a question for patent counsel.

**Action unchanged:** professional freedom-to-operate review plus an AusPat search
before locking the cross-framework mapping feature set or entering the US market.

---

## 9. Open questions — updated after research

1. **Resolved — legislation/framework split.** Verified: the NDIS Practice Standards
   and their outcomes are set out in the NDIS (Provider Registration and Practice
   Standards) Rules 2018 [F2018L00631] — Part 6 plus per-module Schedules — while the
   quality indicators live in a *separate notifiable instrument*, the NDIS (Quality
   Indicators for NDIS Practice Standards) Guidelines 2018 [F2018N00041]. Both were
   amended in 2026. Resolution: `PUBLISHED_IN` added; `INTERPRETS` narrowed.
   Follow-on: node-type list needs a notifiable-instrument type; capture each
   instrument's enabling provision at ingestion.
2. **Partially resolved — indicator granularity.** The Commission describes quality
   indicators as what auditors use to assess compliance, so indicators are plausibly
   valid `EVIDENCES` targets. Supporting practice from OLIR (verified): NIST directs
   mappers to work at the **lowest level of abstraction where practical**. Still
   open: whether tenant evidence links at indicator or outcome level in real NDIS
   audit practice — resolve from actual audit reports.
3. **Still open:** does `OPERATIONALISES` earn its keep vs collapsing into
   `IMPLEMENTS`? Revisit after ingesting one real provider's document set.
4. **Still open, with new data:** the strengthened Aged Care Quality Standards
   (commenced 1 Nov 2025 with the Aged Care Act 2024, housed in the Aged Care Rules
   2025) are structured as expectation statement → outcomes → actions. The generic
   element hierarchy holds across both flagship frameworks, but element *semantics*
   differ, so per-framework config must declare which level is the
   `IMPLEMENTS`/`EVIDENCES` target.
5. **New — framework-edition versioning under live reform.** Verified churn as of
   July 2026: SIL/platform mandatory registration commenced 1 July 2026; new SIL
   Practice Standards; a Commission-wide Practice Standards review; the Integrity and
   Safeguarding Act 2026 (passed ~31 March–1 April 2026; secondary sources differ by
   a day); expansion of mandatory registration to personal care, daily living
   supports, and closed settings from July 2027 with full rollout by end 2030.
   Decide *before build*: how a framework edition is snapshotted for audits that
   straddle an amendment.

---

## 10. Epistemic status

- **Verified against primary sources:** NDIS instrument housing and register IDs; the
  2026 NDIS amendment instruments and reform timeline; Aged Care Act 2024 +
  strengthened Standards commencement and housing; OLIR's five set-relation values,
  the syntactic/semantic/functional rationale enum, the 0–10 strength scale with
  fixed endpoints, and the lowest-abstraction mapping guidance (all IR 8278Ar1);
  IR 8477 rationale-dependence; OSCAL's seven models, Mapping model, and
  version-identifier discipline; UCF schema-family jurisdictions (US + PCT, no AU
  entry), active 2024 continuations, and Oregon litigation; existence of IBM's
  adjacent patents.
- **Established practice:** SKOS mapping vocabulary; control-mitigates-risk semantics.
- **My design/recommendation:** the 25-type list and names, `PUBLISHED_IN`, the
  direction convention, the escape-hatch policy, extension rules, recording reviewed
  non-mappings, and auto-filling derivable strength scores.
- **Unknown / lower confidence:** AU status of UCF's *other* patent families (needs
  AusPat/counsel); whether any claim reads on Rise's design (counsel only);
  completeness of Google Patents family data (it disclaims legal accuracy); §9
  items 2 (partially), 3, and 4.
- **Cautionary specimen:** secondary sources conflict on the penalty for delivering
  SIL unregistered (2 years / 120 penalty units vs a 5-year maximum). Neither was
  checked against the Act itself — a live demonstration of why Rise must anchor
  claims to primary instruments and why `assertion_source` exists.
