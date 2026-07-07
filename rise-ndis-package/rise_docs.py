#!/usr/bin/env python3
"""Generates the full provider document suite from the Rise graph:
- suite/*.md            one markdown file per document (123)
- docs_html.json        {doc_id: rendered_html} for embedding in the dossier
Every compliance link is generated from the register edges - never hand-typed.
Body content: fully drafted for the incident chain; authored policy statements for
all policies; honest scaffolds elsewhere, each carrying a draft banner."""
import json, html, os, re
import rise_build as rb

esc = html.escape
GEN = "2026-07-06"
MODK = {m[0]: m[1] for m in rb.MODULES}

OUT, IN = {}, {}
for f, t, to, n in rb.E:
    OUT.setdefault(f, []).append((t, to, n))
    IN.setdefault(to, []).append((t, f, n))

def nm(i):
    if i in rb.DOCK: return rb.DOCK[i]["title"]
    if i in rb.STDK: return rb.STDK[i][3]
    if i in rb.LEGK: return rb.LEGK[i][1].replace("National Disability Insurance Scheme", "NDIS")
    return MODK.get(i, i)

def isdoc(i): return i in rb.DOCK

BANNER = ("DRAFT v0.1 - scaffold generated from the Rise compliance graph on " + GEN +
 ". All compliance links below are register-verified. Body content is a starting draft: "
 "review, tailor to [Provider Name] and approve before use. Not legal advice.")

PRIVACY = ("We collect this information to support you safely and to meet our legal duties. "
 "Only the people who need it will see it, and the NDIS Commission where the law requires. "
 "You can ask to see information about you at any time. See POL-INF-01.")

# ---------------- link table ----------------
GLOSS = [
 ("IMPLEMENTS","EXISTS TO MEET","This document exists to meet"),
 ("OPERATIONALISES","PUTS INTO PRACTICE","Puts this into day-to-day practice"),
 ("USES","CARRIED OUT USING","Carried out using"),
 ("RECORDS_TO","RECORDS END UP IN","Completed records are logged in"),
]
def link_rows(d):
    i = d["id"]; rows = []
    def tgt(x, extra=""):
        return (x, nm(x), extra)
    for ty, lab, gl in GLOSS:
        outs = [(to, n) for t, to, n in OUT.get(i, []) if t == ty]
        if outs:
            rows.append((lab, gl, [tgt(to, _std_extra(to)) for to, n in outs]))
    refs = [(to, n) for t, to, n in OUT.get(i, []) if t == "RELATES_TO" and n.startswith("Statutory reference")]
    if refs: rows.append(("REFERENCES","Other law this document must follow",[tgt(to) for to, n in refs]))
    invmap = {"OPERATIONALISES":("PUT INTO PRACTICE BY","Put into day-to-day practice by"),
              "USES":("USED WHEN CARRYING OUT","Filled in as part of"),
              "RECORDS_TO":("RECORDS ARRIVE FROM","Rows in this register come from")}
    for ty,(lab,gl) in invmap.items():
        ins = [f for t, f, n in IN.get(i, []) if t == ty]
        if ins: rows.append((lab, gl, [tgt(f) for f in ins]))
    rel = [(to, n, 1) for t, to, n in OUT.get(i, []) if t == "RELATES_TO" and not n.startswith("Statutory reference")]
    rel += [(f, n, 0) for t, f, n in IN.get(i, []) if t == "RELATES_TO" and not n.startswith("Statutory reference")]
    for x, n, _ in rel:
        rows.append(("RELATED","Connected because", [ (x, nm(x), " - " + n if n else "") ]))
    return rows

def _std_extra(sid):
    if sid in rb.STDK:
        c = rb.CIT.get(sid, ""); q = rb.QIREF.get(sid, "")
        bits = []
        if c: bits.append("PRPS " + c)
        if q: bits.append("indicators: QI Guidelines " + q)
        return (" - " + "; ".join(bits)) if bits else ""
    return ""

