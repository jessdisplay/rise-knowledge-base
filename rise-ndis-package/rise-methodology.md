# Rise — Method & Logic, in Plain English

**v0.1 — 5 July 2026.** How this package was built and why you can trust it exactly as
far as it says you can — no further. Companion to `rise-sources.md` (the evidence) and
`rise-plain-english-guide.md` (the subject matter). Written to be challengeable: every
rule below is stated so you can catch me breaking it.

---

## 1. The question the method answers

Compliance work dies from one disease: **confident text nobody can trace.** A policy
cites "the Rules" without saying which clause; a consultant's summary gets copied as if
it were the law; an old requirement lingers after an amendment. The method here is the
cure applied consistently: every fact carries its evidence grade, every link carries
its type, and everything regenerates from one source so nothing can silently drift.

## 2. Five rules the whole build follows

1. **One source of truth.** All data lives in one script (`rise_build.py`). The
   spreadsheet, the JSON, and the dossier are generated from it — never hand-edited.
   If two outputs ever disagree, the generator is broken, not the truth.
2. **Typed links only.** Nothing "relates to" anything vaguely. Every connection has a
   named type with a defined meaning ("implements", "records to", "made under"), and
   the one deliberate escape hatch (`RELATES_TO`) legally requires a written reason —
   and is counted as a smell to be refactored.
3. **Every fact is stamped.** Four grades: **V** (verified against the Federal
   Register or the regulator's own pages, dated), **C** (corroborated — solid but not
   primary-checked), **T** (training knowledge — confirm before relying externally),
   **D** (draft source — the instrument exists but its final text isn't consolidated).
   A stamp is metadata, not decoration: the build carries it into every output.
4. **Primary beats secondary, always.** A law firm's excellent summary can *alert* and
   *corroborate*; only the instrument or the regulator can *verify*. When a
   consultant's module numbering conflicted with the instrument, the instrument won
   and the consultant's page was recorded as a cautionary example.
5. **Official wording beats friendly wording.** Where the Commission's booklet says
   "Feedback and complaints management" and the Rules' clause heading says "Complaints
   management and resolution", the register uses the clause heading — because
   citations are the spine, and the clause is what an auditor can pinpoint.

## 3. The verification ladder — how a fact climbs

Worked example, the mealtime management standard:

- **Start (T):** training knowledge said "added in 2021, Core module, clause unknown"
  → recorded honestly as `Sch 1, Pt 5 — inserted by 2021 amendments, clause TBC`.
- **Corroborated (C):** the Commission's published Practice Standards material
  confirmed the standard exists in the Core module.
- **Verified (V):** fetching the Rules' table of contents from the Federal Register
  showed the clause itself — **cl 26A** — so the citation was written in, the stamp
  flipped to V, and the access date recorded.

The ladder only climbs on evidence; it never climbs on repetition. Ten consultants
saying the same thing is still C. And it can climb *down*: if the July-scheduled
compilation moves clause numbers, every affected V reverts to T until re-checked —
that re-check list is exactly what the graph's legislative-change fan-out produces.

## 4. How the gaps were found (four sweeps)

1. **Instrument census.** Our instrument list was diffed against the Commission's own
   legislation index. Found: the Notice of Changes and Events Guidelines, the
   Behaviour Support Practitioner Application Guidelines, the Approved Quality
   Auditors Rules 2025. Also *deliberately excluded* after review (binding the
   Commissioner rather than providers): the Protection and Disclosure of Information
   Rules and the transitional instruments — exclusion decisions are recorded, not
   silent.
2. **Standards diff.** Every standard name and citation was diffed against the Rules'
   fetched table of contents. Found: title drift on eight standards, three unresolved
   clause numbers (resolved), and confirmation the M2/M2A near-duplication is faithful
   to the instrument, not an error.
3. **Obligation scan of new law.** The 2026 Amendment Act's provider-facing effects
   were listed and matched against the document suite. Two obligations had no home:
   whistleblower protection (→ new policy POL-GOV-03) and tightened change/event
   notifications (→ new procedure PRO-GOV-02).
4. **Logic audit.** Each assumption in the chain was written down and graded: module
   applicability derives from registration groups via the Commission's initial scope
   of audit (mechanism verified; the mapping table itself not yet imported); registers
   are the evidence auditors weigh most (practitioner consensus, not a rule); review
   cycles and priorities are design recommendations, not law.

## 5. Interpreting disagreement between sources

Recorded precedence, applied twice this build: (a) "passed 1 April" (Commission) vs
"Royal Assent 8 April" (portfolio) — not a conflict; both dates are real events and
both are recorded, because bills pass and *then* receive assent; (b) compilation date
vs "the standards apply from 1 July 2026" — also not a conflict; law can commence
before the merged text is published, which is precisely why the D stamp exists.

## 6. Standards this method deliberately aligns with

Established: bitemporal record-keeping (what was true, and when we believed it) and
role-based accountability. Verified in prior sessions: NIST's OLIR crosswalk model
(the source of our mapping-strength dimensions), NIST OSCAL, W3C SKOS. Verified today:
**Akoma Ntoso / OASIS LegalDocML** — the open standard for machine-readable
legislation (OASIS Standard since 2018, revision due for approval late July 2026) —
the recommended structure when full legislative text is imported; and the **UK
legislation.gov.uk open API** as the benchmark for register integration. Emerging
practice, my interpretation: treating verification status as first-class provenance
on every node and edge — the same instinct as the W3C PROV family, applied to
compliance data.

## 7. What this method cannot do

It cannot make anything legal advice. It cannot verify what isn't published (SIL's
consolidated text). It cannot turn a static snapshot into a live feed — the honest
version of "live" today is: outbound links to authorised sources plus a regeneration
script plus a watch list; the automated version awaits confirmation of programmatic
FRL access (see the source register's negative findings). And it cannot substitute
for a professional's judgement about how a standard applies to one provider's facts.

## 8. Reproduce or challenge it

Run `python3 rise_build.py` then `python3 rise_dossier.py`: the workbook, JSON and
dossier rebuild from scratch, and the build refuses to complete if any link dangles.
To challenge a fact: find its stamp, open `rise-sources.md` to see what stands behind
it, and check the primary source — the package is designed to lose that argument
gracefully whenever the instrument says otherwise.
