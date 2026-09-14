"""
Harmony Care — PDF renderer.

Same design as hcdoc.py (LOCK-doc-page.png), output as a fixed-layout PDF so it
looks identical wherever it is opened. Reads the same src/*.md + spec entries.
"""
import os, re, sys, json
from layout import build_story, styles as gstyles, GUTTER, GAP
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, Image, KeepTogether,
                                PageBreak)

HERE = os.path.dirname(os.path.abspath(__file__))
HEADER_ART = f"{HERE}/art/band-header.jpg"
FOOTER_ART = f"{HERE}/art/band-footer.jpg"

pdfmetrics.registerFont(TTFont("Georgia", "/System/Library/Fonts/Supplemental/Georgia.ttf"))
pdfmetrics.registerFont(TTFont("Georgia-Bold", "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"))
pdfmetrics.registerFont(TTFont("Georgia-Italic", "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"))
pdfmetrics.registerFontFamily("Georgia", normal="Georgia", bold="Georgia-Bold",
                              italic="Georgia-Italic", boldItalic="Georgia-Bold")

TYPES = {
    "POLICY":    ("Policy",    "#5C3A52"),
    "PROCEDURE": ("Procedure", "#6683A5"),
    "FORM":      ("Form",      "#C1964F"),
    "REGISTER":  ("Register",  "#8B9C7E"),
    "AGREEMENT": ("Agreement", "#B79BBA"),
    "PLAN":      ("Plan",      "#B79BBA"),
    "REPORT":    ("Report",    "#C6746F"),
}

INK, BODY, MID, GREY = (HexColor("#2F2F2F"), HexColor("#3A3A3A"),
                        HexColor("#6A6A6A"), HexColor("#8C8C8C"))
PAPER  = HexColor("#FDFBF6")   # the letterhead's cream
SAGE   = HexColor("#9EAE8F")   # the rule colour
FOREST = HexColor("#38553E")
HAIR = HexColor("#D8D4CB")
ROW = HexColor("#E6E2D8")

LAW_URLS = {
    # verified in the Rise knowledge base (context/ mirror), not typed from memory
    "NDIS (Provider Registration and Practice Standards) Rules 2018":
        "https://www.legislation.gov.au/F2018L00631/latest/text",
    "PRPS": "https://www.legislation.gov.au/F2018L00631/latest/text",
    "QI Guidelines": "https://www.legislation.gov.au/F2018N00041/latest/text",
    "Quality Indicators": "https://www.legislation.gov.au/F2018N00041/latest/text",
}

REGISTRY = {}   # HCS ref -> output filename, filled by __main__


def outname(spec, ext):
    """Coded documents keep the code-and-hyphens name; the provider's own set
    keeps its plain title, which is how their staff look for it."""
    title = spec["title"].replace("/", "-")
    if spec.get("ref"):
        return f"{spec['ref']}_{title.replace(' ', '-')}.{ext}"
    return f"{title}.{ext}"


def linkify(text):
    """Turn instrument names and HCS document codes into live links.
    Only instruments with a verified URL are linked; everything else stays plain."""
    out = esc(text)
    for name, url in sorted(LAW_URLS.items(), key=lambda kv: -len(kv[0])):
        pat = re.escape(esc(name))
        out = re.sub(rf"(?<!>){pat}",
                     f'<a href="{url}" color="#38553E"><u>{esc(name)}</u></a>', out, count=1)
    def _doc(m):
        ref = m.group(0)
        target = REGISTRY.get(ref)
        if not target:
            return ref
        return f'<a href="{target}" color="#38553E"><u>{ref}</u></a>'
    out = re.sub(r"HCS-[A-Z0-9]+-[A-Z0-9]+-\d+|HCS-[A-Z]+-\d+", _doc, out)
    return out


ENTITY = "Harmony Care Support Services Pty Ltd  ·  ABN 99 691 543 834  ·  ACN 691 543 834"

L = R = 2.45 * cm
TOP = 5.45 * cm
BOT = 6.65 * cm
MEASURE = 0.0 * cm     # the editorial grid owns the internal gutter

