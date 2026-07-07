# Rise Authoring Best Practice — writing and formatting policies, procedures and forms
**Version 0.1 — 7 July 2026** · Produced this session from web research (all sources accessed 7 Jul 2026) plus the in-hand collection. Companion to the five `TPL-*` templates and `rise-document-architecture.md`; this document grounds them in external standards, records one correction, and proposes concrete deltas.

Labels: **[V-now]** verified this session against the cited source · **[V-prior]** verified in a prior Rise session, reproduced from in-hand documents · **[C]** corroborated across multiple secondary sources · **[D]** design opinion / recommendation · **[T]** negative finding (searched for, not found).

---

## 0. Premise check — what already exists, and what this adds

The collection is **not** missing templates. In-hand already:

| Artefact | Already covers |
|---|---|
| `TPL-POL / PRO / WIN / FRM / REG` | Full structural skeletons with worked examples: Document Control table, Compliance Links table, numbered ≤20-word policy statements in "We will" voice, form fields that must "earn their place", privacy notice on forms. |
| `rise-document-architecture.md` §3, §7 | Fixed reading order for every document; accessibility rules (plain English, jargon quarantine, Easy Read companions, "never a wall of text"). |
| Auditor guide §6 (evidence hygiene) + Level 5 | What the 2022 real audit report shows auditors reward in the artefacts themselves. |

What was genuinely missing — and what this document adds — is the **externally verified layer**: which authoritative standards those house rules align with, where they diverge, the production standard for Easy Read (flagged as required-but-undrafted across the collection), and form-design and document-control conventions from outside the NDIS bubble.

**One correction found (§3):** the architecture spec recommends a Year 8–9 reading level; Australian Government guidance targets **Year 7** for content meant for general audiences.

---

## 1. What auditors reward in the document itself **[V-prior]**

From the real 2022 certification report and the auditor guide, both in-hand:

- Every document the auditor cited in an EVIDENCE block carried a **version number and a date** (e.g. "Client Charter (V7)"). The implicit test: current, approved, consistent with practice.
- Auditors assemble a **bundle** per indicator and triangulate document → interview → observation. A beautifully formatted policy fails if workers can't articulate it.
- Proportionality recurs: everything scaled to the provider's "size, scale, scope and complexity".
- **[T]** No source was found this session indicating the NDIS Commission prescribes document *formatting* (fonts, layout, templates). Formatting expectations are indirect: they arrive through evidence quality, accessibility obligations, and whether documents work for the people using them. Do not cite this guide as "the Commission requires X format" — it does not appear to.

---

## 2. Plain language — the verified rules **[V-now]**

Source: Australian Government Style Manual (stylemanual.gov.au), the standard for government writing and the reference every state accessibility toolkit points to.

