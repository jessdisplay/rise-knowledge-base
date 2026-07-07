# How an NDIS Auditor Checks a Provider Against the Practice Standards
### A layered guide (age-5 → data-model) + a best-practice checklist

**Prepared for:** Rise Development
**Date:** 6 July 2026
**Purpose:** Deep-research reference on how an Approved Quality Auditor (AQA) tests a provider's *policies, procedures, forms, registers and records* against the NDIS Practice Standards and Quality Indicators — plus a best-practice checklist and an analysis of a real audit report.

---

## 0. How to read this document (source discipline)

Every substantive claim below carries an epistemic label, matching the V/C/T/D convention used in prior Rise sessions:

| Label | Meaning |
|---|---|
| **[V]** | **Verified** this session against a primary or authoritative source (NDIS Commission text, legislation-derived instrument, or a real audit report). |
| **[C]** | **Corroborated** — multiple independent secondary sources agree, but I did not confirm against the primary instrument this session. |
| **[T]** | **Tentative** — a single source, or a source with a commercial interest, or otherwise weak. |
| **[D]** | **Draft / inference** — my synthesis or interpretation, not a sourced fact. |
| **[M-unverified]** | Carried from prior-session Rise memory (e.g. specific FRL IDs / section numbers) that I **did not re-verify this session**. Treat as a claim to check, not a fact. |

**Two honesty notes up front:**

1. **I could not fetch `ndiscommission.gov.au` pages directly** — the site blocks automated retrieval. Everything attributed to the Commission below comes from its own text surfaced via search snippets, which I judged reliable but is not the same as reading the published instrument end-to-end. Where a detail matters for Rise's graph, verify against the live page or the Federal Register of Legislation.
2. **The "real audit report" evidence is genuine and strong.** I read a full 54-page NDIS *Re-certification Audit Report* (SAI Global, for a Victorian provider, 2022) that the provider published on its own website. That is the single most useful artefact here for your crosswalk work, because it shows *exactly* how an auditor maps documents → indicators. **[V]**

---

## Level 1 — Explain like I'm 5

Imagine you run a shop that helps people. **[D]**

A grown-up whose job is to *check* comes to visit. They are **not** from the government and they are **not** your boss — they're an independent checker the government trusts. **[V]**

They have a **list of promises** every helper-shop must keep: *be kind, be safe, listen to the person, keep secrets safe, don't hurt anyone, fix mistakes.* **[C]**

The checker does three things, over and over: **[V]**

1. **"Show me the rule."** → *Do you have it written down?* (your **policy**)
2. **"Show me how you do it."** → *Is there a step-by-step?* (your **procedure**, and the **forms** people fill in)
3. **"Show me it really happens."** → They ask your workers, they ask the people you help, and they look around. **[V]**

If all three match — *written down, steps exist, and it really happens* — you get a **tick**. **[D]**
If something's missing, you get a **"please fix this."** A small fix = you keep going and fix it soon. A big fix = you must fix it before you're allowed to keep going. **[V]**

That's the whole game: **say it, do it, prove it.**

---

## Level 2 — Plain English (the shape of the system)

**[C] unless marked.**

- Anyone who wants to be a **registered** NDIS provider must pass an independent **quality audit** before (and periodically after) registration. The NDIS Commission itself does not run the audit; it *authorises* private certification bodies — **Approved Quality Auditors (AQAs)** — to do it. **[V]**
- The AQAs are accredited and monitored by **JAS-ANZ** (the Joint Accreditation System of Australia and New Zealand) on the Commission's behalf; the accreditation is anchored in the international conformity-assessment standard **ISO/IEC 17065**. **[V]**
- What the auditor measures a provider against is the **NDIS Practice Standards** (high-level, participant-focused *outcomes*) plus the **Quality Indicators** (the concrete things an auditor looks for to decide whether each outcome is met). **[V]**
- There are **two audit pathways**, decided by the *risk/complexity of the registration groups* the provider applies for — not by the provider's preference: **[V]**
  - **Verification audit** — lower-risk / lower-complexity supports. A **desktop review** of a defined document set (qualifications, insurance, complaints, incidents, worker screening, self-assessment). Usually one auditor, no site visit. **[V/C]**
  - **Certification audit** — higher-risk / more complex supports. **Two stages**: Stage 1 (document/system review, usually off-site) then Stage 2 (on-site: interviews with staff *and* participants, file reviews, observation). At least **two auditors**. **[V/C]**
