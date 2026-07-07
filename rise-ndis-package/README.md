# Rise NDIS Package — README

**Bundle compiled 6 July 2026.** This is the complete Rise NDIS document-and-graph
package: the seed dataset, the 123-document suite, the interactive dossier, the design
and source documentation, and the generator scripts that rebuild everything.

Read `rise-developer-handoff.md` first for the technical index. This README is only
about **how to use the files you now have** — with an honest account of what works
offline and what doesn't.

---

## The one thing to understand first (please read)

**The dossier is a static website, not a running application.**

`rise-dossier.html` is a single self-contained HTML file. You can double-click it to
open it in any browser, or put it on any web server, and it will work the same way in
both cases: you can browse the legislation, standards and 123 documents, click any ID
to travel the links, read every drafted document, and use the graph explorer.

What it is **not**: it is not connected to a database, it has no login, it does not
save changes, and it does not update itself when the law changes. It is a *snapshot* of
the data as generated on the date above. If you edit a document, nothing is written
anywhere — the file is read-only in effect.

This matters because "load onto a server" can mean two very different things:

- **Serving the snapshot** (what this bundle does): copy `rise-dossier.html` to a web
  server and share the URL. Anyone can view it. This works today, offline or online.
- **Running the Rise platform** (what this bundle is *for*, but is *not*): a live
  application with a graph database, editing, versioning, and the legislative-change
  fan-out actually firing. That is the thing your developer builds *from* this package.
  This bundle is the specification and seed data for that build, not the build itself.

I'm stating this plainly because under an accuracy-first standard it would be wrong to
let "load onto a server" imply you're getting a working platform. You're getting a
complete, browsable, self-contained reference and demo — which is genuinely useful, but
it is a document, not software.

---

## How to open it

### Simplest — on your own computer

1. Unzip this bundle anywhere.
2. Double-click `rise-dossier.html`.
3. It opens in your default browser. Everything works. No internet required.

(Fonts are loaded from Google if you happen to be online, purely cosmetic. Offline, the
browser substitutes system fonts and it still looks clean — I made that load
non-blocking on purpose.)

### On a server (to share a link internally)

Any static host works because there is no backend. Examples:

- **Any web server:** copy `rise-dossier.html` (rename to `index.html` if you want it to
  load at the folder root) into the served directory. Done.
- **Python, for a quick local test:** in the unzipped folder run
  `python3 -m http.server 8000` then open `http://localhost:8000/rise-dossier.html`.
- **Static hosts** (Netlify, GitHub Pages, S3, an internal Nginx/Apache): upload the
  single HTML file. No build step, no configuration.

The other files (spreadsheet, JSON, markdown, scripts) are not needed to view the
dossier — everything the dossier shows is embedded inside the one HTML file. They are
included because your developer needs them and because you may want the source data
directly.

---

## What's in the bundle

**View / share**
- `rise-dossier.html` — the interactive dossier. Start here.
- `rise-document-register.xlsx` — the master register as a spreadsheet (123 documents,
  70 standards with QI references, 21 instruments, 528 links). Opens in Excel.

**The documents themselves**
- `suite/` — all 123 documents as Markdown, organised into type folders in hierarchy
  order: `01-policies` (33) · `02-procedures` (44) · `03-work-instructions` (3) ·
  `04-forms-and-agreements` (21) · `05-registers` (19) · `06-plans-and-handbooks` (3).
- `suite/00-INDEX.md` — **the mapping.** Every chain as a tree: policy → procedures →
  work instructions and forms → the register each form records to, with clickable
  relative links into the folders. Generated from the graph edges, so it cannot drift
  from the data. The incident chain is fully drafted; policy statements are drafted for
  every policy; other bodies are marked draft scaffolds (structure and links real,
  wording to be tailored).

**For the developer (build the real platform from these)**
- `rise-developer-handoff.md` — the technical index and import plan. **Their start
  point.**
- `rise-nodes-and-edges.json` — the seed graph (224 nodes, 528 edges) to import.
- `rise-node-examples.json` — the exact data shapes to implement.
- `rise-node-map.mermaid` — the node-type meta-model diagram.
- `rise-node-taxonomy.md`, `rise-document-architecture.md` — the schema and the
  document-generation rules.
- `rise_build.py`, `rise_docs.py`, `rise_dossier.py` — the generators. Run
  `python3 rise_build.py && python3 rise_docs.py && python3 rise_dossier.py` to rebuild
  the spreadsheet, JSON, all 123 documents, and the dossier from one source. Requires
  Python 3 with `openpyxl` installed.

**Understanding and provenance**
- `rise-plain-english-guide.md` — the whole NDIS compliance system explained for anyone.
- `rise-auditor-focus-map.md` — every area auditors examine, mapped to the documents
  that answer it, with Quality Indicators section numbers.
- `rise-methodology.md` — how the package was built and verified; how to challenge it.
- `rise-sources.md` — every claim traced to a tiered, dated source, including what was
  searched for and *not* found.
- `TPL-*.md` — the five blank document templates.

---

## Accuracy and status — what to trust

This carries over from the package's own documentation; repeated here so it travels with
the files:

- **Verified (against the Federal Register or the NDIS Commission, dated in
  `rise-sources.md`):** the instrument list and IDs; the standards and their clause
  citations; the Quality Indicators section for every standard (Guidelines compilation
  C03, in force 1 July 2026, including the new SIL Module 5A).
- **Drafted by me, needs review:** all document body content. The compliance *links* are
  generated from the data and are structurally reliable; the *words* are a starting
  point to be tailored to a specific provider and approved.
- **Explicitly unresolved (flagged in the files):** two statutory timeframes
  (reportable-incident and change-notification windows) are marked "confirm against the
  instrument before approval" rather than stated with false precision; SIL clause
  pinpoints in the PRPS Rules await the next compilation; some Easy Read companions are
  flagged as required but not yet drafted.
- **Not legal advice.** This is a compliance-engineering artefact. Where anything here
  disagrees with the actual instrument on the Federal Register, the instrument governs.

---

## If you want the *live* version next

The honest next step toward "running on a server" as an application is a build task for
your developer, not another document from me: stand up a graph store, import
`rise-nodes-and-edges.json`, and serve the documents and traversals through an
application layer. `rise-developer-handoff.md` §4 lays out that import order and the
validation gates. I can help scope or draft parts of that when you're ready — but I'd be
misrepresenting it to hand you these files and call it a deployable platform.
