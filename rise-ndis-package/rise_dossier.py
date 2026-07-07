#!/usr/bin/env python3
"""Generates rise-dossier.html - a single-file, browser-viewable dossier of the entire
Rise NDIS dataset with live links to the Federal Register of Legislation and NDIS
Commission. Static snapshot; regenerate after editing rise_build.py."""
import html, json
import rise_build as rb

esc = html.escape
FRL = {"ACT":"C2013A00020","PRPS":"F2018L00631","IMRI":"F2018L00633","CMR":"F2018L00634",
 "RPBS":"F2018L00632","WSR":"F2018L00887","COC":"F2018L00629","SDAC":"F2018L00627",
 "PD":"F2018L00628","QI":"F2018N00041","AQA":"F2018N00114","AQAR25":"F2025L01383"}
VSTAMP = {"V":("verified","Verified — FRL / Commission, 5 Jul 2026"),
 "C":("corrob","Corroborated — confirm before external use"),
 "T":("check","Training knowledge — confirm vs compilation"),
 "D":("draft","Draft source — confirm vs made 2026 Rules")}

def stamp(v):
    cls, label = VSTAMP.get(v, ("check", v))
    return f'<span class="stamp {cls}">{esc(label)}</span>'

def frl_link(key):
    if key in FRL:
        i = FRL[key]
        return f'<a class="cite" href="https://www.legislation.gov.au/{i}/latest" target="_blank" rel="noopener">{i}</a>'
    return '<span class="cite dim">FRL id TBC</span>'

# ---------- legislation rows ----------
leg_rows = ""
for k, title, kind, notes, v, role in rb.LEG:
    leg_rows += f'''<tr data-kind="{esc(kind)}"><td><a class="mono id idlink" href="#graph" data-node="{esc(k)}">{esc(k)}</a><br>{frl_link(k)}</td>
<td><strong>{esc(title)}</strong><div class="meta">{esc(kind)} · {esc(role)}</div><div class="note">{esc(notes)}</div></td>
<td>{stamp(v)}</td></tr>\n'''

# ---------- standards rows ----------
std_rows = ""
for sid, mod, div, name, v in rb.STD:
    cit = rb.CIT.get(sid, ""); qi = rb.QIREF.get(sid, "")
    qcell = f'<span class="mono cite">{esc(cit)}</span>' + (f'<br><span class="mono cite dim">indicators: QI {esc(qi)}</span>' if qi else "")
    std_rows += f'''<tr data-mod="{esc(mod)}"><td><a class="mono id idlink" href="#graph" data-node="{esc(sid)}">{esc(sid)}</a></td>
<td><strong>{esc(name)}</strong><div class="meta">{esc(div)}</div></td>
<td>{qcell}</td><td>{stamp(v)}</td></tr>\n'''
mod_chips = "".join(f'<button class="chip" data-chip="{esc(m[0])}">{esc(m[0])}</button>' for m in rb.MODULES)

# ---------- document rows ----------
doc_rows = ""
clusters = sorted({x["cluster"] for x in rb.DOCS})
dtypes = sorted({x["type"] for x in rb.DOCS})
for x in rb.DOCS:
    outs = rb.outg.get(x["id"], []); ins = rb.inc.get(x["id"], [])
    links = ""
    if outs or ins:
        li = "".join(f"<li>{esc(l)}</li>" for l in outs) + "".join(f"<li class='dim'>{esc(l)}</li>" for l in ins)
        links = f"<details><summary>{len(outs)+len(ins)} typed links</summary><ul class='mono links'>{li}</ul></details>"
    ez = ' · <span class="ez">Easy Read</span>' if x["ez"] else ""
    doc_rows += f'''<tr data-type="{esc(x["type"])}" data-cluster="{esc(x["cluster"])}" data-pri="{esc(x["priority"])}">
<td><a class="mono id idlink" href="#library" data-node="{esc(x["id"])}">{esc(x["id"])}</a><div class="meta">{esc(x["priority"])}</div></td>
<td><strong>{esc(x["title"])}</strong><div class="meta">{esc(x["type"])} · {esc(x["cluster"])} · applies: {esc(x["applies"])}{ez}</div>
<div class="note">Implements <span class="mono">{esc("; ".join(x["imp"]))}</span> · Owner: {esc(x["own"])} · Review: {x["rv"]} yr</div>{links}</td></tr>\n'''

cl_opts = "".join(f'<option>{esc(c)}</option>' for c in clusters)
ty_opts = "".join(f'<option>{esc(t)}</option>' for t in dtypes)

