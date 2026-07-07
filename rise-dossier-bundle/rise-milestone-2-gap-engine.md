# Rise — Milestone 2 brief: indicator ingestion and the gap engine

**Status:** specification, follows Milestone 1 (`rise-claude-code-brief.md`). Same
honesty rules, same stack defaults, same reporting-back requirement. Where this
brief and the taxonomy (v0.3) conflict, the taxonomy wins.

## Mission

Turn the several hundred individual quality indicators into addressable, typed,
applicability-gated nodes, and implement gap analysis over them. Milestone 1 proved
the schema; this milestone makes it useful.

## Step 1 — parse indicators into addressed nodes (mechanical, deterministic)

- Ingest the **current compilations** per `rise-source-manifest.md` (never the chat
  transcript). The Guidelines number indicators as items within each section, so
  every indicator has a real address: e.g. "s 69, item 1".
- Emit one node per numbered indicator item, `PART_OF` its section, section
  `PART_OF` its standard's indicator set, `PUBLISHED_IN` the Guidelines.
- This step also resolves the indicator count, which has been deliberately left
  unstated everywhere (estimate from sampled sections: low hundreds; 3–12 items per
  section). Report the exact count.
- Do not paraphrase, renumber, or normalise wording during parsing.

## Step 2 — demand-type classification (AI-suggested, human-verified)

Tag each indicator with one or more of the seven demand types (analysis-derived,
not a legal category — see epistemic note below):

1. policy/documented process · 2. plain-language communication · 3. consent ·
4. training with records · 5. plan developed-and-reviewed · 6. records/registers of
what happened · 7. compliance with a named companion rulebook.

All tags land as `assertion_source=ai`, `verification_status=needs_review`. A human
verifies. The demand type determines what counts as satisfying the indicator, and
therefore what "gap" means for it.

## Step 3 — applicability gates

- **Module level (legislated):** ingest the Rules **s 20(3) table** — 36 classes of
  supports mapped to applicable schedules and assessment method — as *data, not
  code*. Include the s 20(4)–(5) sole-trader/partnership early-childhood variation
  and the s 7(2)/20(1)(b) regulated-restrictive-practice trigger for Module 2A.
- **Indicator level:** capture conditional phrases ("where applicable", "where a
  participant has specific needs") as applicability predicates against a provider
  profile (registration classes, services delivered, participant-need flags).
- Provider profile schema is part of this milestone; keep it minimal but real.

## Step 4 — document mapping

- AI proposes `IMPLEMENTS` edges between provider documents and indicators from
  their texts; humans verify. Expect a sparse matrix (each document plausibly
  serves a handful of indicators) — hundreds of verified edges per provider, not
  thousands (inference, to be confirmed by the pilot).
- Never auto-verify. Every edge keeps its assertion source.

## Gap states (four, plus a by-product)

Evaluate per indicator, per provider, in this order:

1. **Not applicable** — the gate says the indicator doesn't apply. Recorded, not hidden.
2. **Unknown** — the gate cannot be evaluated because the provider profile is
   incomplete. **Must be reported as its own category, never silently folded into
   not-applicable.** Hiding unknowns is how gap reports lie.
3. **Documentation gap** — applicable, zero verified inbound `IMPLEMENTS`
   (the Stage 1 audit failure).
4. **Proof gap** — documented but zero recent inbound `EVIDENCES`
   (the Stage 2 "paper compliance" failure).
5. Else **covered — for now** (recheck on change).

**By-product report:** orphan documents — anything mapping to nothing is wasted
effort or a mis-scoped suite. Also report `RELATES_TO` usage and per-document
edge-count outliers (over-mapping smell).

## Acceptance criteria (tests required)

1. Indicator parser is deterministic: same input → identical node set; exact count reported.
2. s 20(3) lives in data; changing a table row changes gate outcomes without code changes.
3. A provider with an incomplete profile yields **unknown**, not not-applicable.
4. Gate ordering enforced: applicability is evaluated before any gap check.
5. Per-demand-type gap views return planted fixtures and nothing else.
6. Orphan-document report returns the planted orphan.
7. All AI-created edges are `needs_review` until a human action verifies them.

## Honest limits (must survive into UI copy)

- **Coverage is not adequacy.** The engine detects absence — no document, no
  evidence. It cannot detect a bad policy or weak evidence. A fully green indicator
  can still fail a human auditor on quality. Never market otherwise.
- The seven demand types are analysis of the indicator corpus, not categories the
  law declares. The classification of each indicator is judgment work with a
  verification loop, not fact.
- Leave taxonomy §9 items 2–4 as `TODO(taxonomy-9.x)`; do not resolve them here.

## Epistemic status

- **Verified:** indicator item-numbering; the s 20(3) table and its variations; the
  two-stage audit structure this engine mirrors (Commission and instrument sources,
  July 2026).
- **Analysis:** the seven demand types; the four-state gap model; the sparse-matrix
  effort estimate.
- **Unknown until built:** the exact indicator count; real mapping density; how the
  2026 SIL additions change the totals.
