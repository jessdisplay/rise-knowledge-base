# Rise — UI interaction notes: the five-panel book system

**Status:** design analysis for the developer, from the screenshot and the
72-second screen recording reviewed 6–7 July 2026. Method: sixteen sparse frames
plus a one-frame-per-second pass plus a four-frames-per-second transition burst; no
audio analysed; animation trigger and timing inferred only where stated.

## Verified from the recording

- The book mechanic: closed sections collapse to numbered spines on the left and
  right edges; the open spread shows one or two panes with section header bars; the
  spine numbers redistribute as the reader moves; transitions are horizontal
  slides (pane compresses toward its spine while the next expands), not swaps.
- Observed panel states: Policy alone; Policy+Procedure spread; Forms alone;
  Registers alone. Pills at top right track the open sections.
- Wider flow: login → dashboard (audit progress) → checklist review with a
  Conforms/Non-Conforming toggle and threaded comments → pack selection (packs map
  to modules: Certification Pack, Module 1, Module 2, Module 2A) → coach mark →
  the book → notifications panel with threaded updates.

**Not shown in the recording (open, not disproven):** what triggers slides (pill,
spine, or swipe — cursor illegible at sampled resolutions); any non-adjacent spread;
any in-content link navigation. All movement observed was section-driven.

## Design recommendations (opinions, with trade-offs)

1. **Pane 1 must hold both instruments, anchored.** "Legislation" for a standard
   means landing on the Rules clause *and* the Guidelines section (e.g. Sch 1 cl 3
   and s 6), not the top of a 60-page instrument. The verified addresses are the
   anchors; ingestion (Milestone 1/manifest) makes them real.
2. **Chips are edges; a link's destination is a spread.** Generate in-content link
   chips from the graph's typed relationships. Tapping "evidenced in the register"
   from pane 1 should open panes 1 and 5 *together*, so the link is seen in context.
   See `rise-bounce-prototype.html` for the working interaction (vertical layout;
   port the chips, not the layout).
3. **The non-adjacent question — the decisive fork.** A physical book opens only
   adjacent pages; the golden thread routinely needs 1-beside-5 and 2-beside-4.
   Options: (a) arbitrary pairs — breaks book physics, serves the workflow;
   (b) adjacency-only with fast flipping — preserves the metaphor, makes the
   auditor's most common comparison a three-flip journey; (c) **pin and swap**
   (recommended): pin the left page, cycle the right page through 2–5 against it.
   Option (c) is the auditor's mapping matrix made physical and should demo well
   with the pilot provider. Decide before building further navigation.
4. **Pages render by reference, never by copy.** One policy serves many standards;
   the same document node must appear in many packs/books. Per-pack copies would
   silently fork the 123-document suite.
5. **Merge fields from one source.** Organisation, contact and date fields render
   into every pane from a single record — the "Freazer/Fraeser" mismatch observed
   in test data becomes structurally impossible.
6. **Comments should become typed links.** The recording shows a reviewer
   hand-writing "align with section [n] of the Standard" as prose. Offer an
   address picker in comments so cross-references become structured findings
   attached to real nodes — they then feed gap reports and survive renames.
   Cheapest first step toward semantic navigation; uses existing review behaviour.
7. **Structural vs semantic navigation (framing).** The book currently provides
   structural navigation (flip to section 4). The graph adds semantic navigation
   (jump to the piece of section 4 this indicator forces). A document viewer needs
   the first; the product is the second wearing the first as clothing.

## Small verified catches worth keeping

- Both instruments genuinely title some standards differently (e.g. Rules
  "Enrolment of specialist disability accommodation dwellings" vs Guidelines
  "Enrolment of SDA Properties"; "Medication management" vs "Management of
  medication"). Store both titles, attributed. The build's use of the Rules title
  was legitimate, not drift.
- Mobile is undesigned territory: the recording is 1920×1080 desktop; on phones the
  spread collapses to one page plus spines — design that state deliberately.