# ---------- graph explorer data ----------
gnodes = {}
for k, title, kind, notes, v, role in rb.LEG: gnodes[k] = dict(t=title, k="Instrument", l="shared")
gnodes["NDIS-PS"] = dict(t="NDIS Practice Standards", k="Framework", l="shared")
for m in rb.MODULES: gnodes[m[0]] = dict(t=m[1], k="Module", l="shared")
for s in rb.STD: gnodes[s[0]] = dict(t=s[3], k="Standard", l="shared")
for x in rb.DOCS: gnodes[x["id"]] = dict(t=x["title"], k=x["type"], l="tenant")
TN = {
 "Act":("shared","The root of authority - the NDIS Act 2013.","kind, jurisdiction, FRL id, status, bitemporal pair"),
 "Rules / Guidelines":("shared","Delegated legislation made under the Act.","kind, FRL id, compilation no, status, bitemporal pair"),
 "Amending instrument":("shared","An Act or Rules that changes another instrument - the fan-out trigger.","target instrument, commencement dates"),
 "Provision":("shared","A Part, Schedule or clause inside an instrument. Planned import.","native citation, provision kind"),
 "Framework":("shared","A quality framework as a whole - NDIS Practice Standards.","regulator, audit scheme"),
 "Module":("shared","Core, Verification, M1-M5, M2A, SIL - switches on by what you deliver.","applies-when, commencement"),
 "Standard":("shared","The auditable requirement (edge taxonomy calls it Requirement).","division, citation, outcome ref, participant-statement ref"),
 "Quality Indicator":("shared","What auditors look for under a standard. Planned import.","indicator ref"),
 "Organisation":("tenant","The provider - the tenant root.","registration no, registration groups, audit pathway"),
 "Registration Scope":("tenant","What the provider is registered for - drives gap detection.","modules in scope, effective dates"),
 "Site / Home":("tenant","A physical service setting, e.g. a SIL house.","site kind"),
 "Policy":("tenant","The commitments made against standards - the why.","doc type, version, owner role, review cycle, Easy Read flags"),
 "Procedure":("tenant","How, who, when - step by step.","as Policy"),
 "Work Instruction":("tenant","One task, one page, frontline voice.","as Policy"),
 "Form / Agreement":("tenant","Captures each event the same way, every time.","as Policy"),
 "Register":("tenant","The running log - the evidence auditors read first.","as Policy"),
 "Plan / Handbook":("tenant","Standing plans and participant-facing packs.","as Policy"),
 "Role":("tenant","Accountable role, not a person - survives turnover.","role kind"),
 "Person":("tenant","Only where worker-level evidence is needed. PII-minimised.","screening ref, expiry"),
 "Training / Qualification":("tenant","Competency targets, e.g. HIDPA skills.","delivered-by kind"),
 "Risk":("tenant","Entry in the risk register.","category, current and target rating"),
 "Control":("tenant","A mitigation - often is a document.","control kind"),
 "Evidence":("tenant","Proof something happened. Immutable once frozen.","evidence kind, generated-by, frozen-at"),
 "Audit":("tenant","Certification, verification, mid-term or internal.","audit kind, auditor"),
 "Finding":("tenant","Conformity or non-conformity from an audit.","severity"),
 "Improvement Action":("tenant","Closes the loop on a finding.","due date, closed-at"),
}
TE = [
 ["Rules / Guidelines","MADE_UNDER","Act",""],
 ["Amending instrument","AMENDS","Rules / Guidelines","v0.4 candidate - today RELATES_TO + note"],
 ["Provision","PART_OF","Rules / Guidelines",""],
 ["Framework","PUBLISHED_IN","Rules / Guidelines",""],
 ["Module","PART_OF","Framework",""],
 ["Standard","PART_OF","Module",""],
 ["Quality Indicator","PART_OF","Standard",""],
 ["Standard","MAPS_TO","Standard","symmetric cross-framework crosswalk: strength, rationale, score 0-10"],
 ["Policy","IMPLEMENTS","Standard",""],
 ["Policy","REFERENCES","Rules / Guidelines","v0.4 candidate - today RELATES_TO + note"],
 ["Procedure","OPERATIONALISES","Policy",""],
 ["Work Instruction","OPERATIONALISES","Procedure",""],
 ["Procedure","USES","Form / Agreement",""],
 ["Form / Agreement","RECORDS_TO","Register",""],
 ["Evidence","GENERATED_BY","Register",""],
 ["Evidence","EVIDENCES","Standard",""],
 ["Audit","ASSESSES","Standard",""],
 ["Finding","RAISED_IN","Audit",""],
 ["Finding","CITES","Evidence",""],
 ["Finding","CONCERNS","Policy","target may be any governed object"],
 ["Improvement Action","ADDRESSES","Finding",""],
 ["Control","MITIGATES","Risk",""],
 ["Policy","OWNED_BY","Role","applies to any document"],
 ["Procedure","PERFORMED_BY","Role",""],
 ["Role","REQUIRES","Training / Qualification",""],
 ["Person","assigned to","Role","assignment record, not a taxonomy edge"],
 ["Registration Scope","scopes gap detection to","Module","informal - applicability logic"],
 ["Organisation","has","Registration Scope","informal"],
 ["Organisation","operates","Site / Home","informal"],
]
tnodes = {k: dict(t=v[1], k="Type", l=v[0], a=v[2]) for k, v in TN.items()}
GRAPH = json.dumps(dict(n=gnodes, e=[list(e) for e in rb.E], tn=tnodes, te=TE), separators=(",", ":")).replace("</", "<\\/")

DOCSH = json.load(open("/home/claude/docs_html.json"))
DOCSJSON = json.dumps(DOCSH, separators=(",",":")).replace("</", "<\\/")
doc_opts = "".join(f'<option value="{esc(x["id"])}">{esc(x["title"][:60])}</option>' for x in rb.DOCS)

