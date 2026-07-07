# CLAUDE.md — Rise NDIS compliance knowledge base

Orientation for Claude Code (or any agent) working in this repository. Read this before editing anything. This file is written by `_kb/build_kb.py`; edit it there.

## What this repository is

Three preserved session collections plus a generated navigation layer, assembled 7 July 2026:

- `rise-ndis-package/` — the document-and-graph package: 123-document suite, register workbook, seed graph JSON, templates, generator scripts, interactive dossier.
- `rise-audit-pack/` — the audit-research pack: auditor guide, indexed checklist, booklet reconciliation, coverage map v2, the Commission booklet PDF (Nov 2021).
- `rise-dossier-bundle/` — the 5–7 Jul design-session bundle: Claude Code briefs, source manifest, relationship taxonomy v0.3, plain-English map, navigator, visual atlas, training model, prototypes.
- `rise-authoring-research/` — 7 Jul web-verified authoring/formatting best practice.
- `index.html`, `standards.html`, `_kb/` — the generated knowledge-base layer.

## Read in this order for build tasks

1. `rise-dossier-bundle/rise-dossier-index.md` — §5 is the standing instruction for Claude Code.
2. `rise-dossier-bundle/rise-claude-code-brief.md` — Milestone 1 (taxonomy v0.3 embedded as Appendix A).
3. `rise-dossier-bundle/rise-source-manifest.md` — **execute before writing any seed data.**
4. `rise-dossier-bundle/rise-milestone-2-gap-engine.md` — Milestone 2.
5. `rise-ndis-package/rise-developer-handoff.md` — the package's import plan.

## Hard rules (the collection's own discipline — do not relax)

- Never reconstruct clause numbers, section numbers, register IDs, F-numbers, counts or quotes from memory. Retrieve from a file in this repo or a fetched primary source, or leave an explicit `[GAP]`.
- Label claims: verified `[V]` (with source and date) / corroborated `[C]` / design opinion `[D]`. Anything reconstructed later "from memory" of past sessions is unverified by definition.
- The register workbook's READ ME sheet is authoritative for counts when records disagree.
- Treat the three collection folders as **read-only provenance**. Do not edit their files in place; new or superseding work goes in new top-level folders (like `rise-authoring-research/`), versioned, stating what it supersedes.
- Statutory addresses were last verified against fetched instruments in prior sessions (SIL Rules clauses are TBC in the register itself). Before anything load-bearing, re-verify against the in-force compilations on legislation.gov.au: PRPS Rules F2018L00631 · QI Guidelines C03 F2026C00528.
- Not legal advice. Where anything here disagrees with the instrument on the Federal Register, the instrument governs.

## Generated vs source — never hand-edit outputs

`index.html`, `standards.html`, and every rendered `.html` that sits beside a source file (each `*.md` → `.html`, plus `*.py.html`, `*.json.html`, `*.mermaid.html`, `*.xlsx.html`) are **outputs** of `_kb/build_kb.py`. To change them, change the script or the source files, then regenerate from the repo root:

```
pip install openpyxl markdown
python3 _kb/build_kb.py
```

Run in-place it re-renders everything and rewrites `index.html`, `standards.html` and this file; it does not move or delete the collections. It prints sanity counts on completion (expected: 66/70 plain-English matches, 123 suite documents).

## Current open items (as at 7 Jul 2026 — see the index status band)

SIL Rules clauses (TBC in the register) · fresh-fetch currency check of all addresses · two statutory timeframes flagged "confirm before approval" · Easy Read companions flagged but not drafted (production standard: `rise-authoring-research/`) · four standards with no implementing document (M2-2, M2-4, M2-6, M2A-3 — review whether intentional) · the bundle's seven-item open-questions register.

## Layout note

The tree is preserved as-uploaded (provenance-faithful). The unified repo layout proposed in `rise-audit-pack/04-manifest/rise-collection-manifest.md` §2 is a documented restructure option — note it predates `standards.html`, `index.html`, the bundle and the authoring research, so adopting it means extending that plan and updating this generator's paths, as its own versioned step.