# Page geometry per size. Landscape pages use the locked COMPACT furniture:
# the full 4.7 cm footer would take a quarter of a 21 cm-tall page.
PAGES = {
    "A4":  dict(size=(21.0 * cm, 29.7 * cm), top=TOP, bot=BOT,
                head=f"{HERE}/art/band-header.jpg", head_h=3.81 * cm,
                foot=f"{HERE}/art/band-footer.jpg", foot_h=4.70 * cm,
                head_inset=1.27 * cm, foot_inset=1.10 * cm, ctl=6.22 * cm),
    "A4C": dict(size=(21.0 * cm, 29.7 * cm), top=4.15 * cm, bot=4.35 * cm,
                head=f"{HERE}/art/band-header-compact-210mm.png", head_h=2.36 * cm,
                foot=f"{HERE}/art/band-footer-compact-210mm.png", foot_h=2.54 * cm,
                head_inset=1.10 * cm, foot_inset=1.00 * cm, ctl=3.85 * cm),
    "A4L": dict(size=(29.7 * cm, 21.0 * cm), top=4.15 * cm, bot=4.35 * cm,
                head=f"{HERE}/art/band-header-compact-297mm.png", head_h=2.35 * cm,
                foot=f"{HERE}/art/band-footer-compact-297mm.png", foot_h=2.54 * cm,
                head_inset=1.10 * cm, foot_inset=1.00 * cm, ctl=3.85 * cm),
    "A3L": dict(size=(42.0 * cm, 29.7 * cm), top=4.15 * cm, bot=4.35 * cm,
                head=f"{HERE}/art/band-header-compact-420mm.png", head_h=2.35 * cm,
                foot=f"{HERE}/art/band-footer-compact-420mm.png", foot_h=2.54 * cm,
                head_inset=1.10 * cm, foot_inset=1.00 * cm, ctl=3.85 * cm),
}


def page_of(spec):
    return PAGES.get(spec.get("page") or "A4", PAGES["A4"])


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def clean(s):
    s = s.replace("\\*", "*").replace("\\[", "[").replace("\\]", "]")
    s = s.replace("\\#", "#").replace("\\_", "_").replace("\\.", ".").replace("\\|", "|")
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"(?<!\w)\*(.+?)\*(?!\w)", r"\1", s)
    return s.strip()


def styles(rail):
    body = ParagraphStyle("body", fontName="Georgia", fontSize=10.5, leading=15.2,
                          textColor=BODY, spaceAfter=8, alignment=TA_LEFT)
    return {
        "title": ParagraphStyle("title", fontName="Georgia-Bold", fontSize=22, leading=25,
                                textColor=INK, spaceAfter=6),
        "sub": ParagraphStyle("sub", fontName="Georgia", fontSize=11, leading=15,
                              textColor=MID, spaceAfter=18),
        "covers": ParagraphStyle("covers", fontName="Georgia", fontSize=9, leading=13,
                                 textColor=MID, spaceAfter=16),
        "coverslabel": ParagraphStyle("coverslabel", fontName="Helvetica-Bold", fontSize=7,
                                      textColor=GREY, charSpace=1.6),
        "h1": ParagraphStyle("h1", fontName="Helvetica-BoldOblique", fontSize=8.5,
                             leading=12, textColor=HexColor(rail), spaceBefore=19,
                             spaceAfter=6, charSpace=0.9),
        "h2": ParagraphStyle("h2", fontName="Georgia-Bold", fontSize=10.5, leading=14,
                             textColor=INK, spaceBefore=12, spaceAfter=3),
        "body": body,
        "li": ParagraphStyle("li", parent=body, leftIndent=14, bulletIndent=3, spaceAfter=4),
        "cellh": ParagraphStyle("cellh", fontName="Helvetica-Bold", fontSize=7,
                                leading=9.5, textColor=HexColor(rail), charSpace=1.0),
        "cell": ParagraphStyle("cell", fontName="Georgia", fontSize=8.6, leading=12,
                               textColor=BODY),
        "callh": ParagraphStyle("callh", fontName="Helvetica-Bold", fontSize=7,
                                leading=10, textColor=HexColor(rail)),
        "callb": ParagraphStyle("callb", fontName="Georgia", fontSize=9.4, leading=13.4,
                                textColor=MID),
    }


def track(text, pts=1.4):
    """Caps only — real letterspacing is applied via the style's charSpace."""
    return text.upper()


