# Rise source manifest — authoritative copies and how to take them

**Purpose.** "Copies of everything," done safely. Rise's stored copies must come from
the Federal Register of Legislation via download, never from retyped text, chat
transcripts, or screenshots. This manifest lists every instrument in scope, its
register ID where sighted, and its verification status as at 7 July 2026.

## Ingestion rules (hard requirements)

1. Download only from legislation.gov.au (or ndiscommission.gov.au for guidance
   documents). Record for every file: register ID, compilation number, compilation
   date, retrieval timestamp, source URL, and a content hash.
2. On download, verify the compilation ID on the document's authorisation page
   matches this manifest; if the register shows a newer compilation, take the newer
   one and flag the manifest as superseded.
3. Never fill gaps from memory or from AI output. If an ID below is marked
   "not sighted," locate it on the register before ingesting — do not guess F-numbers.
4. Re-check the register on a schedule. Rules s 24 applies the Quality Indicators
   "as existing from time to time," so the *current* compilation is always the
   operative one — stored copies are snapshots for audit trail, not substitutes.

## Core instruments

| Instrument | Register ID | Status |
|---|---|---|
| National Disability Insurance Scheme Act 2013 (Cth) | C2013A00020 | ID and URL sighted in Commission material; not fetched — verify on download |
| NDIS (Provider Registration and Practice Standards) Rules 2018 | Series F2018L00631 · Compilation No. 4 = F2021C01137 (includes amendments up to F2021L01480) | **Fetched and verified in session** (authorised PDF, 15 Nov 2021). Note: 2026 amendments exist and are not consolidated in C04 |
| NDIS (Quality Indicators for NDIS Practice Standards) Guidelines 2018 | F2018N00041 · Compilation No. 1 (15 Nov 2021) | **Fetched and verified in session** (full text). A newer compilation reportedly exists (C03, 1 Jul 2026 per the Rise build) — locate and prefer it |

## 2026 amending instruments (names verified, IDs not sighted — locate on register)

| Instrument | Register ID | Status |
|---|---|---|
| NDIS (Provider Registration and Practice Standards) Amendment (Mandatory Registration and Other Matters) Rules 2026 | not sighted | Name verified via Commission; commenced 1 Jul 2026 |
| NDIS (Quality Indicators for NDIS Practice Standards) Amendment (Supported Independent Living) Guidelines 2026 | not sighted | Name verified via Commission |
| NDIS Amendment (Integrity and Safeguarding) Act 2026 | not sighted | Passage ~31 Mar–1 Apr 2026 per secondary sources (dates conflict by a day) |
| Supported independent living Practice Standards (new module) | not sighted | Existence verified; schedule/section placement unknown — never infer |

## Companion rulebooks named by the standards or Commission (IDs sighted in sources; verify each on download)

| Instrument | Register ID sighted |
|---|---|
| NDIS (Incident Management and Reportable Incidents) Rules 2018 | F2018L00633 |
| NDIS (Complaints Management and Resolution) Rules 2018 | F2018L00634 |
| NDIS (Restrictive Practices and Behaviour Support) Rules 2018 | series F2018L00632 · compilation F2020C01087 |
| NDIS (Specialist Disability Accommodation Conditions) Rule 2018 | F2020C00549 |
| NDIS (Practice Standards – Worker Screening) Rules 2018 | F2021C00788 |
| NDIS (Provider Definition) Rule 2018 | F2021C00694 |
| NDIS (Quality and Safeguards Commission and Other Measures) Transitional Rules 2018 | F2020C01102 |
| NDIS (Protection and Disclosure of Information – Commissioner) Rules 2018 | F2021C00306 |
| NDIS (Approved Quality Auditors Scheme) Guidelines 2018 | F2018N00114 |
| NDIS (Approved Quality Auditors) Rules 2025 | F2025L01383 |

## Status legend

- **Fetched and verified in session** — the full text passed through Claude's context
  on 6–7 July 2026 and structural claims in the Rise documents were checked against it.
- **ID sighted** — the register ID appeared in Commission or reputable secondary
  sources this session; the document itself was not opened. Verify title and
  currency on download.
- **Not sighted** — the instrument's existence is verified but no register ID was
  observed. Locate it on legislation.gov.au; inventing an F-number is prohibited.