# ---------------- content library ----------------
S = {
"POL-GOV-01":["Our board and leadership own quality and safety, with decision-making delegations recorded in REG-GOV-01.","We keep our registration details current and notify the Commission of notifiable changes and events on time (PRO-GOV-02).","Decisions that affect participants are made at the right level and recorded.","We resource the systems this suite describes: risk, quality, complaints, incidents and people.","Leadership reviews compliance, incidents, complaints and improvement actions on a set cycle."],
"POL-GOV-02":["Everyone declares actual, potential and perceived conflicts of interest using FRM-GOV-01.","Declared conflicts are recorded in REG-GOV-02 and managed or removed before decisions are made.","Support coordination and SDA conflicts are handled under the specific module requirements.","No worker or key person may gain personally from a relationship with a participant.","The conflict register is reviewed by leadership on a set cycle."],
"POL-GOV-03":["Anyone - workers, participants, families, contractors - can report suspected wrongdoing, including anonymously.","We do not tolerate reprisals against anyone who speaks up in good faith.","A discloser's identity is protected; revealing it without consent is itself a breach.","Reports are assessed promptly and investigated in proportion to what is alleged.","Our settings follow the strengthened whistleblower protections introduced in 2026 - obtain legal review of the final wording before approval."],
"POL-RSK-01":["We identify risks to participants, workers, finances, work health and safety, and service delivery.","Every identified risk is rated, given an owner and a treatment, and entered in REG-RSK-01.","Participant-specific risks feed directly into support planning.","Incidents, complaints and audit findings feed back into the risk register.","Leadership reviews the register on a set cycle and after any serious event."],
"POL-QMS-01":["We run a documented quality system that covers everything we deliver.","Documents are controlled: current versions only, with owners and review dates (this suite's register is REG-GOV-03).","Improvements from any source - feedback, incidents, audits, ideas - are logged in REG-QMS-01 and followed through.","We audit ourselves against the Practice Standards on a planned schedule.","We measure whether changes actually worked before closing them."],
"POL-INF-01":["We collect only the information we need, with informed consent recorded on FRM-INF-01.","Information is stored securely and seen only by people who need it for their role.","Participants can see and correct information about them.","Suspected privacy breaches are handled immediately under PRO-INF-02, including our data-breach notification duties.","Records are kept, and destroyed, according to the retention rules that apply to them."],
"POL-FBK-01":["Feedback and complaints are welcome, easy to give, and can be made with support or anonymously.","No one is treated worse for complaining.","Complaints are acknowledged quickly and resolved fairly, with procedural fairness for everyone involved.","We always tell people about external options, including the NDIS Commission.","Every complaint is recorded in REG-FBK-01 and feeds our improvement register."],
"POL-INC-01":["The safety and wellbeing of participants comes before every other consideration when an incident occurs.","We record every incident, including near misses, in REG-INC-01.","We notify the NDIS Commission of reportable incidents within the timeframes set by the Incident Rules, using PRO-INC-02.","We support participants affected by an incident, including advocates and information they understand.","We review incidents to find causes and act on what we learn.","We never punish anyone for raising an incident in good faith."],
"POL-HRM-01":["Workers are screened before starting risk-assessed roles, with an NDIS Worker Screening Check verified and recorded.","Every worker is inducted on the NDIS Code of Conduct, safeguarding and the parts of this suite they use.","Workers are trained and assessed as competent for the supports they deliver, recorded in REG-HRM-02.","Workers receive regular supervision and honest performance feedback.","Only workers with current, assessed competence perform high intensity supports or administer medication."],
"POL-COC-01":["The NDIS Code of Conduct applies to every worker, key person, volunteer and contractor.","Everyone acknowledges the Code in writing before starting (FRM-HRM-02).","Code obligations are built into recruitment, induction, supervision and training.","We act on suspected breaches, including reporting where the law requires."],
"POL-COS-01":["Participants keep receiving their supports through disruptions, planned or not.","Worker absences are covered by planned backup arrangements participants know about.","We maintain and test a business continuity plan (PLN-COS-01).","Participants are told early and clearly when changes affect them."],
"POL-EDM-01":["We plan for emergencies and disasters for each service setting and each participant's needs.","Everyone knows their role in an emergency, and plans are practised.","Plans are reviewed after every activation, drill, and relevant external event.","Emergency planning connects to continuity of supports so care does not stop."],
"POL-RGT-01":["Each participant directs their own supports; we fit around their choices, not the reverse.","Culture, identity, values and beliefs are respected in how supports are delivered.","We communicate in each participant's preferred language, mode and pace.","We actively support access to advocates, interpreters and communication aids."],
"POL-RGT-02":["Personal care is delivered in a way that protects privacy and dignity, every time.","Personal information is handled under POL-INF-01 and shared only with consent or legal requirement.","Participants choose who is present and involved in their care wherever possible."],
"POL-RGT-03":["We presume every participant can make decisions, and we support decision-making rather than substitute for it.","Decisions are made with the participant, in their preferred way, with the people they choose.","Dignity of risk is respected: informed choices are supported and documented, not overridden.","Substitute decision-making is used only where the law provides, and recorded.","In SIL settings this policy operates through PRO-SIL-01 and FRM-SIL-01."],
"POL-SGD-01":["We have zero tolerance for violence, abuse, neglect, exploitation and discrimination.","Every worker can recognise the signs and knows how to respond and report, including reportable incidents.","We recruit safely, supervise actively, and act on concerns early.","Participants are supported to speak up safely, with advocates where wanted.","Concerns are never minimised because of a person's disability or communication style."],
"POL-SUP-01":["Who we can support, and any entry criteria and costs, are clear and communicated accessibly.","Access decisions are non-discriminatory and recorded.","Waiting arrangements are transparent and reviewed.","We do not refuse or withdraw supports just because a participant makes an informed dignity-of-risk choice."],
"POL-SUP-02":["Every participant has a current support plan they led the development of.","Plans reflect preferences, goals, communication needs and assessed risks.","Plans are reviewed on schedule and whenever circumstances change.","Workers deliver to the plan, and say so when the plan needs to change."],
"POL-SUP-03":["A written service agreement is in place before or as supports start.","Agreements are in plain language, with Easy Read available, and the participant keeps a copy.","Agreements cover the supports, costs, how to change things, and how either party can end them.","Changes are agreed, not imposed."],
"POL-SUP-04":["Entries, exits and transitions are planned with the participant and the people they choose.","Information transfers to new providers only with consent, using FRM-SUP-04.","Supports are never withdrawn abruptly or punitively.","Transition risks are assessed and managed."],
"POL-ENV-01":["Every environment where we deliver supports is safe and fit for purpose.","Hazards are checked using FRM-ENV-01, recorded in REG-ENV-01, and fixed.","Work health and safety duties are met alongside participant safety (POL-WHS-01)."],
"POL-MNY-01":["We handle participant money or property only with documented consent and a clear purpose.","Every transaction is recorded on FRM-MNY-01 with receipts, and logged in REG-MNY-01.","Verification controls apply to every transaction - no exceptions for small amounts.","Workers never borrow from, lend to, or benefit financially from participants.","The register is reconciled and reviewed on a set cycle."],
"POL-MED-01":["Only workers trained and assessed as competent administer or assist with medication.","Medication charts (FRM-MED-01) are current, complete and followed exactly.","PRN medication is given only per WIN-MED-01 and the participant's plan.","Every medication error or near miss is an incident: reported, recorded and learned from.","Medication is stored and disposed of safely."],
"POL-MTM-01":["Mealtime needs are assessed and planned for each participant who needs support to eat or drink safely (FRM-MTM-01).","Texture modifications and positioning are followed exactly as planned.","Concerns about swallowing escalate promptly, including to PRO-HID-03 where dysphagia is assessed.","Workers who support mealtimes are trained for it."],
"POL-WST-01":["Waste, including clinical waste, is handled, stored and disposed of safely.","Standard infection control precautions apply across all services.","Jurisdictional waste and infection control requirements are identified and met."],
"POL-WHS-01":["Health and safety duties are owned from the top and resourced properly.","Workers are consulted on things that affect their health and safety.","Hazards, injuries and near misses are reported and acted on - psychosocial hazards included.","WHS obligations are managed alongside, never instead of, participant safety."],
"POL-HID-01":["High intensity supports are delivered only by workers trained and assessed against the HIDPA skills descriptors.","Training and assessment involve an appropriately qualified health practitioner, recorded in REG-HID-01.","Each participant receiving high intensity supports has a current health support plan (FRM-HID-01).","Escalation pathways to health practitioners are defined and known.","Competence is reassessed on a set cycle and after any incident."],
"POL-BSP-01":["We practise positive behaviour support and work to reduce and eliminate restrictive practices.","A regulated restrictive practice is used only when authorised, in a current behaviour support plan, as a last resort, least restrictive, for the shortest time.","Every use is recorded (FRM-BSP-01) and reported to the Commission as required, including monthly reporting.","Behaviour support plans are implemented as written, by trained workers, and reviewed.","Unauthorised use of a restrictive practice is a reportable incident."],
"POL-ECS-01":["Our early childhood supports are family-centred, inclusive and evidence-informed.","A key worker approach coordinates supports around the child and family.","Supports build family and community capacity and happen in natural settings where possible.","We measure outcomes that matter to the child and family."],
"POL-SCO-01":["The participant's interests come first in every coordination decision.","Conflicts of interest - especially recommending our own services - are declared, recorded and managed.","Options presented to participants are genuine and documented.","We support participants to understand and direct their own supports."],
"POL-SDA-01":["SDA dwellings are enrolled, and kept compliant with, the SDA rules and design requirements.","Tenancy rights are respected; SDA and support provision conflicts are declared and managed.","Service agreements meet the SDA module requirements.","Dwelling condition and compliance are tracked in REG-SDA-01."],
"POL-SIL-02":["A SIL house is the participant's home first; safeguards protect without controlling.","Home risks are assessed with participants, respecting dignity of risk (PRO-SIL-02).","Concerns about safety, abuse or neglect escalate immediately under POL-SGD-01 and the incident system.","Participants shape house rules and routines."],
"POL-SIL-03":["Every SIL house has clear practice governance: named supervision, planned rosters, recorded handovers.","House-level incidents, complaints and risks are visible to management, not just to the house.","Worker training specific to each participant's needs is tracked and current.","Practice in each house is reviewed on a set cycle against the SIL indicators (QI Guidelines s 72D)."],
}