class Doc(BaseDocTemplate):
    total = None

    def __init__(self, path, spec, **kw):
        self.spec = spec
        self.label, self.rail = TYPES[spec["type"]]
        # colour and type label are separable: a policy can carry the Business
        # Plan colourway and still be labelled "Policy"
        self.rail = spec.get("rail", self.rail)
        self.label = spec.get("label", self.label)
        self.geo = page_of(spec)
        W, H = self.geo["size"]
        top, bot = self.geo["top"], self.geo["bot"]
        super().__init__(path, pagesize=(W, H), leftMargin=L, rightMargin=R + MEASURE,
                         topMargin=top, bottomMargin=bot,
                         title=" ".join(x for x in (spec.get("ref"), spec["title"]) if x),
                         author="Harmony Care Support Services Pty Ltd", **kw)
        frame = Frame(L, bot, W - L - R - MEASURE, H - top - bot, id="body",
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=self.furniture)])

    def furniture(self, c, doc):
        s = self.spec
        g = self.geo
        W, H = g["size"]

        # cream ground
        c.setFillColor(PAPER)
        c.rect(0, 0, W, H, stroke=0, fill=1)

        # header band — inset 1.27 cm from the page top, matching the proof.
        # The artwork has no internal padding, so drawing it flush clips the cast.
        try:
            c.drawImage(g["head"], 0, H - g["head_inset"] - g["head_h"], width=W,
                        height=g["head_h"], mask="auto")
        except Exception:
            pass

        # document identification, sitting under the band against the right margin
        # A document code is printed only where the document actually has one.
        # The provider's own set has no code scheme, so the type label carries
        # that slot rather than an identifier invented at render time.
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(FOREST)
        c.drawRightString(W - R, H - g["head_inset"] - 1.31 * cm,
                          s.get("ref") or self.label.upper())
        c.setFont("Helvetica", 7.2)
        c.setFillColor(MID)
        bits = [self.label] if s.get("ref") else []
        if s.get("version"):
            bits.append(f"v{s['version']}")
        if s.get("status"):
            bits.append(s["status"])
        if s.get("module"):
            bits.append(s["module"])
        if bits:
            c.drawRightString(W - R, H - g["head_inset"] - 1.75 * cm,
                              "  ·  ".join(bits))

        # footer band, full bleed
        try:
            c.drawImage(g["foot"], 0, g["foot_inset"], width=W, height=g["foot_h"],
                        mask="auto")
        except Exception:
            pass

        # page number and control line, above the footer artwork
        c.setFont("Helvetica", 6.6)
        c.setFillColor(GREY)
        ctl = [x for x in (s.get("ref"),
                           f"Version {s['version']}" if s.get("version") else "",
                           f"Approved {s['effective']}" if s.get("effective") else "",
                           f"Next review {s['review']}" if s.get("review") else "") if x]
        if ctl:
            c.drawString(L, g["ctl"], "  ·  ".join(ctl) + "  ·  Retain 7 years")
        c.drawRightString(W - R, g["ctl"],
                          f"Page {c.getPageNumber()} of {self.total or '?'}")


def parse_table(block):
    rows = []
    for l in block:
        if re.match(r"^\|[\s:\-|]+\|$", l.strip()):
            continue
        cells = [clean(x) for x in l.strip().strip("|").split("|")]
        if any(cells):
            rows.append(cells)
    if not rows:
        return None, None
    w = max(len(r) for r in rows)
    rows = [r + [""] * (w - len(r)) for r in rows]
    return rows[0], rows[1:]


def build(spec, outdir):
    rail = spec.get("rail", TYPES[spec["type"]][1])
    st = styles(rail)
    avail = page_of(spec)["size"][0] - L - R - MEASURE
    story = [Paragraph(esc(spec["title"]), st["title"])]
    if spec.get("subtitle"):
        story.append(Paragraph(esc(spec["subtitle"]), st["sub"]))
    if spec.get("covers"):
        story.append(Paragraph(
            f'<font name="Helvetica-Bold" size="7" color="#8A8286">COVERS</font>'
            f'&nbsp;&nbsp;&nbsp; {esc(spec["covers"])}', st["covers"]))

    # ---- compliance links: what this document answers to, at the top ----
    if spec.get("links"):
        from layout import tint as _tint
        lst = gstyles(rail)
        hdr = [Paragraph(h, lst["cellh"]) for h in ("LINK TYPE", "PLAIN ENGLISH", "LINKED TO")]
        rows = [hdr]
        for kind, plain, target in spec["links"]:
            rows.append([Paragraph(kind.upper(), lst["cellh"]),
                         Paragraph(esc(plain), lst["cell"]),
                         Paragraph(linkify(target), lst["cellb"])])
        lt = Table(rows, colWidths=[avail * .19, avail * .28, avail * .53],
                   repeatRows=1, hAlign="LEFT")
        lt.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), _tint("#38553E", 0.93)),
            ("LINEBELOW", (0, 0), (-1, 0), 0.7, HexColor("#38553E")),
            ("LINEBELOW", (0, 1), (-1, -2), 0.3, HexColor("#E6E2D8")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(lt)
        story.append(PageBreak())

    gst = gstyles(rail, spec.get("base", 9.4))
    story += build_story(os.path.join(HERE, spec["source"]), gst, rail, avail)



    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, outname(spec, "pdf"))
    import copy
    d1 = Doc(path, spec); d1.build(copy.deepcopy(story))
    total = d1.page
    d2 = Doc(path, spec); d2.total = total; d2.build(story)
    return path


if __name__ == "__main__":
    specs = json.load(open(sys.argv[1]))
    if isinstance(specs, dict):
        specs = [specs]
    outdir = os.path.join(HERE, "pdf")
    for sp in specs:
        if sp.get("ref"):
            REGISTRY[sp["ref"]] = outname(sp, "pdf")
    failed = []
    for s in specs:
        try:
            print("  ->", os.path.basename(build(s, outdir)))
        except Exception as exc:                     # keep going, report at the end
            failed.append((s["title"], f"{type(exc).__name__}: {exc}"))
            print("  !! FAILED", s["title"])
    if failed:
        print(f"\n{len(failed)} of {len(specs)} failed:")
        for t, e in failed:
            print(f"   {t}: {e[:150]}")
