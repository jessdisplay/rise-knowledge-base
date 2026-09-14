"""The two human-facing layers of a policy, built on the same furniture as the
reference document (hcpdf.Doc) so all three share one letterhead and one page grid.

  worker card        one line per procedure step: tick box, step, who, record.
                     Read-Do checklist, set at 11 pt. The title words are the
                     policy's own; nothing is paraphrased.
  participant page   a plain-language summary at 16 pt, one idea per sentence,
                     hard words in bold and explained in a word list, a picture
                     slot beside every sentence for the Easy Read illustrations.
                     New words, marked as a summary: the policy stays the document
                     that applies.
"""
import os, re, sys, copy
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, KeepTogether
import hcpdf
from hcpdf import L, R, INK, BODY, MID, GREY, FOREST, SAGE, esc, clean
from layout import tint, modal, HAIR, ROW

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def steps_from(src):
    """The >> step cards in a template source: (title, who, records, actions)."""
    out, cur = [], None
    for line in open(src).read().split("\n"):
        if line.startswith(">>"):
            head = [x.strip() for x in clean(line[2:]).split("|")]
            title, who, rec = (head + ["", ""])[:3]
            cur = [title, who, rec, []]; out.append(cur)
        elif cur and re.match(r"^\s*[-*•]\s+", line):
            cur[3].append(clean(re.sub(r"^\s*[-*•]\s+", "", line)))
        elif line.startswith("# "):
            cur = None
    return out


SHORT = {   # the short names the policy itself uses for its records
    "Business Continuity, Emergency and Disaster Preparedness Management Plan": "Business Continuity Plan",
    "Incident Management and Reporting Policy": "Incident Management System",
}


def _finish(path, spec, story):
    d1 = hcpdf.Doc(path, spec); d1.build(copy.deepcopy(story))
    d2 = hcpdf.Doc(path, spec); d2.total = d1.page; d2.build(story)
    return path


# ----------------------------------------------------------------- worker card
def build_worker_card(spec, src, outdir):
    W = hcpdf.page_of(spec)["size"][0]; avail = W - L - R
    st = {
        "title": ParagraphStyle("t", fontName="Georgia-Bold", fontSize=22, leading=25, textColor=INK, spaceAfter=4),
        "lead":  ParagraphStyle("l", fontName="Helvetica", fontSize=11, leading=16.5, textColor=BODY, spaceAfter=14),
        "h":     ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=7.4, leading=10, textColor=FOREST, charSpace=0.9),
        "no":    ParagraphStyle("n", fontName="Helvetica-Bold", fontSize=10.5, leading=15, textColor=SAGE),
        "step":  ParagraphStyle("s", fontName="Helvetica-Bold", fontSize=10, leading=13.5, textColor=INK),
        "act":   ParagraphStyle("a", fontName="Helvetica", fontSize=9.6, leading=14, textColor=BODY, leftIndent=9, bulletIndent=0),
        "who":   ParagraphStyle("w", fontName="Helvetica", fontSize=9.4, leading=13, textColor=BODY),
        "box":   ParagraphStyle("b", fontName="Helvetica", fontSize=13, leading=15, textColor=GREY),
        "foot":  ParagraphStyle("f", fontName="Helvetica", fontSize=9.6, leading=14, textColor=MID, spaceBefore=10),
    }
    steps = steps_from(src)
    story = [Paragraph(esc(spec["title"]), st["title"]),
             Paragraph(esc(spec["subtitle"]), st["lead"])]
    hdr = [Paragraph("", st["h"]), Paragraph("", st["h"]), Paragraph("STEP", st["h"]),
           Paragraph("WHO", st["h"]), Paragraph("RECORD", st["h"])]
    rows = [hdr]
    for k, (title, who, rec, acts) in enumerate(steps, 1):
        cell = [Paragraph(esc(title), st["step"])]
        recs = "<br/>".join(esc(SHORT.get(r.strip(), r.strip())) for r in rec.split("·") if r.strip()) if rec else ""
        box = Table([[""]], colWidths=[0.42 * cm], rowHeights=[0.42 * cm])
        box.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.7, MID)]))
        rows.append([box, Paragraph(f"{k:02d}", st["no"]), cell,
                     Paragraph(esc(who or "—"), st["who"]), Paragraph(recs, st["who"])])
    t = Table(rows, colWidths=[0.75 * cm, 0.95 * cm, avail - 0.75 * cm - 0.95 * cm - 4.0 * cm - 4.0 * cm,
                               4.0 * cm, 4.0 * cm], repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 0.7, FOREST),
        ("LINEBELOW", (0, 1), (-1, -1), 0.35, ROW),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Paragraph("The policy is the document that applies.", st["foot"]))
    os.makedirs(outdir, exist_ok=True)
    return _finish(os.path.join(outdir, hcpdf.outname(spec, "pdf")), spec, story)