PSTEPS = {
"PRO-INC-01":[("Any worker","Make the participant safe; get medical help if needed","- ; immediately"),
 ("Any worker","Tell the Service Manager what happened","Verbal + FRM-INC-01 started ; same shift"),
 ("Service Manager","Complete FRM-INC-01 with the worker; support the participant and involve their chosen supporters","FRM-INC-01 ; within 24 hours"),
 ("Quality Manager","Enter the incident in REG-INC-01; classify severity; assess whether it is reportable","REG-INC-01 ; same business day"),
 ("Quality Manager","If reportable or unsure - follow PRO-INC-02 now","Commission notification record"),
 ("Quality Manager","Investigate cause; record corrective actions","REG-QMS-01 entry"),
 ("Service Manager","Close the loop with the participant and workers involved","Note on FRM-INC-01")],
"PRO-INC-02":[("Quality Manager","Confirm the incident is (or may be) a reportable incident under the Incident Rules","Assessment noted on FRM-INC-01"),
 ("Quality Manager","Notify the Commission within the statutory window - 24 hours for the most serious categories, with fuller detail within 5 business days; unauthorised restrictive practice within 5 business days. CONFIRM current categories and windows against IMRI (F2018L00633) before approving this procedure","Commission portal notification ; statutory"),
 ("Quality Manager","Record the notification reference in REG-INC-01","REG-INC-01 updated"),
 ("CEO","Oversee required follow-up, investigation and any Commission directions","Investigation record"),
 ("Quality Manager","Keep the participant informed and supported throughout","Notes on FRM-INC-01")],
"PRO-GOV-02":[("Any manager","Identify that a notifiable change or event has occurred or is planned (ownership, key personnel, scale, adverse events)","Note to CEO ; immediately"),
 ("CEO","Confirm the notification duty and the deadline that applies - the 2026 Rules SHORTENED several windows; confirm current timeframes against the amended PRPS rr 13-13A before approval","- ; statutory"),
 ("CEO","Notify the Commission through the required channel within the window","Notification record"),
 ("Quality Manager","File the notification and any Commission response with registration records","Registration file"),
 ("CEO","Review whether the change triggers other updates (scope, documents, insurances)","REG-QMS-01 entry if needed")],
"PRO-FBK-01":[("Any worker","Receive feedback or a complaint in any form; offer support and an advocate","WIN-FBK-01 ; at the time"),
 ("Quality Manager","Acknowledge the complaint promptly and record it","FRM-FBK-01 + REG-FBK-01"),
 ("Quality Manager","Assess seriousness; check whether it is also an incident","Cross-reference to REG-INC-01 if so"),
 ("Quality Manager","Resolve with procedural fairness - hear everyone affected","Resolution note"),
 ("Quality Manager","Tell the complainant the outcome and their external options, including the NDIS Commission","Outcome letter/record"),
 ("Quality Manager","Log improvements arising","REG-QMS-01")],
"PRO-SGD-01":[("Any worker","Act immediately on any sign of abuse, neglect or exploitation - safety first, 000 if needed","- ; immediately"),
 ("Any worker","Report to the Service Manager the same day; never investigate alone","Verbal + FRM-INC-01"),
 ("Quality Manager","Treat as an incident; assess reportability - most safeguarding matters are reportable","PRO-INC-02 pathway"),
 ("Service Manager","Support the participant: safety, advocacy, information their way","Support notes"),
 ("CEO","Oversee response incl. any worker stand-downs and external referrals","Decision record")],
"PRO-MED-01":[("Service Manager","Confirm the worker is assessed competent and the chart (FRM-MED-01) is current before any administration","REG-HRM-02 check"),
 ("Worker","Check right person, medication, dose, route, time against the chart","FRM-MED-01 signed each time"),
 ("Worker","Record administration immediately; record refusals and reasons","FRM-MED-01"),
 ("Worker","Treat any error or near miss as an incident - report the same shift","FRM-INC-01"),
 ("Service Manager","Review charts and errors on a set cycle","Chart audit note")],
"PRO-HRM-01":[("HR Manager","Screen before start: verify NDIS Worker Screening Check for risk-assessed roles; verify qualifications","FRM-HRM-01 + REG-HRM-01"),
 ("HR Manager","Collect signed Code of Conduct acknowledgement","FRM-HRM-02"),
 ("Service Manager","Induct on this suite, safeguarding, incidents and the participant's plans","Induction record in REG-HRM-02"),
 ("HR Manager","Set supervision and probation checkpoints","Supervision schedule"),
 ("HR Manager","Diarise screening expiry and re-checks","REG-HRM-01")],
"PRO-SIL-01":[("House Supervisor","Learn how each participant prefers to make decisions, and who they want involved","FRM-SIL-01 started"),
 ("Worker","Offer real choices in daily life; give information the participant's way; allow time","Daily practice"),
 ("House Supervisor","Record significant decisions and the support given - not to control, to evidence support","FRM-SIL-01"),
 ("Service Manager","Review decision-support records for patterns of substitute decision-making","Review note"),
 ("House Supervisor","Escalate where a participant's decision is being overridden without lawful basis","POL-SGD-01 pathway")],
"PRO-BSP-02":[("Service Manager","Confirm any regulated restrictive practice is authorised and in a current behaviour support plan before use","BSP + authorisation on file"),
 ("Worker","Use only as the plan describes: last resort, least restrictive, shortest time","FRM-BSP-01 each use"),
 ("Service Manager","Record every use in REG-BSP-01 and report through the Commission's monthly online reporting","Monthly report record ; per RPBS"),
 ("Quality Manager","Treat any unauthorised use as a reportable incident - PRO-INC-02 immediately","REG-INC-01 + notification"),
 ("Service Manager","Feed usage data into BSP review with the practitioner","Review note")],
}