- The output is an **audit report** with a **rating against every applicable standard and indicator**, submitted to the Commission. The Commission — not the auditor — makes the actual **registration decision**. **[V]**
- Certification registration runs up to **3 years** with a **mid-term audit** (~18 months) focused on governance/operational management plus any prior problem areas. Verification registration runs up to **5 years** with a renewal audit at expiry. **[C]** *(Timeframes are widely and consistently reported by AQAs; confirm the mid-term basis against the Provider Registration & Practice Standards Rules if precision matters — see §7.)*

---

## Level 3 — The regulatory stack (the part that matters most for Rise)

This is the hierarchy your typed-edge graph is trying to represent. Direction of authority runs **upward** (dependent artefact → its authority), matching your v0.3 convention (procedure → policy → standard → indicator → rules → Act). **[D for the framing; underlying facts labelled below.]**

```
National Disability Insurance Scheme Act 2013 (primary legislation)      [C]
        ▲
NDIS (Provider Registration and Practice Standards) Rules 2018           [V that the Standards live here]
  → contains / gives force to the NDIS Practice Standards (the OUTCOMES)  [M-unverified FRL: F2018L00631]
        ▲
NDIS (Quality Indicators) Guidelines 2018 (the INDICATORS auditors use)  [V that indicators are a separate instrument]
  → 2026 amendment added Supported Independent Living indicators          [V: "…Quality Indicators…Amendment (Supported Independent Living) Guidelines 2026"]
        ▲
──────── (the line where regulation stops and the PROVIDER begins) ────────
        ▲
Provider POLICIES        (the provider's written commitment per outcome)  [V from real report]
        ▲
Provider PROCEDURES      (the step-by-step that operationalises a policy)  [V]
        ▲
FORMS / TEMPLATES / REGISTERS  (consent forms, service agreements,
   risk registers, incident registers, RAR register, CI register…)        [V]
        ▲
RECORDS / EVIDENCE       (completed forms, file notes, minutes, training
   logs, interviews, site observation — what proves it actually happens)   [V]
```

**The single most important mechanic for your crosswalk:** the auditor does **not** grade a policy in isolation. For each *indicator*, they assemble a **bundle** of artefacts that together demonstrate the outcome, then **triangulate** across three evidence modes — **document review + interview + observation**. A policy with no procedure, or a procedure with no completed records, or records that contradict what staff say in interview, does not pass. **[V — this is exactly what the real report shows.]**

The Commission's own description of the auditor's stance captures it: the auditor examines the documented system, then repeatedly asks *"Can you show me?"* — moving from what's written to what's evidenced in board minutes, incident reports, risk registers, improvement logs, and lived practice. **[V]**

> **Rise modelling note [D]:** In the real report, the provider had **"mapped policies and procedures to the standards."** That artefact — a provider-side policy-to-indicator crosswalk — is functionally the same object Rise generates. An auditor treats its *existence and currency* as evidence under Quality Management (Outcome 2.3). This is a concrete product hook: Rise's crosswalk is not just internal scaffolding, it is itself an auditable artefact.

---

## Level 4 — How the auditor actually works (mechanics)

**[V/C] as marked. Grounded in the Commission's auditor guidance and the real report.**

### 4.1 Before arriving
The auditor reviews the provider's **scope of registration**, **previous audit history**, and any **higher-risk modules**, and plans a **sampling approach** (which sites, which participant files, which workers). Their role is to *evaluate*, explicitly **not** to consult or coach. **[V]**