# ------------------------------------------------------------ participant page
def build_participant_page(spec, items, words, outdir):
    """items: list of (sentence html, picture caption). 16 pt, 1.5 spacing, a picture slot per idea."""
    W = hcpdf.page_of(spec)["size"][0]; avail = W - L - R
    st = {
        "title": ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=26, leading=32, textColor=INK, spaceAfter=6),
        "lead":  ParagraphStyle("l", fontName="Helvetica", fontSize=16, leading=24, textColor=BODY, spaceAfter=18),
        "idea":  ParagraphStyle("i", fontName="Helvetica", fontSize=16, leading=24, textColor=INK),
        "pic":   ParagraphStyle("p", fontName="Helvetica", fontSize=8, leading=11, textColor=GREY, alignment=1),
        "h":     ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=18, leading=24, textColor=FOREST, spaceBefore=18, spaceAfter=8),
        "word":  ParagraphStyle("w", fontName="Helvetica-Bold", fontSize=14, leading=21, textColor=INK),
        "mean":  ParagraphStyle("m", fontName="Helvetica", fontSize=14, leading=21, textColor=BODY),
        "foot":  ParagraphStyle("f", fontName="Helvetica", fontSize=12, leading=18, textColor=MID, spaceBefore=14),
    }
    story = [Paragraph(esc(spec["title"]), st["title"]),
             Paragraph(esc(spec["subtitle"]), st["lead"])]
    pic_w = 3.6 * cm
    for sentence, cap in items:
        slot = Table([[Paragraph(esc(cap), st["pic"])]], colWidths=[pic_w], rowHeights=[2.7 * cm])
        slot.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.6, SAGE), ("BACKGROUND", (0, 0), (-1, -1), tint("#9EAE8F", 0.93)),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        row = Table([[slot, Paragraph(sentence, st["idea"])]], colWidths=[pic_w + 0.7 * cm, avail - pic_w - 0.7 * cm])
        row.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LINEBELOW", (0, 0), (-1, -1), 0.35, ROW),
        ]))
        story.append(KeepTogether(row))
    story.append(Paragraph("Word list", st["h"]))
    wl = Table([[Paragraph(esc(w), st["word"]), Paragraph(esc(m), st["mean"])] for w, m in words],
               colWidths=[4.6 * cm, avail - 4.6 * cm], hAlign="LEFT")
    wl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LINEBELOW", (0, 0), (-1, -2), 0.35, ROW),
    ]))
    story.append(wl)
    story.append(Paragraph("This page is a summary. The Risk Management Policy is the document that applies. "
                           "The picture boxes are for the Easy Read illustrations.", st["foot"]))
    os.makedirs(outdir, exist_ok=True)
    return _finish(os.path.join(outdir, hcpdf.outname(spec, "pdf")), spec, story)


def build_layers(cfg_path):
    """cfg: {"source": md, "outdir": dir, "control": {...}, "worker": {...}, "participant": {...}}"""
    import json
    cfg = json.load(open(cfg_path))
    here = os.path.dirname(os.path.abspath(cfg_path))
    src = os.path.join(here, cfg["source"]); out = os.path.join(here, cfg["outdir"])
    base = dict(type="POLICY", rail="#38553E", ref="", page="A4", **cfg.get("control", {}))
    w, p = cfg["worker"], cfg["participant"]
    print("->", build_worker_card({**base, "page": "A4C", "label": w.get("label", "Worker card"),
                                   "title": w["title"], "subtitle": w["subtitle"]}, src, out))
    print("->", build_participant_page({**base, "label": p.get("label", "Plain language summary"),
                                        "title": p["title"], "subtitle": p["subtitle"]},
                                       [tuple(x) for x in p["items"]], [tuple(x) for x in p["words"]], out))


if __name__ == "__main__":
    for cfg in sys.argv[1:] or [os.path.join(HERE, "templates", "layers_risk.json")]:
        build_layers(cfg)