WSTEPS = {
"WIN-INC-01":["Keep the participant safe. Move away from danger. Call 000 if anyone needs urgent help.","Stay calm and stay with the participant if you can.","Tell your Service Manager before your shift ends - phone, do not wait for email.","Write down what you saw while it is fresh: what happened, when, who was there.","Start the Incident Report Form (FRM-INC-01) with your manager.","Do not discuss the incident outside the team.","Ask for support if you are affected - that is what the debrief is for."],
"WIN-FBK-01":["Thank the person - feedback is welcome here.","Listen. Do not defend or explain yet.","Write down their words as close as you can.","Ask how they would like it fixed, and if they want an advocate.","Give it to the Quality Manager today using FRM-FBK-01.","Never treat anyone differently for complaining."],
"WIN-MED-01":["Check the chart: is this PRN authorised, and do the conditions apply right now?","Check right person, medication, dose, route, time.","Give the medication and watch for the effect the chart says to expect.","Record it on FRM-MED-01 immediately, with the reason.","If in doubt at any point - do not give it. Call your Service Manager.","Anything unexpected: treat as an incident and report this shift."],
}

REGCOLS = {
"REG-INC-01":[("Incident ID","auto number","Stable reference"),("Date of incident / date recorded","dates","Timeliness is itself audited"),("Participant ref","ID, not full name","Privacy-minimised link"),("Summary","short text","Retrieval"),("Severity","minor / moderate / major","Trends"),("Reportable?","yes / no","Statutory pathway split"),("Notified to Commission (date)","date","Deadline evidence (PRO-INC-02)"),("Corrective action ref","REG-QMS-01 ID","Learning loop"),("Status","open / closed","Nothing left hanging")],
}