### 4.2 Certification: Stage 1 then Stage 2
- **Stage 1 (documentation/system review):** reviews the **self-assessment** and the policy/procedure suite; identifies gaps and readiness. Stage 1 findings must be given to the provider before Stage 2 (reported as ~2 weeks prior if a non-conformity was found, ~1 week if not). **[C]**
- **Stage 2 (on-site):** tests **implementation** — interviews **key personnel, workers who directly deliver support, and participants** (individually, not only in groups; face-to-face where possible; guided by participant preference), reviews participant and staff **files**, and **observes** the environment/service. **[V]**

### 4.3 The three evidence modes (triangulation)
1. **Document review** — policies, procedures, forms, registers, plans, minutes, training records, staff files. **[V]**
2. **Interview** — do workers *know* the procedure? do participants *experience* the outcome? **[V]**
3. **Observation / site inspection** — signage, safety equipment, environment, physical practice. **[V]**

### 4.4 Sampling
Auditors sample rather than review everything. Real-report example: a **minimum of 5 participants** interviewed (or all, if the provider has ≤5); staff files sampled (6 of 12 in the real case). Site sampling determines which locations are physically visited. **[V]**

### 4.5 The rating scale (per standard *and* per indicator)
A **0–3** scale is applied. **[V — appears in the real report; wording corroborated against the AQA Scheme Guidelines via secondary source.]**

| Score | Label | Meaning |
|---|---|---|
| **3** | Conformity with elements of best practice | Clearly demonstrates best practice — innovative, responsive, continuous improvement. **[C]** |
| **2** | Conformity | Outcomes/indicators met, proportionate to size and scale. **[V — the rating used throughout the real report]** |
| **1** | Minor non-conformity | Gap that does *not* immediately risk participants; longer to fix; registration can continue. **[V]** |
| **0** | Major non-conformity | Serious gap; **3 months** to fix; registration does **not** progress until closed and re-audited. **[V]** |

- **Critical risk** (uncontrolled risk to participant safety, incl. matters under the Incident Management & Reportable Incidents Rules 2018) → the auditor must **notify the Commission immediately or within 24 hours**, and this usually triggers an on-site follow-up/re-audit within 3 months. **[V]**
- After the audit the auditor requests a **corrective action plan (CAP)** for any non-conformity; unresolved 0/1 ratings become **"open non-conformities"** followed up within set timeframes (desktop or on-site). **[V]**

### 4.6 Report → review → submission → decision
The draft report is shown to the provider for **factual-accuracy** correction (not to negotiate findings), then a **technical reviewer** independent of the audit checks it is accurate, complete, and properly documents any auditor/provider disagreement. It is submitted to the Commission — **within ~14 days (verification)** or **~28 days (certification / mid-term)**. The Commission then decides registration, may request more information, or impose conditions. **[V]**

---

## Level 5 — Anatomy of a REAL audit report (SAI Global, 2022) **[V]**

This is the structure you asked to "look at." Reproduced as *structure*, paraphrased (not verbatim), from a genuine published NDIS re-certification report covering the Core Module + Module 4 (Specialised Support Coordination).

**Report sections, in order:**

