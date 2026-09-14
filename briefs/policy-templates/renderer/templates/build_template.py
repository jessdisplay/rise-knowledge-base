"""Builds the worked Policy and Procedure template from Harmony Care's own source.

Nothing in the wording is rewritten. Three things are added, each taken from a
document Harmony Care already holds:

  @notes   the marginal column: standard, quality indicators, register entry
  !!       the key commitment, lifted verbatim from the policy's own 1.2
  >>       section 4's two-column table re-set as numbered procedure steps,
           with the responsibility column kept and the records named in the
           step's own words linked to the real documents in the set
"""
import json, re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "src-hc", "Risk Management Policy.md")
OUT = os.path.join(HERE, "src", "Risk Management Policy and Procedure.md")

titles = [s["title"] for s in json.load(open(os.path.join(ROOT, "spec_hc.json")))]
ALIAS = {
    "Risk Register": "Risk Register",
    "Business Continuity Plan": "Business Continuity, Emergency and Disaster Preparedness Management Plan",
    "Incident Management System": "Incident Management and Reporting Policy",
    "Emergency Plan": "Client Emergency Plan",
    "Continuous Improvement": "Continuous Improvement Register",
}
LOOKUP = sorted({**{t: t for t in titles}, **ALIAS}.items(), key=lambda kv: -len(kv[0]))

# marginal notes, keyed by section number. Every value is quoted from a
# Harmony Care document: the policy's own 1.1/1.3, the Policy Register, the
# Legislation Register.
MARGIN = {
    1: [("standard", "Risk Management, NDIS Practice Standards"),
        ("indicators", "Six, lettered (a) to (f) at 1.3"),
        ("register", "Policy Register: Version 1, approved October 2023")],
    2: [("terms", "Nine defined terms, used throughout")],
    3: [("evidence", "Risk Register  ·  Business Continuity Plan"),
        ("law", "WHS Act 2011 (QLD) and WHS Regulation 2011 (QLD)")],
    4: [("who", "Principal  ·  All Workers"),
        ("records", "Named on each step below")],
    5: [("legislation", "Listed in the Legislation Register"),
        ("review", "Register says October 2026. This document says October 2025.")],
}

def records_in(text):
    """The documents this step names, in the step's own words."""
    found = []
    for phrase, doc in LOOKUP:
        if re.search(r"\b" + re.escape(phrase) + r"\b", text, re.I) and doc not in found:
            found.append(doc)
    return found[:3]

lines = open(SRC).read().split("\n")
out, i, n = [], 0, len(lines)
while i < n:
    line = lines[i]
    m = re.match(r"^# (\d+)\.", line)
    if m:
        out.append(line)
        for lab, val in MARGIN.get(int(m.group(1)), []):
            out.append(f"@{lab.strip()} {val}")
        i += 1
        # section 4: the procedure table becomes numbered steps
        if m.group(1) == "4":
            while i < n and not lines[i].strip().startswith("|"):
                out.append(lines[i]); i += 1
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if cells and cells[0] and cells[0].lower() != "procedure":
                    rows.append(cells)
                i += 1
            for cells in rows:
                parts = [p.strip() for p in cells[0].split("¶") if p.strip()]
                who = cells[1].strip() if len(cells) > 1 else ""
                title, acts = parts[0], parts[1:]
                recs = records_in(" ".join(parts))
                out.append(f">> {title} | {who} | {'  ·  '.join(recs)}")
                for a in acts:
                    out.append(f"- {a}")
                out.append("")
        continue
    # the key commitment, lifted from 1.2 without a word changed
    if line.startswith("## 1.2 Policy Aims"):
        out.append(line)
        j = i + 1
        while j < n and not lines[j].strip():
            j += 1
        out.append("")
        out.append("!! " + lines[j].strip())
        i = j + 1
        continue
    out.append(line); i += 1

open(OUT, "w").write("\n".join(out))
steps = sum(1 for l in out if l.startswith(">>"))
print(f"{OUT}\n  {len(out)} lines, {steps} procedure steps, "
      f"{sum(1 for l in out if l.startswith('@'))} marginal notes")