AGRSEC = ["Parties and start date","Supports to be provided, and how often","Costs and how payment works","Your rights, our responsibilities","How we change this agreement together","How either of us can end it, and what notice applies","Signatures - and a copy for you"]
SILAGR = ["Who lives here and who provides support (they can be different agreements)","Your home: tenancy or occupancy terms, in plain language","Your supports: what, when, by whom","Costs, split clearly between housing and supports","How house decisions are made together","Changing or ending either agreement - your protections","Signatures - and Easy Read copies (QI Guidelines s 72E)"]
STASEC = ["Welcome and how to use this handbook","Your rights (and what you can expect from us)","Choosing, changing and directing your supports","Service agreements and costs, in plain words","How to give feedback or make a complaint - including straight to the NDIS Commission","Staying safe: what happens if something goes wrong","Your privacy and your information","Advocates, interpreters and getting extra support"]
PLNSEC = ["Purpose and scope","Roles and contact tree","Scenarios planned for","Participant-specific arrangements","Response actions","Recovery and return to normal supports","Testing, drills and review record"]

def purpose(d):
    stds = "; ".join(f"{s} {nm(s)}" for s in d["imp"][:2])
    generic = {
     "Policy": f"This policy states [Provider Name]'s commitments for {d['title'].lower().replace(' policy','')}, meeting {stds}.",
     "Procedure": f"This procedure sets out how, who and when for {d['title'].lower().replace(' procedure','')}.",
     "Work Instruction": "The one-page frontline version: exactly what you do, right now.",
     "Form": "What we capture, the same way every time - completed copies become audit evidence.",
     "Register": "The running log that proves this process operates over time. Auditors read registers first.",
     "Plan": "A standing plan kept current and tested - the difference between a document and a capability.",
     "Agreement": "The written agreement between the participant and [Provider Name], in plain language.",
     "Handbook": "The participant-facing guide to their rights and our service, with an Easy Read companion.",
    }
    return generic.get(d["type"], generic["Policy"])