1. **Cover / metadata** — organisation, trading name, **all site addresses**, **scope** (each registration group by code, e.g. `0132 Support Coordination`, `0136 Group & Centre-Based Activities`), audit dates, audit team (Lead Auditor + Auditor), work-item IDs, report version.
2. **Background information** — purpose, the ISO/IEC 17065 + ISO 19011 basis, the **sampling caveat** (audit is based on a sample, not exhaustive).
3. **Executive overview** — narrative of what was found, changes to the plan (e.g. a site toured remotely), overall effectiveness, and **named strengths**.
4. **Recommendation** — which groups get a **Certification** recommendation vs **Provisional Certification** (groups with no current participants).
5. **Meeting attendance register** — who was in the opening/closing meetings, entry/exit.
6. **Organisational overview** — what the provider does, history, whether it serves children (0–16).
7. **Staff numbers + number of staff files audited** (e.g. 6 of 12).
8. **Participant interview methodology & file reviews** — a **table by registration group**: participants, number interviewed, method (phone/face-to-face/carer), files reviewed; opt-outs and reasons.
9. **Client & stakeholder feedback summary** — direct positive quotes and **"opportunities for improvement"** raised by participants/families.
10. **Staff file review details** — a **per-worker table**: role, risk category, **Worker Screening (NDIS check number + expiry, WWCC)**, qualifications/training (incl. **NDIS Worker Orientation module**, infection-control modules), and HR documentation (signed Code of Conduct, PD, induction checklist, references, supervision notes).
11. **Summary of audit findings (the rating table)** — every standard and sub-outcome listed with its score. In this case: **Core Module 1.1–1.5, 2.1–2.9, 3.1–3.5, 4.1–4.5, and Module 4's three standards — all "2 – Conformity."**
12. **Per-outcome findings** — for **each** indicator: the **Outcome** statement, a per-indicator **Rating**, then three labelled blocks:
    - **EVIDENCE:** — a dense list of the *named documents with version numbers and dates* that demonstrate the outcome, followed by what **interviews** and **site tours** confirmed.
    - **Opportunities for improvement** — non-binding observations (e.g. *consent forms "not as easy-read as they could be"*; a first-aid kit with expired items; an org chart with inconsistent titles).
    - **Non-conformity** — here, N/A throughout.

**Why this artefact is gold for Rise [D]:** Section 12 *is* a crosswalk instance. For **Outcome 1.1 (Person-Centred Supports)** alone, the auditor cited: *NDIS Participants Rights & Responsibilities Policy & Procedure; Participant Charter; Participant Handbook (V12, dated); Service Delivery Policy & Procedure; Physical Accessibility Policy & Procedure; Decision-Making & Choice Policy & Procedure; Policy Manual; Your Rights & Responsibilities (V4); Client Charter (V7); Service Agreement — easy read (V9); Staff Orientation & Induction Checklist (V1)* — **plus** staff interviews and reviewed welcome packs. That is a **many-to-one edge fan-in**: many provider artefacts → one indicator → one outcome. Every one of those documents carried a **version and date**, which is precisely the **bitemporal / version discipline** your model treats as day-one. The auditor's implicit test is: *is this version current, approved, and consistent with practice?*

---

## 6. THE BEST-PRACTICE CHECKLIST

**How to use it [D]:** For each Core Module outcome, the checklist states *what the auditor is testing*, the *artefacts that typically map to it*, and the *evidence modes* they'll triangulate. Aim for **"say it (policy) → do it (procedure + form) → prove it (records + interview + observation)."** Every document should be **version-controlled, approved, dated, and reflected in real practice** — the most common audit failure is the **gap between what the policy says and what actually happens**. **[C]**

> The mapping of documents→outcomes below is **[C/D]**: it reflects what the real report and multiple provider-guidance sources show auditors looking for. It is *typical*, not a legislated list. Treat it as a strong default to verify against the current Practice Standards + Quality Indicators text for the provider's specific scope.

### Module structure (what applies to whom) **[V/C]**
- **Core Module — Groups 1 & 2 (Rights & Responsibilities; Governance & Operational Management): apply to EVERY registered provider.** **[V]**
- **Core Module — Group 3 (Provision of Supports) & Group 4 (Support Provision Environment):** apply depending on whether the provider delivers direct/ongoing supports and, for environment, settings like SIL/shared living. *(Some sources order these differently — confirm against the current module text.)* **[T on the exact Group-3/4 ordering; V that both exist.]**
- **Supplementary modules** apply by registration group: High-Intensity Daily Personal Activities; Specialist Behaviour Support (+ Implementing BSPs); Early Childhood; Specialised Support Coordination (Module 4); Specialist Disability Accommodation; **Supported Independent Living (new — see §7).** **[V/C]**
- **Verification Module** — the pared-down outcome set for verification-only providers. **[C]**

---

### Group 1 — Rights and Responsibility (all providers)