1. **Target reading level: Australian Year 7** ("reading level 2") for content aimed at general audiences. The Style Manual ties this to WCAG success criterion 3.1.5 (AAA), which defines a lower-secondary-education reading level (roughly ages 12–14). The literacy rationale: educational attainment doesn't equal reading level — the Style Manual notes around 30% of Australians hold a diploma or higher but only about 1.2% read at that level, and higher-literacy readers *prefer* plain content because they are time-poor.
2. **Short sentences, active voice, personal pronouns** ("we", "you"). Active voice makes it clear who must do what — directly relevant to procedures.
3. **Positive instructions** over negative ones; people respond to "do this" better than "if you don't…".
4. **Front-load everything.** Most users scan. Key message first; topic sentence starts each paragraph; headings ≤70 characters with the keywords in the first 2–3 words.
5. **Jargon quarantine** (the in-hand spec's term; the Style Manual's substance): avoid or explain unusual terms, expand acronyms on first use, glossary for term-heavy documents. Reserve shortened forms for the most frequent terms only.
6. **Readability testing:** check drafts with a tool (Word's built-in Flesch-Kincaid, Hemingway, Readable) and **remove proper nouns before scoring** so names don't distort the result (SA Government Online Accessibility Toolkit). The Style Manual cautions against over-editing to chase a score — the basics matter more than the number. **[C]**

**The correction:** architecture spec §7 recommends Year 8–9 for policies/procedures (and honestly flags this as its own unverified recommendation). Against the Style Manual, the defensible split is: **participant-facing documents (handbooks, charters, agreements, forms) target Year 7**; internal policies/procedures at Year 8–9 remain a reasonable house choice, but note it sits above the government benchmark. **[V-now for the benchmark; D for the split]**

Literacy context, corroborated: PIAAC data — about 44% of Australian adults read at or below Year-10 level — appears in the in-hand zero-knowledge training model and independently on Queensland Government accessibility guidance. **[C]** This is the structural reason plain language is a compliance capability, not a style preference.

---

## 3. Document control — industry consensus, mapped to what Rise already does

Source basis: ISO 9001:2015 clause 7.5 ("documented information"), read via multiple consistent secondary sources this session. **The standard's text itself was not fetched (paywalled); treat the following as industry consensus [C], not verified clause text.** Certification audits are explicitly anchored in ISO/IEC 17065 [V-prior], and AQA expectations visibly rhyme with these conventions.

| Convention [C] | Rise status |
|---|---|
| Unique ID, title, version, owner, dates on every controlled document | ✓ Document Control table in every template |
| Formal review + approval **before use**; approver recorded | ✓ table rows exist; approval workflow itself is a build item |
| Version history / change trail — who, what, when, why | ✓ "version history" section in reading order; SUPERSEDES edges are the graph-native version |
| **Obsolete versions withdrawn from circulation** but retained, clearly marked | Partially — retention is designed (bitemporal); an explicit "mark/withdraw superseded copies, especially printed ones" rule is a gap → delta §6.2 |
| Control of **external documents** (legislation, standards): assigned owner monitors updates | ✓ this is exactly the legislative-change fan-out design |
| Documentation scaled to organisation size/complexity | ✓ mirrors the Standards' recurring proportionality phrase |

The common failure modes named across sources — "Final_v4" filename versioning, outdated printed copies on the floor, two versions in circulation — are precisely what the register-driven model prevents. Worth stating in the QMS procedure so the *discipline* survives outside the platform.

---

## 4. Forms — verified guidance **[V-now]**

Source: Style Manual "Forms" content-type page (written for digital, most of it applies to print).

1. **Work out if the form is even needed**, then build a **question protocol**: for every field, record why it's asked, who uses the answer, and what happens downstream. The protocol itself becomes a record. This independently confirms TPL-FRM's existing rule that every field must feed the register or a notification — upgrade that rule's standing from house opinion to corroborated. **[C]**
2. Completed forms are **records/evidence** and need managed retention (for government, under the Archives Act; for a provider, per the records-management procedure and privacy notice — both already in-hand).
3. For future **digital** forms in the Rise platform: start prototyping with **one thing per page**, add a **"check your answers"** summary before submission, and only use progress indicators where the form is long and linear.
4. General form-usability consensus **[C]** (multiple design sources): single-column layouts produce fewer errors; visible labels (never placeholder-only); mark fields "(optional)" in words rather than asterisk conventions; group related fields; error messages say what went wrong and how to fix it; sans-serif at readable sizes.

---

## 5. Easy Read — the production standard the collection was missing

The register flags Easy Read companions as required for participant-facing documents but none are drafted. This section is the how.

**What it is [V-now]:** a distinct format — not just simpler plain language — pairing short sentences with images that carry meaning, designed for people with intellectual disability, low literacy, or limited English. Users are drawn to the image first, then the adjacent text. Treat the Easy Read version as a **summary of the source document**, published **alongside** it (same place, same time), not a replacement.

**Production rules** (Style Manual Easy Read page; Inclusion Australia's commissioning guide; NSW/Qld government guidance — consistent across all four) **[V-now/C]:**
- Layout: generous white space, wide margins, line spacing ≥1.5, sans-serif font ≥14pt, high contrast, minimal decoration. Avoid tables, graphs and columns.
- One idea per sentence; explain each new concept; define terms in place ("The NDIS is…").
- Images: one consistent style per document — photographs **or** illustrations, never mixed; age- and culturally-appropriate; every image needs alt text in digital versions.
- Length: keep it short — Inclusion Australia advises aiming for ~5 pages (add a contents page beyond that); NSW guidance treats ~20 pages as the ceiling. Page numbers at body-text size once past 4 pages.
- Publish as an accessible web page plus accessible PDF/Word, downloadable from the same location as the source document.
- **Process is part of the standard:** involve Easy Read expertise, and test with people who have intellectual disability — a multi-stage review (self → peer → usability test → final QA). A document is not Easy Read because its author says so.

**Status in law [C, academic]:** a 2026 peer-reviewed review notes the UK legally mandates accessible information in health/social care; Australia (a CRPD signatory) has government-proposed guidelines but no equivalent legal mandate. In the NDIS context the pull is practical and reputational rather than statutory-formatting: the Commission itself publishes Easy Read versions of its SIL material — the "new rules for good and safe support" factsheet, Easy Read reflective questions, and an Easy Read glossary **[V-now: ndiscommission.gov.au SIL page]** — which confirms the in-hand spec's precedent claim, and accessible formats for household agreements are already discussed as audit-relevant in SIL commentary **[T-tier lead only]**.

**Commissioning note [V-now, Inclusion Australia]:** budget time and money; ask providers for examples of prior work; a document labelled Easy Read is not necessarily easy to read. Inclusion Australia is also the body the Commission co-designed the SIL standards with — using their guide keeps Rise aligned with the regulator's own collaborators.

---

## 6. Recommended deltas — concrete, numbered **[D]**

1. **Reading-level rule (amends spec §7.1):** participant-facing documents target Year 7; internal documents may sit at Year 8–9 with the divergence noted. Add a readability-test step (tool + strip proper nouns) to the document-approval checklist in PRO-QMS-02.
2. **Superseded-copy rule (adds to PRO-QMS-02 / TPL headers):** printed or exported copies carry status ("DRAFT / APPROVED / SUPERSEDED — see register for current"); superseded versions withdrawn from circulation points, retained in the archive. The graph already does this; the paper world needs the sentence.
3. **Question-protocol column (amends TPL-FRM):** the field table gains "why we ask / who uses it" — making the existing earn-its-place rule auditable field-by-field.
4. **Easy Read production appendix (new TPL or appendix to TPL-FRM/handbook docs):** encode §5's layout numbers and the mandatory user-testing step; first candidates per the register: Participant Handbook, complaints form, service agreement.
5. **Heading + topic-sentence rule (amends all TPL body guidance):** headings ≤70 characters, keywords first; each section opens with its point.
6. **Digital-form patterns (developer handoff note):** one-thing-per-page and check-your-answers as default patterns when suite forms become platform forms.

None of these change the compliance-graph structure; they are authoring-layer refinements.

---

## 7. Sources (tiered, all accessed 7 Jul 2026)

**Tier 1 — government standards and the regulator**
- Australian Government Style Manual: "Plain language and word choice"; "Literacy and access"; "Quick guide: plain language"; "Easy Read"; "Forms" — stylemanual.gov.au. The load-bearing source for §§2, 4, 5.
- NDIS Commission: SIL Practice Standards page (Easy Read factsheet, reflective questions, glossary; Evidence Guide for Providers and Workers) — ndiscommission.gov.au.
- Qld Government "Develop Easy Read content" (PIAAC figures); Digital NSW Easy Read and plain-language pages; SA Online Accessibility Toolkit (readability testing method).

**Tier 2 — peak body and academic**
- Inclusion Australia, *A Guide to Commissioning Easy Read Resources* (PDF) — production and commissioning specifics.
- *The evidence underlying guidelines for Easy Read…*, Journal of Intellectual & Developmental Disability (Taylor & Francis, 2026) — evidence base and legal-status comparison.

**Tier 3 — industry consensus (used only where consistent across several)**
- ISO 9001:2015 cl 7.5 secondary explainers (QT9, Cognidox, DocuWare, others) — document-control conventions. *Standard text not fetched.*
- Form-design practice literature (Style Manual bibliography's own references; Adam Silver; Coyle) — §4.4 only.
- SIL compliance commentary (ndiscompliant.com.au) — lead-only corroboration that accessible formats surface at audit.

**In-hand anchors [V-prior]:** auditor guide (real 2022 report analysis; evidence hygiene), `rise-document-architecture.md`, the five templates, zero-knowledge training model (literacy framing).

## 8. Changelog
- v0.1 (2026-07-07): initial research and gap analysis; one correction (reading level), six deltas proposed, Easy Read production standard added.