def genpsteps(d):
    uses = [to for t, to, n in OUT.get(d["id"], []) if t == "USES"]
    recs = []
    for u in uses: recs += [to for t, to, n in OUT.get(u, []) if t == "RECORDS_TO"]
    frm = uses[0] if uses else "the relevant form"
    reg = recs[0] if recs else "the relevant register"
    return [("Responsible role","Confirm the trigger applies and gather what is needed","-"),
     ("Responsible role", f"Carry out the task as this procedure's parent policy commits, recording on {frm}", f"{frm}"),
     ("Responsible role", f"Log the completed record in {reg}", f"{reg}"),
     ("Manager","Check completeness and escalate anything unresolved","Escalation note"),
     ("Owner","Review samples on a set cycle and log improvements","REG-QMS-01")]

def body_sections(d):
    """Returns list of (heading, kind, payload). kind: p (text), n (numbered), t (steps table), c (columns table), b (box)."""
    i, ty = d["id"], d["type"]; sec = []
    sec.append(("Purpose","p", purpose(d)))
    if ty == "Policy":
        sec.append(("Scope","p","Applies to all workers, key personnel, volunteers and contractors of [Provider Name], across the services named in our registration. [Adjust if narrower.]"))
        sec.append(("Policy statements","n", S.get(i) or ["We meet the requirements of " + "; ".join(nm(s) for s in d["imp"]) + " in everything this policy covers.","We keep records that show how.","Workers are trained on this policy and supported to follow it.","We review this policy on schedule and when the law or our services change.","Anyone can raise a concern under this policy without fear."]))
        if d["ez"] or i in ("POL-INC-01","POL-SGD-01","POL-RGT-03"):
            sec.append(("What this means for participants","b","[One short paragraph, first person, in the style of the SIL participant statements. Example for incidents: If something goes wrong, the people supporting me act quickly to keep me safe. They tell me what happened, listen to me, and involve the people I choose.]"))
        sec.append(("Roles and responsibilities","p", f"Owner: {d['own']}. All managers apply this policy in their services; all workers follow it and report concerns. [Add roles specific to your structure.]"))
    elif ty == "Procedure":
        sec.append(("When this procedure starts","p","[The trigger, in one sentence a frontline worker recognises.]"))
        sec.append(("Steps","t", PSTEPS.get(i) or genpsteps(d)))
        sec.append(("Escalation","p","If a step cannot be completed, or severity increases: escalate to the owner, then the CEO. Never leave a statutory deadline unowned."))
    elif ty == "Work Instruction":
        sec.append(("When to use this","p","[One sentence.]"))
        sec.append(("What you do","n", WSTEPS.get(i) or ["Confirm the task and the participant's plan.","Do the task as trained - if anything differs from the plan, stop.","Record it straight away on the linked form.","Tell your manager anything unusual.","Stop and escalate if you are unsure at any point."]))
        sec.append(("Stop and escalate if","b","[2-4 red flags for this task. When in doubt - report anyway.]"))
    elif ty in ("Form","Agreement"):
        sec.append(("Privacy notice (printed on the form)","b", PRIVACY))
        if ty == "Agreement":
            sec.append(("Sections","n", SILAGR if i == "AGR-SIL-01" else AGRSEC))
        else:
            sec.append(("Form sections","n", ["A. Details - date, time, location, service","B. People - participant ref, workers, others involved","C. " + d["title"].replace(" Form","").replace(" Record","") + " - the substance this form exists to capture [define fields]","D. Assessment / manager review [where applicable]","E. Sign-off - names, signatures, date entered in the linked register"] if i != "FRM-INC-01" else ["A. The incident - date and time; location; what happened; near miss? (Y/N)","B. People - participant(s) involved; workers present; witnesses","C. Immediate response - actions taken; medical help needed?; participant informed and supported?","D. Assessment (manager) - severity (minor/moderate/major); reportable? (yes / no / unsure - if yes or unsure, go to PRO-INC-02 now)","E. Sign-off - worker and manager signatures; date entered in REG-INC-01"]))
        sec.append(("Completion and retention","p","[Who completes which sections, by when; where originals live; retention per the instrument cited above - cite, do not guess.]"))
    elif ty == "Register":
        cols = REGCOLS.get(i) or [("Ref","auto number","Stable reference"),("Date","date","Timeliness"),("Linked record","form/doc ID","The evidence trail"),("Summary","short text","Retrieval"),("Owner","role","Accountability"),("Status","open / closed","Nothing left hanging"),("Next action / review","date + note","Keeps it live")]
        sec.append(("Column specification","c", cols))
        sec.append(("Rhythm","p", f"Maintained by the {d['own']}. Entries within the timeframes of the feeding procedure; reviewed on a set cycle; overdue items and trends reported upward."))
        sec.append(("Audit view","p","An auditor samples rows and traces each one back to its completed form and forward to actions taken. A current, complete register is the strongest single evidence this process is real; an empty one next to a perfect policy is a red flag."))
    elif ty == "Plan":
        sec.append(("Plan sections","n", PLNSEC))
        sec.append(("Keeping it real","p","A plan that is never tested is a document, not a capability. Record every drill and activation, and review after each."))
    elif ty == "Handbook":
        sec.append(("Contents","n", STASEC))
        sec.append(("Accessibility","p","Written to plain-English rules (short sentences, everyday words); an Easy Read companion is required before publication."))
    if d["ez"]:
        sec.append(("Easy Read","b","An Easy Read companion of this document is flagged as required in the register - produce before participant-facing use."))
    sec.append(("Review triggers","p","Review at the due date, and earlier if: any instrument in the links table is amended; a major audit finding or serious incident touches this document; our registration scope changes."))
    return sec