**1.1 Person-Centred Supports** — *rights understood and built into everyday practice; accessible communication; supported to engage with support network.*
- [ ] Rights & Responsibilities policy **and** procedure, referencing UN CRPD / human-rights & disability legislation **[V pattern]**
- [ ] Participant Charter + Participant Handbook (accessible / easy-read versions)
- [ ] Accessible-communication / interpreter provisions documented
- [ ] Evidence in **practice**: staff can describe it; participants confirm information was clear
- **Auditor tests:** document review + participant interview + staff interview.

**1.2 Individual Values and Beliefs** — *culture, diversity, values, beliefs identified and respected.*
- [ ] Cultural responsiveness in service-delivery / decision-making procedures
- [ ] Prompts for cultural/religious context in planning templates
- [ ] Participants/families confirm culturally appropriate support.

**1.3 Privacy and Dignity** — *consistent privacy practices; confidentiality explained accessibly; informed consent incl. audio/visual.*
- [ ] Privacy & Confidentiality policy/procedure + **easy-read privacy flyer**
- [ ] Consent / image-release **forms** (ideally granular, not blanket)
- [ ] Signage for any cameras/recording; observed in site tour
- **Real-report gotcha:** blanket consent with no "program-use-only" option was flagged as an *opportunity for improvement*. **[V]**

**1.4 Independence and Informed Choice** — *active decision-making; dignity of risk; autonomy incl. intimacy/sexual expression; time to decide; advocate access.*
- [ ] Decision-Making & Choice policy referencing guardianship/administration law
- [ ] "Your Right to Advocacy" information + advocate contacts
- [ ] Dignity-of-risk documented, not just "safety-first"
- [ ] Files show participants given time; consent re-signed periodically.

**1.5 Violence, Abuse, Neglect, Exploitation & Discrimination (VANED)** — *active prevention; advocate access on allegation; allegations acted on, recorded, learned from.*
- [ ] Protecting-Participants-from-Harm policy with definitions, prevention, response, investigation (incl. concurrent police involvement)
- [ ] Anti-discrimination / harassment policy
- [ ] Link to incident system + advocacy
- [ ] Screened, risk-assessed roles.

---

### Group 2 — Provider Governance and Operational Management (all providers)

**2.1 Governance & Operational Management** — *robust, proportionate governance; people-with-disability input; defined structure meeting legislative/financial/regulatory duties; delegations; conflict of interest.*
- [ ] Governance framework / policy + **organisational chart with clear accountability**
- [ ] Strategic + business plan referencing legislative requirements & risks
- [ ] **Delegations register** (incl. absence delegations)
- [ ] **Conflict-of-Interest register / policy**
- [ ] Key-personnel records; board/management oversight evidence (minutes)
- **Real-report gotcha:** inconsistent role titles across documents, and surveys not run per policy during COVID, were flagged. **[V]**

**2.2 Risk Management** — *risks to participants/workers/provider identified, analysed, treated; system covers incidents, complaints, financial, governance, HR, information, WHS, emergency/disaster; infection control where relevant; appropriate insurance.*
- [ ] Risk Management policy + **Risk Register** (identify→analyse→treat→monitor→report)
- [ ] Individual participant risk assessments
- [ ] Financial-management controls (delegations, anti-fraud, accounting-standard reference)
- [ ] **Insurance register + current certificates** (public liability, professional indemnity, accident/WorkCover)
- **Real-report gotcha:** untested/untagged electrical equipment and expired first-aid items at a delivery site. **[V]**

**2.3 Quality Management** — *proportionate QMS defining how legislation & standards are met; documented internal-audit program; continuous improvement from outcomes, risk data, feedback.*
- [ ] QMS / Policy & Procedures Manual, **version-controlled**
- [ ] **Policies mapped to the Practice Standards** ← *this is the crosswalk artefact*
- [ ] Internal-audit schedule + completed internal-audit records
- [ ] **Continuous Improvement Register** with action / owner / timeline
- **Rise hook [D]:** currency of the policy-to-standard map is itself audited here.