SOURCES = [
 ("Tier 1 - primary law and the regulator", [
  ("Federal Register of Legislation - PRPS Rules 2018 full table of contents (compilation C04, 15 Nov 2021). The keystone: every schedule, clause citation and official heading.","https://www.legislation.gov.au/F2018L00631/latest/text"),
  ("FRL series pages for all NDIS instruments in the Legislation section (links on each row).","https://www.legislation.gov.au/"),
  ("NDIS Commission - reform hub: SIL standards from 1 Jul 2026; mandatory SIL + platform registration; 2026 amendment instruments; tightened notification duties.","https://www.ndiscommission.gov.au/about-us/ndis-commission-reform-hub"),
  ("NDIS Commission - legislation, rules and policies index (the instrument census).","https://www.ndiscommission.gov.au/about-us/legislation-rules-and-policies"),
  ("NDIS Commission - types of audits: 14-day / 28-day report windows, audit conduct.","https://www.ndiscommission.gov.au/provider-registration/apply-registration/types-audits"),
  ("Dept of Health, Disability and Ageing - 2026 NDIS Act amendments: Integrity and Safeguarding Act passed 1 Apr, assent 8 Apr 2026; Securing the NDIS Bill introduced 14 May 2026.","https://www.health.gov.au/our-work/ndis-legislation-changes/amendments"),
  ("NDIS (ministerial release, 1 Apr 2026) - new offences and penalties incl. unregistered provision of registration-required supports.","https://ndis.gov.au/news/11506-parliament-passes-tough-new-laws-protect-ndis-fraudsters-predators-and-shonks"),
 ]),
 ("Tier 2 - standards bodies and comparators", [
  ("OASIS Akoma Ntoso / LegalDocML v1.0 (OASIS Standard, 29 Aug 2018) - the open standard for machine-readable legislation; revision scheduled for approval late Jul 2026.","https://www.oasis-open.org/news/announcements/akoma-ntoso-v1-0-akn-oasis-standard-published/"),
  ("legislation.gov.uk API documentation - the benchmark open register API (bulk access, open licences, CORS).","https://legislation.github.io/data-documentation/api/overview.html"),
 ]),
 ("Tier 3 - professional secondary (corroboration only, never sole basis for a Verified stamp)", [
  ("MinterEllison (Apr 2026) - IS26 commencement split and penalty analysis.","https://www.minterellison.com/articles/ndis-legislative-amendments"),
  ("Team DSC (Apr 2026) - whistleblower mechanics and information-notice compression.","https://teamdsc.com.au/resources/what-you-need-to-know-about-the-ndis-amendment-integrity-and-safeguarding-bill-2026/"),
  ("Michael West Media (Jun 2026) - registration statistics; journalistic, single-sourced - do not republish without a primary source.","https://michaelwest.com.au/the-54b-question-ndis-compliance-looms-247000-providers-yet-to-be-registered/"),
 ]),
]
src_html = ""
for tier, items in SOURCES:
    lis = "".join(f'<li>{esc(d)} <a class="cite" href="{u}" target="_blank" rel="noopener">source</a></li>' for d, u in items)
    src_html += f'<div class="fact"><b>{esc(tier)}</b><ul class="srcs">{lis}</ul></div>'
src_html += '<div class="watch"><h3>Negative findings - searched for, not found</h3><p>No public API documentation for legislation.gov.au (the US and UK register APIs are different systems); no post-2026 PRPS compilation published yet; FRL ids for two 2019/2020 Commission guidelines not yet located; support-coordination mandatory-registration timing unresolved. Full trace and access dates: rise-sources.md.</p></div>'

node_opts = "".join(f'<option value="{esc(i)}">{esc(d["t"][:60])}</option>' for i, d in gnodes.items())

nV = sum(1 for s in rb.STD if s[4]=="V"); nD = sum(1 for s in rb.STD if s[4]=="D")
counts = dict(docs=len(rb.DOCS), stds=len(rb.STD), leg=len(rb.LEG), edges=len(rb.E), v=nV, d=nD)

WATCH = [
 ("NDIS Amendment (Securing the NDIS for Future Generations) Bill 2026","Third tranche of NDIS Act reform, introduced to Parliament 14 May 2026. Not yet law - track passage and commencements.","https://www.health.gov.au/our-work/ndis-legislation-changes/amendments"),
 ("Mandatory registration expansion to 2030","SIL and platform providers mandatory from 1 Jul 2026; broader phased program flagged through 2030 (secondary reporting). Timing for other categories - including support coordination - unresolved; confirm before relying on it.",""),
 ("SIL (Module 5A) - PRPS clause pinpoints","RESOLVED on the indicators side: QI Guidelines compilation C03 (1 Jul 2026) consolidates Module 5A, ss 72B-72E - names verified. Still open: the PRPS Rules compilation remains C04 (2021), so SIL schedule/clause pinpoints in the Standards sheet stay TBC until the next PRPS compilation.","https://www.legislation.gov.au/F2018L00631/latest"),
 ("NDIS Practice Standards Review","Commission review of the Practice Standards under way; may reshape modules and introduce expectation statements. Any change fans out across this whole register.","https://www.ndiscommission.gov.au/about-us/ndis-commission-reform-hub"),
 ("Approved Quality Auditors Rules 2025 vs 2018 Scheme Guidelines","Both listed as current; the relationship (supplement or partial replacement) is unconfirmed. New AQA approvals are suspended during the reform program.","https://www.legislation.gov.au/F2025L01383/latest"),
 ("Quality Indicators import","The QI Guidelines 2018 (as amended for SIL) contain the indicators auditors actually assess - not yet imported into the graph. Next shared-data task.",""),
 ("Jurisdictional overlays","State/Territory NDIS worker screening schemes, WHS law, and child-safe requirements (relevant to Module 3) vary by jurisdiction and are represented only as adjacent placeholders.",""),
 ("Akoma Ntoso revision - late July 2026","A revision of the OASIS LegalDocML standard is scheduled for approval this month. Relevant to how Rise structures full-text legislative imports; adopt the new revision if ratified.","https://www.oasis-open.org/news/announcements/akoma-ntoso-v1-0-akn-oasis-standard-published/"),
 ("FRL programmatic access - unconfirmed","No public API documentation found for legislation.gov.au (the UK register's open API is the benchmark). Resolve by contacting the Office of Parliamentary Counsel; until then, integrate at page level with respectful caching.","https://legislation.github.io/data-documentation/api/overview.html"),
]
watch_rows = "".join(
    f'''<div class="watch"><h3>{esc(t)}</h3><p>{esc(d)}</p>{f'<a class="cite" href="{u}" target="_blank" rel="noopener">source / track here</a>' if u else ''}</div>'''
    for t, d, u in WATCH)

page = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rise · NDIS Regulatory Dossier — snapshot 5 July 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:wght@500;700;800&family=Public+Sans:wght@400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap" media="all" onerror="this.media='none'">
<style>
:root{--navy:#12284b;--navy2:#1d3a66;--bg:#eef1f2;--panel:#fff;--ink:#17202b;--mut:#5a6673;
--rule:#c9d1d6;--ok:#1e7a4f;--okbg:#e5f2ea;--amb:#8a5b00;--ambbg:#f6ecd6;--chk:#7a4a1e;--chkbg:#f3e7dc;}
*{box-sizing:border-box}html{scroll-behavior:smooth}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 "Public Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,system-ui,sans-serif}
.mast{background:var(--navy);color:#e9eef6;padding:40px 20px 28px}
.mast .wrap{max-width:1060px;margin:0 auto;display:flex;gap:28px;flex-wrap:wrap;align-items:flex-end;justify-content:space-between}
.eyebrow{font:600 12px/1 "Public Sans";letter-spacing:.22em;text-transform:uppercase;color:#9fb3d1;margin:0 0 10px}
h1{font:800 clamp(30px,4.5vw,44px)/1.08 Spectral,serif;margin:0;max-width:640px}
h1 em{font-style:italic;font-weight:500;color:#b9c9e2}
.stampbox{border:2px solid #8fa5c8;padding:12px 16px;font:600 12px/1.7 "IBM Plex Mono",monospace;
letter-spacing:.06em;color:#cdd9ec;text-transform:uppercase;transform:rotate(-1.2deg);white-space:nowrap}
.stampbox b{color:#fff}
nav{position:sticky;top:0;background:var(--navy2);z-index:9;box-shadow:0 2px 8px rgba(10,20,40,.25)}
nav .wrap{max-width:1060px;margin:0 auto;display:flex;flex-wrap:wrap}
nav a{color:#dbe4f2;text-decoration:none;font:600 13px/1 "Public Sans";letter-spacing:.04em;padding:14px 16px}
nav a:hover,nav a:focus-visible{background:rgba(255,255,255,.12);outline:none}
main{max-width:1060px;margin:0 auto;padding:12px 20px 80px}
section{margin-top:56px}
h2{font:700 26px/1.2 Spectral,serif;border-bottom:3px solid var(--navy);padding-bottom:8px;margin:0 0 6px}
.lede{color:var(--mut);max-width:72ch;margin:8px 0 18px}
.panel{background:var(--panel);border:1px solid var(--rule);border-radius:4px;padding:0;overflow:hidden}
table{width:100%;border-collapse:collapse;font-size:14.5px}
td{padding:12px 14px;border-top:1px solid var(--rule);vertical-align:top}
tr:first-child td{border-top:none}
.mono{font-family:"IBM Plex Mono",monospace}
.id{font-weight:600;font-size:13.5px;background:#eef2f7;border:1px solid #d5dde8;padding:2px 7px;border-radius:3px;white-space:nowrap}
.cite{font-family:"IBM Plex Mono",monospace;font-size:12.5px;color:var(--navy);text-decoration:none;border-bottom:1px dotted var(--navy)}
a.cite:hover{background:#e7edf6}
.cite.dim{color:var(--mut);border-bottom:none}
.meta{color:var(--mut);font-size:12.5px;margin-top:3px}
.note{font-size:13px;margin-top:6px;max-width:80ch}
.stamp{display:inline-block;font:600 10.5px/1.2 "IBM Plex Mono",monospace;letter-spacing:.05em;text-transform:uppercase;
border:1.5px solid;padding:4px 8px;border-radius:2px;white-space:normal;max-width:150px}
.stamp.verified{color:var(--ok);border-color:var(--ok);background:var(--okbg)}
.stamp.draft{color:var(--amb);border-color:var(--amb);background:var(--ambbg)}
.stamp.corrob,.stamp.check{color:var(--chk);border-color:var(--chk);background:var(--chkbg)}
.tools{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 12px;align-items:center}
input[type=search],select{font:14px "Public Sans";padding:9px 12px;border:1px solid var(--rule);border-radius:4px;background:#fff;min-width:200px}
input[type=search]:focus-visible,select:focus-visible,.chip:focus-visible,summary:focus-visible{outline:2px solid var(--navy);outline-offset:1px}
.chip{font:600 12.5px "IBM Plex Mono";padding:7px 11px;border:1px solid var(--rule);background:#fff;border-radius:3px;cursor:pointer}
.chip.on{background:var(--navy);color:#fff;border-color:var(--navy)}
.ladder{background:var(--panel);border:1px solid var(--rule);border-radius:4px;padding:22px 24px;font-size:15px}
.rung{display:flex;gap:14px;padding:9px 0;border-top:1px dashed var(--rule);align-items:baseline}
.rung:first-child{border-top:none}
.rung .mono{color:var(--navy);font-weight:600;font-size:12px;min-width:170px;text-transform:uppercase;letter-spacing:.05em}
.links{columns:1;font-size:12px;color:#3a4756;margin:6px 0 0;padding-left:18px}
.links .dim{color:#8792a0}
details summary{cursor:pointer;font-size:12.5px;color:var(--navy);margin-top:6px;font-weight:600}
.ez{color:var(--ok);font-weight:700;font-size:11.5px;letter-spacing:.04em;text-transform:uppercase}
.watch{background:var(--panel);border:1px solid var(--rule);border-left:4px solid var(--amb);border-radius:4px;padding:16px 18px;margin-bottom:12px}
.watch h3{margin:0 0 6px;font:700 17px Spectral,serif}
.watch p{margin:0 0 6px;font-size:14px;max-width:85ch}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}
.fact{background:var(--panel);border:1px solid var(--rule);border-radius:4px;padding:14px 16px;font-size:14px}
.fact b{font-family:"IBM Plex Mono";color:var(--navy)}
footer{border-top:3px solid var(--navy);margin-top:70px;padding:22px 20px;color:var(--mut);font-size:13px}
footer .wrap{max-width:1060px;margin:0 auto}
.gwrap{background:var(--panel);border:1px solid var(--rule);border-radius:4px}
#gsvg{width:100%;height:auto;display:block}
a.idlink{text-decoration:none;color:inherit;cursor:pointer}
a.idlink:hover,a.idlink:focus-visible{background:#dfe7f2;outline:none}
.gnode{cursor:pointer}
.gedge{stroke:#93a3b3;stroke-width:1.4;fill:none}
.gedge.in{stroke-dasharray:5 4}
.glab{font:600 9.5px "IBM Plex Mono";fill:#415061}
#glist ul{margin:6px 0 0;padding-left:18px;font:12px/1.6 "IBM Plex Mono";color:#3a4756;list-style:square}
#glist .dim{color:#8792a0}
#gchain .rung .mono{min-width:140px}
.srcs{margin:8px 0 0;padding-left:18px;font-size:13px}
.srcs li{margin-bottom:7px}
.gnode:focus{outline:none}
.gnode:focus rect,.gnode:focus-visible rect{stroke-width:3.2}
.dh{font:700 17px Spectral,serif;border-bottom:2px solid var(--rule);padding-bottom:4px;margin:20px 0 8px}
#dread table{margin:4px 0 10px}
#dread ol{padding-left:22px}
#dread ol li{margin-bottom:6px}
@media(max-width:640px){.rung .mono{min-width:110px}td{padding:10px}}
</style></head><body>

<header class="mast"><div class="wrap">
<div><p class="eyebrow">Rise · Compliance Knowledge Graph</p>
<h1>NDIS Regulatory Dossier <em>— every instrument, standard and document, in one traceable chain</em></h1></div>
<div class="stampbox">Snapshot · compiled 5 Jul 2026<br><b>__DOCS__ documents · __STDS__ standards</b><br>__LEG__ instruments · __EDGES__ typed links<br>static register — outbound links live</div>
</div></header>

<nav><div class="wrap">
<a href="#logic">The logic</a><a href="#legislation">Legislation</a><a href="#standards">Standards</a>
<a href="#documents">Documents</a><a href="#library">Reader</a><a href="#graph">Graph explorer</a><a href="#verification">Verification</a><a href="#sources">Sources</a><a href="#watch">Watch list</a>
</div></nav>

<main>
<section id="logic"><h2>The logic, top to bottom</h2>
<p class="lede">One chain explains the whole system. Every layer below answers to the layer above it, and every link in this dossier is one of these typed relationships.</p>
<div class="ladder">
<div class="rung"><span class="mono">Parliament</span><span>makes the <strong>NDIS Act 2013</strong> — the source of all authority.</span></div>
<div class="rung"><span class="mono">Made under the Act</span><span><strong>Rules and Guidelines</strong> (delegated legislation) — registration, incidents, complaints, restrictive practices, worker screening, the Code of Conduct, audit scheme.</span></div>
<div class="rung"><span class="mono">Set out in the Rules</span><span>The <strong>NDIS Practice Standards</strong> — Core module for everyone on the certification pathway, plus modules that switch on with what you deliver (high-intensity supports, behaviour support, early childhood, support coordination, SDA, and from 1 July 2026, SIL).</span></div>
<div class="rung"><span class="mono">Implements</span><span>Your <strong>policies</strong> — the commitments you make against each standard.</span></div>
<div class="rung"><span class="mono">Operationalises</span><span>Your <strong>procedures and work instructions</strong> — how, who, when.</span></div>
<div class="rung"><span class="mono">Uses → records to</span><span><strong>Forms</strong> capture each event; <strong>registers</strong> keep the running log.</span></div>
<div class="rung"><span class="mono">Evidences</span><span>Completed records become <strong>evidence</strong>; an approved quality auditor samples it against the standards; findings drive improvement actions. The loop closes.</span></div>
</div>
<div class="grid2" style="margin-top:14px">
<div class="fact"><b>Who checks?</b> Independent approved quality auditors — certification audits for higher-risk supports, desktop verification for lower-risk ones — reporting to the NDIS Commission.</div>
<div class="fact"><b>What changed in 2026?</b> SIL and platform providers must register from 1 July; new SIL Practice Standards apply; and the Integrity and Safeguarding Act sharply raises penalties, including for delivering registration-required supports while unregistered.</div>
<div class="fact"><b>Why a graph?</b> When any instrument changes, following the links backwards produces the exact review list of affected documents — the fan-out that keeps a provider current.</div>
</div></section>

<section id="legislation"><h2>Legislation — __LEG__ instruments</h2>
<p class="lede">FRL codes link to the Federal Register of Legislation (always the live, current version). The Commission maintains its own index of <a class="cite" href="https://www.ndiscommission.gov.au/about-us/legislation-rules-and-policies" target="_blank" rel="noopener">legislation, rules and policies</a>.</p>
<div class="tools"><input type="search" placeholder="Search instruments…" data-filter="#legtable"></div>
<div class="panel"><table id="legtable"><tbody>__LEGROWS__</tbody></table></div></section>

<section id="standards"><h2>Practice Standards — __STDS__ standards</h2>
<p class="lede">Citations pinpoint the schedule and clause of the Provider Registration and Practice Standards Rules 2018 (latest published compilation C04, 15 Nov 2021 — SIL locations pending consolidation). Each standard also shows the section of the Quality Indicators Guidelines (compilation C03, 1 Jul 2026) auditors assess it against.</p>
<div class="tools"><input type="search" placeholder="Search standards…" data-filter="#stdtable"><button class="chip on" data-chip="">All modules</button>__MODCHIPS__</div>
<div class="panel"><table id="stdtable"><tbody>__STDROWS__</tbody></table></div></section>

<section id="documents"><h2>Provider document suite — __DOCS__ documents</h2>
<p class="lede">The full best-practice suite: what to write, what each document implements, and how the pieces connect. Priority P1 is the audit-critical first wave. Expand a row for its typed links.</p>
<div class="tools"><input type="search" placeholder="Search documents…" data-filter="#doctable">
<select data-sel="type" data-target="#doctable"><option value="">All types</option>__TYOPTS__</select>
<select data-sel="cluster" data-target="#doctable"><option value="">All clusters</option>__CLOPTS__</select>
<select data-sel="pri" data-target="#doctable"><option value="">All priorities</option><option>P1</option><option>P2</option><option>P3</option></select></div>
<div class="panel"><table id="doctable"><tbody>__DOCROWS__</tbody></table></div></section>

<section id="library"><h2>Document reader — every document, drafted and linked</h2>
<p class="lede">All __DOCS__ documents exist as living drafts generated straight from the graph. Click any document ID anywhere in this dossier to open it here. Inside a document, every link is live: standards and legislation open in the graph explorer, documents open here. <span class="stamp draft">All drafts v0.1 — review before approval</span></p>
<div class="tools"><input id="dpick" list="gdocs" type="search" placeholder="Open a document, e.g. POL-INC-01" style="min-width:280px"><datalist id="gdocs">__DOCOPTS__</datalist><button class="chip" id="dgraph" type="button">Open current in graph explorer</button></div>
<article id="dread" class="panel" style="padding:22px 26px" aria-live="polite"><p class="meta">Pick a document to read it here.</p></article>
</section>

<section id="graph"><h2>Graph explorer — travel the linkages</h2>
<p class="lede">Pick any node — a policy, a form, a standard, an instrument — and see what it connects to, with every link typed. Solid lines point outward (toward authority or the things this node uses); dashed lines point in. <strong>Click any neighbour to travel.</strong> Click any ID anywhere in this dossier to jump here. Busy nodes show their 22 strongest links in the picture; the complete list is always below.</p>
<div class="tools"><button class="chip on" id="gmI" type="button">Instances</button><button class="chip" id="gmM" type="button">Data model</button><input id="gpick" list="gnodes" type="search" placeholder="Type an ID or title, e.g. POL-INC-01" style="min-width:280px"><datalist id="gnodes">__NODEOPTS__</datalist><span class="meta" id="gcrumb" aria-live="polite"></span></div>
<div class="gwrap"><svg id="gsvg" viewBox="0 0 1000 620" role="img" aria-label="Node linkage diagram"></svg></div>
<div class="grid2" style="margin-top:12px">
<div class="fact"><b id="gptitle">Authority chain</b><div id="gchain"></div></div>
<div class="fact"><b>All links for this node</b><div id="glist"></div></div>
</div></section>

<section id="verification"><h2>Verification & known gaps</h2>
<p class="lede">Nothing in this dossier hides its epistemic status. Every row carries a stamp.</p>
<div class="grid2">
<div class="fact"><span class="stamp verified">Verified — FRL / Commission, 5 Jul 2026</span><p>Checked against the Federal Register or the Commission's own pages. __V__ of __STDS__ standards, including the full Core, all supplementary modules and the verification module, traced to schedule and clause.</p></div>
<div class="fact"><span class="stamp draft">Draft source — confirm vs made 2026 Rules</span><p>The __D__ SIL standards. The module commenced 1 Jul 2026 but no consolidated compilation is published yet; names derive from the Commission's draft module.</p></div>
<div class="fact"><span class="stamp corrob">Corroborated / check</span><p>Adjacent-law placeholders (Privacy, WHS, discrimination, state worker screening) and two Commission guidelines whose FRL ids are still to be pulled.</p></div>
<div class="fact"><b>Not yet in the graph</b><p>Quality-indicator text (the thing auditors actually assess); registration-group → module applicability table; provision-level nodes; Easy Read companion documents as their own rows; jurisdictional overlays.</p></div>
</div></section>

<section id="sources"><h2>Sources - what stands behind every stamp</h2>
<p class="lede">Verified stamps rest only on Tier 1. Lower tiers corroborate and alert - never verify alone. Full register with access dates and the claim-by-claim trace: <span class="mono">rise-sources.md</span>. All accessed 5 July 2026.</p>
<div class="grid2">__SOURCES__</div></section>

<section id="watch"><h2>Watch list — moving parts</h2>
<p class="lede">Live reform items that will change this register. Each is a standing research task.</p>
__WATCH__</section>
</main>

<footer><div class="wrap"><strong>Rise dossier v0.1.</strong> Static snapshot generated 5 July 2026 by rise_build.py / rise_dossier.py — regenerate after any data change. Outbound links resolve to live sources. Suite composition, priorities and review cycles are design recommendations. This dossier is a compliance-engineering artefact, not legal advice.</div></footer>

<script>
(function(){
function rows(t){return Array.from(document.querySelectorAll(t+" tbody tr"))}
document.querySelectorAll("input[data-filter]").forEach(function(inp){
  inp.addEventListener("input",function(){
    var q=inp.value.toLowerCase();
    rows(inp.dataset.filter).forEach(function(r){
      r.style.display = r.textContent.toLowerCase().indexOf(q)>-1 ? "" : "none";});});});
var mod="";
document.querySelectorAll(".chip").forEach(function(c){
  c.addEventListener("click",function(){
    document.querySelectorAll(".chip").forEach(function(x){x.classList.remove("on")});
    c.classList.add("on"); mod=c.dataset.chip;
    rows("#stdtable").forEach(function(r){
      r.style.display = (!mod || r.dataset.mod===mod) ? "" : "none";});});});
var sels={type:"",cluster:"",pri:""};
document.querySelectorAll("select[data-sel]").forEach(function(s){
  s.addEventListener("change",function(){
    sels[s.dataset.sel]=s.value;
    rows(s.dataset.target).forEach(function(r){
      var ok=(!sels.type||r.dataset.type===sels.type)&&(!sels.cluster||r.dataset.cluster===sels.cluster)&&(!sels.pri||r.dataset.pri===sels.pri);
      r.style.display = ok ? "" : "none";});});});
})();
</script>
<script type="application/json" id="graphdata">__GRAPH__</script>
<script type="application/json" id="docdata">__DOCSJSON__</script>
<script>
(function(){
var D=JSON.parse(document.getElementById("graphdata").textContent);
function mkAdj(E){var a={};E.forEach(function(e){
 (a[e[0]]=a[e[0]]||[]).push({o:1,ty:e[1],x:e[2],n:e[3]||""});
 (a[e[2]]=a[e[2]]||[]).push({o:0,ty:e[1],x:e[0],n:e[3]||""});});return a}
var adjI=mkAdj(D.e),adjM=mkAdj(D.te),mode="i";
function adjOf(){return mode==="i"?adjI:adjM}
function NODES(){return mode==="i"?D.n:D.tn}
var adj=adjI;
var PRI={IMPLEMENTS:0,OPERATIONALISES:1,USES:2,RECORDS_TO:3,PART_OF:4,PUBLISHED_IN:5,MADE_UNDER:6};
function pri(t){return PRI[t]!==undefined?PRI[t]:8}
var DOCSH=JSON.parse(document.getElementById("docdata").textContent);
var dread=document.getElementById("dread"),dpick=document.getElementById("dpick"),curDoc=null;
var svg=document.getElementById("gsvg"),chainEl=document.getElementById("gchain"),
listEl=document.getElementById("glist"),crumb=document.getElementById("gcrumb"),
pick=document.getElementById("gpick"),trail=[];
function nk(i){return NODES()[i]||{t:i,k:"?",l:"shared"}}
function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;")}
function cut(s,n){s=String(s);return s.length>n?s.slice(0,n-1)+"\u2026":s}
function box(id,x,y,c,tip){var n=nk(id),w=176,h=46;
 var f=c?"#12284b":(n.l==="shared"?"#eef2f7":"#fdf6e7");
 var st=c?"#12284b":(n.l==="shared"?"#12284b":"#a06a00");
 var t1=c?"#fff":"#12284b",t2=c?"#cdd9ec":"#5a6673";
 return '<g class="gnode" tabindex="0" role="button" aria-label="'+esc(id)+'" data-id="'+esc(id)+'">'+(tip?'<title>'+esc(tip)+'</title>':'')+
 '<rect x="'+(x-w/2)+'" y="'+(y-h/2)+'" width="'+w+'" height="'+h+'" fill="'+f+'" stroke="'+st+'" stroke-width="1.6" rx="5"/>'+
 '<text x="'+x+'" y="'+(y-6)+'" text-anchor="middle" style="font:600 11px IBM Plex Mono,monospace" fill="'+t1+'">'+esc(cut(id,24))+'</text>'+
 '<text x="'+x+'" y="'+(y+11)+'" text-anchor="middle" style="font:10.5px Public Sans,sans-serif" fill="'+t2+'">'+esc(cut(n.t,30))+'</text></g>';}
function step(id,ty){var m=(adj[id]||[]).filter(function(e){return e.o&&e.ty===ty})[0];return m?m.x:null}
function rung(a,b){return '<div class="rung"><span class="mono">'+esc(a)+'</span><span>'+esc(b)+'</span></div>'}
function chainFrom(std){var out="";
 out+=rung("standard",std+" \u2014 "+nk(std).t);
 var mod=step(std,"PART_OF");if(!mod)return out;
 out+=rung("part of module",cut(mod+" \u2014 "+nk(mod).t,70));
 var fw=step(mod,"PART_OF");if(!fw)return out;
 out+=rung("framework",nk(fw).t);
 var ru=step(fw,"PUBLISHED_IN");if(!ru)return out;
 out+=rung("set out in",cut(nk(ru).t,72));
 var act=step(ru,"MADE_UNDER");if(act)out+=rung("made under",nk(act).t);
 return out;}
function chain(id){var n=nk(id),h="";
 if(n.k==="Standard")return chainFrom(id);
 if(n.k==="Module"){h+=rung("module",cut(nk(id).t,70));var fw=step(id,"PART_OF");
  if(fw){h+=rung("framework",nk(fw).t);var ru=step(fw,"PUBLISHED_IN");
   if(ru){h+=rung("set out in",cut(nk(ru).t,72));var a=step(ru,"MADE_UNDER");if(a)h+=rung("made under",nk(a).t);}}
  return h;}
 if(n.k==="Instrument"||n.k==="Framework"){h+=rung(n.k.toLowerCase(),cut(n.t,72));
  var a2=step(id,"MADE_UNDER");if(a2)h+=rung("made under",nk(a2).t);
  var r2=step(id,"PUBLISHED_IN");if(r2)h+=rung("set out in",cut(nk(r2).t,72));
  return h;}
 h+=rung(n.k.toLowerCase(),id+" \u2014 "+cut(n.t,60));
 var stds=(adj[id]||[]).filter(function(e){return e.o&&e.ty==="IMPLEMENTS"}).map(function(e){return e.x});
 if(!stds.length)return h+"<p class=meta>No IMPLEMENTS link \u2014 this node reaches law only via its related documents.</p>";
 if(stds.length>1)h+=rung("implements",stds.join("; ")+" (chain shown for the first)");
 return h+chainFrom(stds[0]);}
function typeInfo(id){var n=nk(id);
 return rung("purpose",n.t)+rung("key attributes",n.a||"see node taxonomy")+rung("layer",n.l==="shared"?"shared reference - one copy, centrally maintained":"tenant - private to each provider");}
function fillPick(){var o="";Object.keys(NODES()).forEach(function(k){o+='<option value="'+esc(k)+'">'+esc(cut(nk(k).t,60))+"</option>"});document.getElementById("gnodes").innerHTML=o;}
function setMode(m,start){mode=m;trail=[];
 document.getElementById("gmI").classList.toggle("on",m==="i");
 document.getElementById("gmM").classList.toggle("on",m==="m");
 fillPick();sel(start);}
document.getElementById("gmI").addEventListener("click",function(){setMode("i","POL-INC-01")});
document.getElementById("gmM").addEventListener("click",function(){setMode("m","Policy")});
function linkList(id,nb){var o="<ul>";
 nb.forEach(function(m){
  o+="<li"+(m.o?"":" class=dim")+">"+(m.o?esc(m.ty)+" \u2192 ":"\u2190 "+esc(m.ty)+" ")+
  '<a class="idlink" data-node="'+esc(m.x)+'" href="#graph">'+esc(m.x)+"</a>"+
  (m.n?" \u00b7 <span style=color:#8792a0>"+esc(cut(m.n,80))+"</span>":"")+"</li>";});
 return o+"</ul>";}
function sel(id){if(!NODES()[id])return;adj=adjOf();
 if(trail[trail.length-1]!==id)trail.push(id);
 if(trail.length>6)trail=trail.slice(-6);
 crumb.textContent="Path: "+trail.join(" \u2192 ");
 var nb=(adj[id]||[]).slice().sort(function(a,b){return pri(a.ty)-pri(b.ty)});
 var shown=nb.slice(0,22),extra=nb.length-shown.length;
 var W=1000,H=620,cx=W/2,cy=H/2,out="";
 shown.forEach(function(m,i){var a=-Math.PI/2+i*2*Math.PI/Math.max(shown.length,1);
  m._x=cx+Math.cos(a)*370;m._y=cy+Math.sin(a)*245;
  out+='<path class="gedge'+(m.o?"":" in")+'" d="M'+cx+" "+cy+" L"+m._x+" "+m._y+'"/>';
  var lx=cx+(m._x-cx)*0.55,ly=cy+(m._y-cy)*0.55;
  out+='<text class="glab" x="'+lx+'" y="'+(ly-3)+'" text-anchor="middle">'+esc(m.ty)+(m.o?" \u2192":" \u2190")+"</text>";});
 shown.forEach(function(m){out+=box(m.x,m._x,m._y,false,m.n)});
 out+=box(id,cx,cy,true,"");
 if(extra>0)out+='<text class="glab" x="'+cx+'" y="'+(H-10)+'" text-anchor="middle">+'+extra+" more \u2014 complete list below</text>";
 svg.innerHTML=out;
 svg.querySelectorAll(".gnode").forEach(function(g){function go(){sel(g.getAttribute("data-id"))}g.addEventListener("click",go);g.addEventListener("keydown",function(ev){if(ev.key==="Enter"||ev.key===" "){ev.preventDefault();go()}})});
 document.getElementById("gptitle").textContent=(mode==="i"?"Authority chain":"Type details");chainEl.innerHTML=(mode==="i"?chain(id):typeInfo(id));listEl.innerHTML=linkList(id,nb);pick.value=id;
}
pick.addEventListener("change",function(){var q=pick.value.trim();
 if(D.n[q])return sel(q);
 var qq=q.toLowerCase(),hit=null;
 Object.keys(D.n).forEach(function(k){if(!hit&&(k.toLowerCase()===qq||nk(k).t.toLowerCase().indexOf(qq)>-1))hit=k});
 if(hit)sel(hit);});
function openDoc(id){if(!DOCSH[id])return;curDoc=id;dread.innerHTML=DOCSH[id];dpick.value=id;}
function route(n){if(DOCSH[n]){openDoc(n)}else{if(mode!=="i"){setMode("i",n)}else{sel(n)}}}
document.addEventListener("click",function(ev){var a=ev.target.closest("a.idlink[data-node]");if(!a)return;route(a.getAttribute("data-node"));});
dpick.addEventListener("change",function(){var q=dpick.value.trim();if(DOCSH[q])return openDoc(q);
 var qq=q.toLowerCase(),hit=null;Object.keys(DOCSH).forEach(function(k){if(!hit&&D.n[k]&&D.n[k].t.toLowerCase().indexOf(qq)>-1)hit=k});if(hit)openDoc(hit);});
document.getElementById("dgraph").addEventListener("click",function(){if(!curDoc)return;if(mode!=="i"){setMode("i",curDoc)}else{sel(curDoc)}location.hash="#graph";});
sel("POL-INC-01");openDoc("POL-INC-01");
})();
</script></body></html>"""

for k, v in [("__DOCS__",counts["docs"]),("__STDS__",counts["stds"]),("__LEG__",counts["leg"]),
 ("__EDGES__",counts["edges"]),("__V__",counts["v"]),("__D__",counts["d"]),
 ("__LEGROWS__",leg_rows),("__STDROWS__",std_rows),("__DOCROWS__",doc_rows),
 ("__MODCHIPS__",mod_chips),("__TYOPTS__",ty_opts),("__CLOPTS__",cl_opts),("__WATCH__",watch_rows),("__GRAPH__",GRAPH),("__NODEOPTS__",node_opts),("__SOURCES__",src_html),("__DOCSJSON__",DOCSJSON),("__DOCOPTS__",doc_opts)]:
    page = page.replace(k, str(v))

open("/home/claude/rise-dossier.html","w").write(page)
print("dossier written:", len(page), "bytes")