# ---------------- renderers ----------------
def slug(t): return re.sub(r"[^A-Za-z0-9]+","-",t).strip("-")

def render_md(d):
    L = [f"# {d['title']}", "", f"**{d['type']} · {d['id']} · DRAFT v0.1**", "", f"> {BANNER}", ""]
    L += ["## Document control","", "| Field | Entry |","|---|---|",
          f"| Document ID / Type | {d['id']} · {d['type']} |",
          "| Version / Status | 0.1 · Draft |",
          f"| Owner (role) | {d['own']} |",
          "| Approved by / Effective from | [role] · [date] |",
          f"| Review cycle | {d['rv']} year(s), or on any trigger below |",
          f"| Applies to | {d['applies']} · Priority {d['priority']} |",""]
    L += ["## Compliance links","", "| Link type | Plain English | Linked to |","|---|---|---|"]
    for lab, gl, tgts in link_rows(d):
        tt = "; ".join(f"{x} {t}{e}" for x, t, e in tgts)
        L.append(f"| {lab} | {gl} | {tt} |")
    L.append("")
    for h, kind, pay in body_sections(d):
        L += [f"## {h}",""]
        if kind == "p": L += [pay,""]
        elif kind == "b": L += [f"> {pay}",""]
        elif kind == "n": L += [f"{j+1}. {s}" for j, s in enumerate(pay)] + [""]
        elif kind == "t":
            L += ["| # | Who | What they do | Record / deadline |","|---|---|---|---|"]
            L += [f"| {j+1} | {w} | {a} | {r} |" for j,(w,a,r) in enumerate(pay)]; L.append("")
        elif kind == "c":
            L += ["| Column | Type / values | Why |","|---|---|---|"]
            L += [f"| {c} | {t} | {y} |" for c, t, y in pay]; L.append("")
    L += ["## Version history","","| Version | Date | Change | Approved |","|---|---|---|---|",
          f"| 0.1 | {GEN} | Generated scaffold from the Rise graph | - |",""]
    return "\n".join(L)