**2.4 Information Management** — *participant info identifiable, accurate, current, confidential, accessible to the participant, appropriately used by workers; consent to collect/use/disclose; storage/retention/destruction.*
- [ ] Records & Information Management policy (retention aligned to legislated timeframes)
- [ ] Data-breach notification provision
- [ ] Access/correction/withdraw-consent process
- **Real-report gotcha:** a worker's health-identifier number (HIN) visible on vaccination records. **[V]**

**2.5 Feedback & Complaints Management** — *accessible complaints system compliant with the Complaints Management & Resolution Rules 2018; procedural fairness; external avenues incl. Commission; continuous improvement; workers trained.*
- [ ] Feedback/Complaints policy referencing the Complaints Rules
- [ ] Accessible complaints flyer + Commission contact details
- [ ] **Feedback/Complaints register** with resolution + trend review
- [ ] Staff trained (records).

**2.6 Incident Management** — *system compliant with the Incident Management & Reportable Incidents Rules 2018; participants informed; continuous improvement; workers trained.*
- [ ] Incident Management policy referencing the Incident Rules (definitions, reportable-incident **timeframes**)
- [ ] **Incident register** + incident report forms
- [ ] Cross-references to other regulators where relevant
- [ ] Staff trained (records).

**2.7 Human Resource Management** — *role skills defined; pre-employment checks; orientation incl. mandatory NDIS Worker Orientation; training system; supervision; performance management; emergency-capable workforce; infection-control training; contact + secondary-employment details recorded.*
- [ ] Position descriptions with role requirements + **risk-assessed-role (RAR) determination**
- [ ] **Worker Screening**: NDIS Worker Screening Check (valid 5 yrs) + WWCC where relevant; register with numbers/expiries
- [ ] NDIS Worker Orientation module completion
- [ ] Training calendar + records (incl. infection control + refreshers)
- [ ] Supervision + performance records
- **Real-report gotcha:** infection-control records missing from newer staff files; a qualification not retained on file. **[V]**

**2.8 Continuity of Supports** — *no interruption; cover for absence/vacancy; documented preferences given to workers; arrangements across the service agreement.*
- [ ] Continuity arrangements + business-continuity plan
- [ ] Absence/vacancy cover documented
- **Real-report gotcha:** a "business continuity plan" that was really an infection-control statement and didn't address staff absence. **[V]**

**2.9 Emergency & Disaster Management** — *plans for continuity of critical supports before/during/after; governing-body-owned, tested, reviewed, communicated; each worker trained.* (A comparatively recent addition — watch for providers whose older maps predate it.)
- [ ] Emergency Management Plan + evacuation plans per site
- [ ] Evidence of **testing** and periodic review, with participant consultation
- [ ] Worker training records.

---

### Group 3 — Provision of Supports (providers delivering direct supports)

**3.1 Access to Supports** — *supports & entry criteria/costs defined & communicated accessibly; reasonable adjustments; supports not withdrawn solely for a dignity-of-risk choice.*
- [ ] Service Access policy (waitlist fairness, entry/exit/eligibility/cost)
- [ ] Information pack; documented reasons for any refusal.

**3.2 Support Planning** — *participant actively involved; plans reflect needs/goals/strengths; risk assessments in plans; annual (or earlier) review; preventative-health & emergency responses incorporated.*
- [ ] Assessment/Planning/Review policy
- [ ] Individual support plans + individual risk assessments
- [ ] Annual review evidence in files.

**3.3 Service Agreements** — *collaboratively developed; understood accessibly; signed copy provided (or reason recorded); SIL-in-SDA arrangements documented; emergency arrangements set out.*
- [ ] Service-agreement template (accessible/easy-read) + signed copies in files
- [ ] Record kept where a participant declines / can't receive a copy
- **Real-report note:** the "easy-read" agreement still read at a grade-10 level — a quality nuance auditors notice. **[V]**

**3.4 Responsive Support Provision** — *least-intrusive, evidence-informed supports; links to health/allied providers with consent; participant involved in worker selection incl. gender for personal care; workers trained to specific needs.*
- [ ] Individualised support records / activity logs
- [ ] Evidence of least-restrictive, responsive practice.

**3.5 Transitions To/From the Provider** — *planned, collaborative, documented transition; transition risks (incl. temporary transitions like hospitalisation) identified and responded to.*
- [ ] Exit & Transition policy (incl. temporary transitions)
- [ ] Transition/exit plans in files.

---

### Group 4 — Support Provision Environment (settings-based, incl. SIL/shared living)

**4.1 Safe Environment** — *appropriate, safe setting; workers identifiable; medical-emergency protocols & trained workers; escalation; infection prevention & control incl. PPE, cleaning, hand-hygiene training.*
- [ ] Site safety checklists (per site) + observed conditions
- [ ] IPC precautions, PPE availability, cleaning of touch-points, training records.

**4.2 Participant Money and Property** — *safe handling; protection against financial loss.*
- [ ] Money/property-handling procedure + records.

**4.3 Management of Medication** — *safe storage, administration, recording (where in scope).*
- [ ] Medication policy — or a clear **"not in scope"** statement if the provider doesn't administer.
- **Real-report note:** provider explicitly scoped medication *out*, and the auditor accepted that. Scope-out statements are legitimate evidence. **[V]**

**4.4 Mealtime Management** — *safe mealtime/dysphagia management where relevant.*
- [ ] Mealtime-management / dysphagia procedures where applicable.

**4.5 Management of Waste** — *safe storage/disposal of hazardous/infectious waste per legislation; incidents reported; emergency plan; workers trained.*
- [ ] Waste-management procedure + training records.

---

### Cross-cutting "evidence hygiene" checklist (applies to everything) **[D, distilled from the real report]**
- [ ] Every document **version-numbered and dated**; superseded versions traceable *(your immutable-supersede edges map directly to this)*
- [ ] Every policy has a matching **procedure** and, where relevant, a **form/register**
- [ ] Every form has **completed instances** on file (proof of operation)
- [ ] **Registers are live** (incidents, complaints, risks, CI, delegations, insurance, RAR) — not empty templates
- [ ] Policy references to **legislation/rules are current** (watch renamed departments, superseded rules)
- [ ] **Staff can articulate** the procedure in interview
- [ ] **Participants confirm** the lived experience
- [ ] A **policy-to-standard map** exists and is current
- [ ] **Self-assessment** completed against the *current* standards (incl. newer outcomes like Emergency & Disaster Management)
- [ ] Proportionality is explicit: everything scaled to the provider's **size, scale, scope and complexity** (this phrase recurs in almost every indicator). **[V]**

---

## 7. The 2026 changes you must account for (with verification flags)

Because Rise is explicitly built to survive regulatory churn, here is what I could and could not verify this session.

**Verified this session [V]:**
- **SIL providers and NDIS digital-platform providers must be registered from 1 July 2026**, announced Dec 2025 by the Minister for the NDIS (Jenny McAllister). **[V]**
- The Commissioner made **two instruments** to give effect to this: the **NDIS (Provider Registration and Practice Standards) Amendment (Mandatory Registration and Other Matters) Rules 2026** and the **NDIS (Quality Indicators for NDIS Practice Standards) Amendment (Supported Independent Living) Guidelines 2026.** **[V]**
- New **SIL-specific Practice Standards** commence 1 July 2026, co-designed with Inclusion Australia and pilot-tested in an audit pilot (Feb–Mar 2026). They **sit alongside** the Core Module — providers must meet **both**. **[V]**
- SIL registration is a **Certification** pathway; existing registered SIL providers are assessed against the new SIL standards **at their next scheduled audit** (mid-term or renewal). **[C]**
- The **NDIS Amendment (Integrity and Safeguarding) Bill 2026 passed Parliament on 1 April 2026** — i.e. it amends the **NDIS Act 2013**; it is *not* a standalone "Integrity and Safeguarding Act." **[V]**