def render_html(d):
    def a(x, t, e=""):
        h = "#library" if isdoc(x) else "#graph"
        return f'<a class="idlink" data-node="{esc(x)}" href="{h}">{esc(x)}</a> {esc(t)}{esc(e)}'
    H = [f'<p class="meta">{esc(d["type"])} · {esc(d["id"])} · <span class="stamp draft">Draft v0.1 - scaffold</span></p>']
    H.append(f'<h1 style="font:700 24px Spectral,serif;margin:6px 0 10px">{esc(d["title"])}</h1>')
    H.append(f'<div class="watch" style="border-left-color:#a06a00"><p>{esc(BANNER)}</p></div>')
    H.append('<h2 class="dh">Document control</h2><table class="doc"><tbody>')
    for k, v in [("Document ID / Type", f"{d['id']} · {d['type']}"),("Version / Status","0.1 · Draft"),
                 ("Owner (role)", d["own"]),("Review cycle", f"{d['rv']} year(s), or on triggers"),
                 ("Applies to", f"{d['applies']} · Priority {d['priority']}")]:
        H.append(f"<tr><td><strong>{esc(k)}</strong></td><td>{esc(v)}</td></tr>")
    H.append("</tbody></table>")
    H.append('<h2 class="dh">Compliance links</h2><table class="doc"><tbody>')
    for lab, gl, tgts in link_rows(d):
        tt = "; ".join(a(x, t, e) for x, t, e in tgts)
        H.append(f'<tr><td style="white-space:nowrap"><span class="mono" style="font-size:11px;font-weight:600">{esc(lab)}</span><div class="meta">{esc(gl)}</div></td><td>{tt}</td></tr>')
    H.append("</tbody></table>")
    for h, kind, pay in body_sections(d):
        H.append(f'<h2 class="dh">{esc(h)}</h2>')
        if kind == "p": H.append(f"<p>{esc(pay)}</p>")
        elif kind == "b": H.append(f'<div class="fact">{esc(pay)}</div>')
        elif kind == "n": H.append("<ol>" + "".join(f"<li>{esc(s)}</li>" for s in pay) + "</ol>")
        elif kind == "t":
            H.append('<table class="doc"><tbody><tr><td><strong>#</strong></td><td><strong>Who</strong></td><td><strong>What they do</strong></td><td><strong>Record / deadline</strong></td></tr>')
            H += [f"<tr><td>{j+1}</td><td>{esc(w)}</td><td>{esc(x)}</td><td>{esc(r)}</td></tr>" for j,(w,x,r) in enumerate(pay)]
            H.append("</tbody></table>")
        elif kind == "c":
            H.append('<table class="doc"><tbody><tr><td><strong>Column</strong></td><td><strong>Type / values</strong></td><td><strong>Why</strong></td></tr>')
            H += [f"<tr><td>{esc(c)}</td><td>{esc(t)}</td><td>{esc(y)}</td></tr>" for c, t, y in pay]
            H.append("</tbody></table>")
    H.append(f'<p class="meta">Version 0.1 · {GEN} · generated from the Rise graph. Round-trip rule: the graph is authoritative; this header regenerates from it.</p>')
    return "".join(H)

os.makedirs("/home/claude/suite", exist_ok=True)
dh = {}
for d in rb.DOCS:
    md = render_md(d)
    open(f"/home/claude/suite/{d['id']}_{slug(d['title'])[:60]}.md","w").write(md)
    dh[d["id"]] = render_html(d)
json.dump(dh, open("/home/claude/docs_html.json","w"))
print("suite:", len(rb.DOCS), "documents |", sum(len(v) for v in dh.values())//1024, "KB html")