**Reported but not primary-verified this session [T]:**
- A new registration group **"0138 Assistance with Supported Independent Living"** commencing 1 July 2026, and the SIL standards described as a **"Supplementary Module."** **[T — single commercial source; plausible and consistent, but confirm on the Commission's SIL page / FRL.]**
- Various consultancies describe the new SIL standards as **"four domains"** (e.g. tenancy/housing-separate-from-support, choice & control, worker capability, quality of support). The Commission's own page frames SIL as a supplementary module with an Evidence Guide and Reflective Questions for Participants. **The exact published structure should be read from the final module, not from consultancy summaries.** **[T]**
- A broader **Practice Standards Review** (KPMG-led) proposing to replace the Core Module with **four "Core Practice Domains"** (Individual Rights, Provider Leadership, Safe Support Practice, Effective & Impactful Support) and to replace supplementary modules with outcomes-focused "Supplementary Quality Standards." **This is proposed / consultative, not commenced.** Do not model it as current law. **[C that a review exists and these are proposed; T on specifics.]**

**Carried from Rise memory, NOT re-verified this session [M-unverified]:**
- FRL IDs `F2018L00631` (PRPS Rules), `F2026C00528` / "C03 compilation" (QI Guidelines).
- SIL sections **"ss 72B–72E."** I found no confirmation of those specific section numbers this session — **verify against the Federal Register of Legislation before relying on them in the graph or any provider-facing artefact.**

---

## 8. Negative findings & open questions (worth recording per Rise practice)

- **NDIS certification/verification audit reports do not appear to be centrally published** by the Commission (unlike aged care, where quality-audit outcomes are publicly surfaced). The real report used here was **self-published by the provider on its own website** — a voluntary act, not a public register. **Confidence: [T].** I did not do an exhaustive search for a public register; I found none. *What would resolve it:* checking the Commission's provider-finder/registration pages and any FOI/disclosure logs. **Implication for Rise:** you cannot assume a corpus of real audit reports to train/validate against — your validation pilot's own provider documents are more valuable precisely because public exemplars are scarce.
- **The document→outcome mappings in §6 are typical, not authoritative.** They are induced from one real report plus provider guidance. The authoritative test is always the *current* Practice Standards + Quality Indicators text for the provider's specific registration groups. **[D]**
- **Group 3 vs Group 4 ordering / naming** varies between sources; treat the module ordering in §6 as indicative until confirmed against the current module. **[T]**
- **Mid-term audit basis** (18 months; governance-focused) is consistently reported but I did not read it from the Rules this session. **[C]**

---

## 9. Sources (what each is worth)

**Primary / authoritative [V-grade]:**
- NDIS Quality & Safeguards Commission — *The quality audit process*; *Information for quality auditors*; *NDIS Practice Standards* + *Core Module* pages; *Supplementary module: Supported independent living*; *NDIS regulatory reform / reform hub* (accessed via search snippets; direct fetch blocked by the site).
- **Real audit report:** SAI Global, *NDIS (Practice Standards) Re-certification Audit Report — Core Module + Module 4*, Prioletti Consultants Pty Ltd (t/a Catalyst), 2022 — full 54-page PDF read this session.
- NDIS (Approved Quality Auditors Scheme) Guidelines 2018 (via NDS-hosted copy) — for the ISO/IEC 17065 conformity-assessment basis and audit-program proportionality.

**Corroborating secondary [C-grade]:** Team DSC (rating-scale wording); NDS factsheet (registration/audit pathways); multiple AQA sites (HDAA, IHCA, Australian QC, Engels Floyd, GCC) and provider-guidance blogs (NDISCompliant, ClinicComply, Nomotix, iinduct) for pathway/timeframe/module details.

**Tentative [T-grade]:** consultancy posts describing the *proposed* Practice Standards Review "four domains," the SIL "four domains," and registration group 0138 — directionally useful, not authoritative.

---

*Prepared by Claude for Rise Development. Files are session-scoped — download and retain this document; it will not persist in a later conversation. Every mapping and 2026 detail flagged **[T]** or **[M-unverified]** should be confirmed against the current Commission text / Federal Register of Legislation before it enters the Rise graph or any provider-facing artefact.*
