"""
Harmony Care — structured policy layout.

The previous build was a title followed by undifferentiated prose. This lays the
document on a real editorial grid:

  · a marginal column carrying the section number, the clause reference and the
    evidence codes — so the wide right/left margin does work instead of sitting empty
  · content typed into blocks: statements, steps, definitions, responsibilities,
    each with its own visual treatment rather than all being paragraphs
  · numbered policy statements with hanging decimals (3.1, 3.2 …)
  · procedure steps with the step number set in the rail colour
  · tables with a tinted header band and hairline rows
  · a closing document-control block

Source markup understood, per section:
    # 1. Purpose                 -> section
    @clause  Schedule 1, Cl 3    -> marginal note on the current section
    @evidence HCS-F-PCS-001      -> marginal evidence code
    !! key commitment text       -> pulled-out commitment panel
    1. / - / |table|             -> steps, bullets, tables
"""
import os, re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, KeepTogether

GUTTER = 3.6 * cm
GAP = 0.8 * cm

INK, BODY, MID, GREY = (HexColor("#2F2F2F"), HexColor("#3A3A3A"),
                        HexColor("#6A6A6A"), HexColor("#8C8C8C"))
SAGE = HexColor("#9EAE8F")
FOREST = HexColor("#38553E")
HAIR = HexColor("#D8D4CB")
ROW = HexColor("#E6E2D8")


def tint(hexcolor, amount=0.92):
    c = HexColor(hexcolor)
    return HexColor("#%02x%02x%02x" % (
        int(255 - (255 - c.red * 255) * (1 - amount)),
        int(255 - (255 - c.green * 255) * (1 - amount)),
        int(255 - (255 - c.blue * 255) * (1 - amount))))


def styles(rail, base_pt=9.4):
    rail = "#38553E"   # the letterhead uses forest/sage, not a per-type colour
    k = base_pt / 9.4     # every size and leading below scales with the base
    base = ParagraphStyle("b", fontName="Helvetica", fontSize=9.4*k, leading=14.6*k,
                          textColor=BODY, spaceAfter=7,
                          allowWidows=0, allowOrphans=0)
    return {
        "body": base,
        "lead": ParagraphStyle("lead", parent=base, fontSize=11*k, leading=16.5*k,
                               textColor=MID, spaceAfter=10),
        "num": ParagraphStyle("num", fontName="Helvetica-Bold", fontSize=17*k, leading=19*k,
                              textColor=SAGE),
        "seclabel": ParagraphStyle("seclabel", fontName="Helvetica-Bold", fontSize=8*k,
                                   leading=11*k, textColor=HexColor(rail), charSpace=0.9),
        "margin": ParagraphStyle("margin", fontName="Helvetica", fontSize=6.6*k,
                                 leading=9.4*k, textColor=GREY),
        "marginlab": ParagraphStyle("marginlab", fontName="Helvetica-Bold", fontSize=6*k,
                                    leading=9*k, textColor=HexColor(rail), charSpace=0.7),
        "stmt": ParagraphStyle("stmt", parent=base, fontSize=10*k, leading=15*k, spaceAfter=5),
        "stmtno": ParagraphStyle("stmtno", fontName="Helvetica-Bold", fontSize=8.5*k,
                                 leading=14*k, textColor=HexColor(rail)),
        "keyh": ParagraphStyle("keyh", fontName="Helvetica-Bold", fontSize=6.5*k,
                               leading=10*k, textColor=HexColor(rail), charSpace=1.2),
        "key": ParagraphStyle("key", fontName="Helvetica", fontSize=9.6*k, leading=14.6*k,
                              textColor=INK),
        "cellh": ParagraphStyle("cellh", fontName="Helvetica-Bold", fontSize=6.6*k,
                                leading=9.5*k, textColor=HexColor(rail), charSpace=0.8),
        "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4*k, leading=12.2*k,
                               textColor=BODY),
        "cellb": ParagraphStyle("cellb", fontName="Helvetica-Bold", fontSize=8.4*k, leading=12.2*k,
                                textColor=INK),
        "steptitle": ParagraphStyle("steptitle", fontName="Helvetica-Bold", fontSize=9.8*k,
                                    leading=13.4*k, textColor=INK, spaceAfter=4),
        "stepact": ParagraphStyle("stepact", fontName="Helvetica", fontSize=9.2*k, leading=14*k,
                                  textColor=BODY, leftIndent=11, bulletIndent=1,
                                  spaceAfter=3, allowWidows=0, allowOrphans=0),
        "stepchip": ParagraphStyle("stepchip", fontName="Helvetica", fontSize=7.4*k,
                                   leading=10.5*k, textColor=MID, charSpace=0.2),
    }


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def clean(s):
    s = (s.replace("\\*", "*").replace("\\[", "[").replace("\\]", "]")
          .replace("\\#", "#").replace("\\_", "_").replace("\\.", ".").replace("\\|", "|"))
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"(?<!\w)\*(.+?)\*(?!\w)", r"\1", s)
    return s.strip()


def _grid(gutter_flow, main_flow, width, gutter=GUTTER):
    """One row of the editorial grid: marginal column, then content.

    A document with no marginal notes gets no marginal column: an empty
    3.6 cm rail on every page is dead space, and it pushes the body out of
    line with the title and the letterhead."""
    if not gutter:
        t = Table([[main_flow]], colWidths=[width], hAlign="LEFT")
        t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        return t
    t = Table([[gutter_flow, main_flow]],
              colWidths=[gutter + GAP, width - gutter - GAP], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, 0), GAP),
        ("RIGHTPADDING", (1, 0), (1, 0), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


MODAL = re.compile(r"\b(must not|must|should not|should|may)\b", re.I)


def modal(text):
    """Obligation words carry the weight of a procedure: set them bold."""
    return MODAL.sub(lambda m: f"<b>{m.group(1)}</b>", text)


def build_story(src, st, rail, width, gutter=None):
    """Parse the source into a laid-out story.

    gutter=None auto-detects: documents that carry @clause/@standard notes get
    the marginal column, documents that do not get the full measure."""
    lines = open(src).read().split("\n")
    if gutter is None:
        gutter = GUTTER if any(re.match(r"^@\w+\s", l.strip()) for l in lines) else 0
    pull = gutter + GAP if gutter else 0
    avail = width - pull
    story, i, n = [], 0, len(lines)
    sec = 0
    step_no = 0
    pending_margin = []          # @clause / @evidence waiting for their section
    main = []                    # flowables for the current section

    def flush(title=None, number=None):
        nonlocal main, pending_margin
        if title is None and not main:
            return
        gut = []
        if number is not None and gutter:
            gut.append(Paragraph(f"{number:02d}", st["num"]))
            gut.append(Spacer(1, 3))
        for lab, val in pending_margin:
            gut.append(Paragraph(lab.upper(), st["marginlab"]))
            gut.append(Paragraph(esc(val), st["margin"]))
            gut.append(Spacer(1, 5))
        # the section label sits on the first grid row with the marginal column;
        # every following block gets its own row so content can break across pages
        head = []
        if title:
            chip = "  ·  ".join(v for k, v in pending_margin
                                if k in ("clause", "standard", "rules"))
            lab = esc(title).upper()
            if not gutter and number is not None:
                lab = (f'<font name="Helvetica-Bold" size="10" color="#9EAE8F">'
                       f'{number:02d}</font>&nbsp;&nbsp;&nbsp;' + lab)
            if chip:
                lab += (f'&nbsp;&nbsp;&nbsp;<font name="Helvetica" size="6" '
                        f'color="#8B9C7E">{esc(chip.upper())}</font>')
            head.append(Paragraph(lab, st["seclabel"]))
            head.append(Spacer(1, 5))
        def is_raw(x):
            return isinstance(x, tuple) and x and x[0] == "RAW"

        def is_h2(x):
            return isinstance(x, tuple) and x and x[0] == "H2"

        lead = []
        rest = list(main)
        while rest and not is_raw(rest[0]) and not is_h2(rest[0]):
            lead.append(rest.pop(0))
            if len(lead) >= 2:
                break
        # a sub-heading straight after the section label joins the lead block
        if rest and is_h2(rest[0]) and len(lead) < 2:
            lead.append(rest.pop(0)[1])
            if rest and not is_raw(rest[0]) and not is_h2(rest[0]):
                lead.append(rest.pop(0))
        story.append(KeepTogether(_grid(gut or Spacer(1, 1), head + lead, width, gutter)))
        k = 0
        while k < len(rest):
            item = rest[k]
            if is_h2(item):
                # pair the sub-heading with whatever follows it — unless the
                # next item is itself a sub-heading, which stands alone
                nxt = rest[k + 1] if k + 1 < len(rest) else None
                h2row = _grid(Spacer(1, 1), [item[1]], width, gutter)
                if nxt is None or is_h2(nxt):
                    story.append(h2row)
                elif is_raw(nxt):
                    # only bind a short block to its heading: a long table must
                    # stay free to split, or it cannot be laid out at all
                    short = len(getattr(nxt[1], "_cellvalues", []) or []) <= 4
                    if short:
                        story.append(KeepTogether([h2row, nxt[1]]))
                    else:
                        story.append(h2row)
                        story.append(nxt[1])
                    k += 1
                else:
                    story.append(KeepTogether([h2row,
                                               _grid(Spacer(1, 1), [nxt], width, gutter)]))
                    k += 1
            elif is_raw(item):
                story.append(item[1])
            else:
                story.append(_grid(Spacer(1, 1), [item], width, gutter))
            k += 1
        story.append(Spacer(1, 16))
        main, pending_margin = [], []

    title_pending, num_pending = None, None
    while i < n:
        raw = lines[i].rstrip()
        line = raw.strip()
        if not line:
            i += 1; continue

        if line.startswith("@"):
            m = re.match(r"@(\w+)\s+(.*)", line)
            if m:
                pending_margin.append((m.group(1), clean(m.group(2))))
            i += 1; continue

        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m and len(m.group(1)) == 1:
            flush(title_pending, num_pending)
            sec += 1
            step_no = 0
            title_pending = re.sub(r"^\d+[\.\)]\s*", "", clean(m.group(2)))
            num_pending = sec
            i += 1; continue
        if m:
            main.append(("H2", Paragraph(esc(clean(m.group(2))),
                                  ParagraphStyle("h2", parent=st["body"],
                                                 fontName="Helvetica-Bold", fontSize=9.4,
                                                 textColor=INK, spaceBefore=6,
                                                 spaceAfter=4))))
            i += 1; continue

        if line.startswith("!!"):
            txt = clean(line[2:])
            k = Table([[Paragraph("KEY COMMITMENT", st["keyh"])],
                       [Paragraph(esc(txt), st["key"])]],
                      colWidths=[avail], hAlign="LEFT")
            k.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), tint(rail, 0.94)),
                ("LINEBEFORE", (0, 0), (0, -1), 2.0, HexColor(rail)),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (0, 0), 7),
                ("BOTTOMPADDING", (0, 0), (0, 0), 1),
                ("TOPPADDING", (0, 1), (0, 1), 0),
                ("BOTTOMPADDING", (0, 1), (0, 1), 8),
            ]))
            main.append(k); main.append(Spacer(1, 9))
            i += 1; continue

        if line.startswith(">>"):
            head = [x.strip() for x in clean(line[2:]).split("|")]
            title, who, rec = (head + ["", ""])[:3]
            i += 1
            acts = []
            while i < n and re.match(r"^\s*[-*\u2022]\s+", lines[i]):
                acts.append(clean(re.sub(r"^\s*[-*\u2022]\s+", "", lines[i]))); i += 1
            step_no += 1
            cell = [Paragraph(esc(title), st["steptitle"])]
            for a in acts:
                cell.append(Paragraph(modal(esc(a)), st["stepact"], bulletText="\u2013"))
            chips = []
            for lab, val in (("WHO", who), ("RECORDS", rec)):
                if val:
                    chips.append(f'<font name="Helvetica-Bold" size="6.4" color="{rail}">'
                                 f'{lab}</font>&nbsp;&nbsp;{esc(val)}')
            if chips:
                cell.append(Spacer(1, 2))
                cell.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;".join(chips), st["stepchip"]))
            t = Table([["", Paragraph(f"{step_no:02d}", st["stmtno"]), cell]],
                      colWidths=[pull, 1.05 * cm, avail - 1.05 * cm], hAlign="LEFT")
            t.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("LINEABOVE", (1, 0), (-1, 0), 0.4, HAIR),
            ]))
            t.splitInRow = 1
            main.append(("RAW", t))
            continue

        if line.startswith("|"):
            blk = []
            while i < n and lines[i].strip().startswith("|"):
                blk.append(lines[i]); i += 1
            rows = []
            for l in blk:
                if re.match(r"^\|[\s:\-|]+\|$", l.strip()):
                    continue
                cells = [clean(x) for x in l.strip().strip("|").split("|")]
                if any(cells):
                    rows.append(cells)
            if not rows:
                continue
            w = max(len(r) for r in rows)
            rows = [r + [""] * (w - len(r)) for r in rows]
            if w == 2:
                cw = [avail * .40, avail * .60]
            elif w == 3:
                cw = [avail * .26, avail * .30, avail * .44]
            else:
                # proportional to longest cell per column, so tick/rating
                # columns stay narrow and text columns get the width
                mx = [max(len(r[j]) for r in rows) for j in range(w)]
                wt = [min(max(m, 6), 34) for m in mx]
                cw = [avail * x / sum(wt) for x in wt]
                floor = min(1.6 * cm, avail / w)
                cw = [max(floor, c) for c in cw]
                s = sum(cw)
                cw = [c * avail / s for c in cw]
            def cellpara(text, style):
                # ¶ marks a paragraph break carried over from the source cell
                return Paragraph(esc(text).replace("¶", "<br/><br/>"), style)

            # a first row of long prose is data, not a header: treating it as a
            # header repeats it on every page, sets it in caps, and makes it
            # unsplittable
            # short cells = a real header row; a first row of long prose is
            # data (a ¶ is fine, headers wrap too)
            hdr_like = len(rows) > 1 and all(len(c) <= 160 for c in rows[0])
            # wide registers need a smaller cell size, or words break mid-word
            # in 1.9 cm columns
            if w >= 10:
                st = dict(st)
                st["cell"] = ParagraphStyle("cellsm", parent=st["cell"],
                                            fontSize=7.2, leading=10)
                st["cellb"] = ParagraphStyle("cellbsm", parent=st["cellb"],
                                             fontSize=7.2, leading=10)
                st["cellh"] = ParagraphStyle("cellhsm", parent=st["cellh"],
                                             fontSize=6.0, leading=8.5)
            data = ([[""] + [cellpara(c.upper(), st["cellh"]) for c in rows[0]]]
                    if hdr_like else [])
            data += [[""] + [cellpara(c, st["cell" if j else "cellb"])
                             for j, c in enumerate(r)]
                     for r in (rows[1:] if hdr_like else rows)]
            # splitInRow lets a single very tall row break across pages instead
            # of failing the whole document (some provider forms have one cell
            # taller than the frame)
            t = Table(data, colWidths=[max(pull - 7, 0)] + cw,
                      repeatRows=1 if hdr_like else 0,
                      hAlign="LEFT", splitByRow=1, splitInRow=1)
            t.setStyle(TableStyle(([
                ("BACKGROUND", (1, 0), (-1, 0), tint(rail, 0.93)),
                ("LINEBELOW", (1, 0), (-1, 0), 0.7, HexColor(rail)),
            ] if hdr_like else []) + [
                ("LINEBELOW", (1, 1 if hdr_like else 0), (-1, -2), 0.3, ROW),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (0, -1), 0),
                ("RIGHTPADDING", (0, 0), (0, -1), 0),
                ("LEFTPADDING", (1, 0), (-1, -1), 7),
                ("RIGHTPADDING", (1, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            main.append(("RAW", t)); main.append(Spacer(1, 10))
            continue

        if line.startswith("%%"):
            # clause carrying its own number, e.g. "%% 1.3.1 text" — the
            # provider's numbering, preserved so cross-references still resolve
            items = []
            while i < n and lines[i].strip().startswith("%%"):
                rawl = lines[i]
                m2 = re.match(r"^%%\s+(\S+)\s+(.*)$", rawl.strip())
                if m2:
                    depth = (len(rawl) - len(rawl.lstrip())) // 2
                    items.append((m2.group(1), clean(m2.group(2)), depth))
                i += 1
            if not items:
                continue
            step = 0.75 * cm
            numw = min(3.2 * cm,
                       max(1.05 * cm,
                           0.2 * cm * max(len(k) for k, _, _ in items)
                           + step * max(d for _, _, d in items)))
            data = []
            for k, v, d in items:
                ind = d * step
                data.append(["",
                             Paragraph(esc(k), ParagraphStyle(
                                 "n%d" % d, parent=st["stmtno"], leftIndent=ind)),
                             Paragraph(esc(v), ParagraphStyle(
                                 "s%d" % d, parent=st["stmt"], leftIndent=ind))])
            t = Table(data, colWidths=[pull, numw, avail - numw], hAlign="LEFT")
            t.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LINEBELOW", (1, 0), (-1, -2), 0.3, ROW),
            ]))
            main.append(("RAW", t)); main.append(Spacer(1, 9))
            continue

        if re.match(r"^\s*\d+[\.\)]\s+", raw):
            steps = []
            while i < n and re.match(r"^\s*\d+[\.\)]\s+", lines[i]):
                steps.append(clean(re.sub(r"^\s*\d+[\.\)]\s+", "", lines[i]))); i += 1
            data = [["", Paragraph(f"{k+1:02d}", st["stmtno"]),
                     Paragraph(esc(s2), st["stmt"])] for k, s2 in enumerate(steps)]
            t = Table(data, colWidths=[pull, 1.05 * cm, avail - 1.05 * cm],
                      hAlign="LEFT")  # steps have no cell padding, so no pull-back
            t.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LINEBELOW", (1, 0), (-1, -2), 0.3, ROW),
            ]))
            main.append(("RAW", t)); main.append(Spacer(1, 9))
            continue

        if re.match(r"^\s*[-*\u2022]\s+", raw):
            items = []
            while i < n and re.match(r"^\s*[-*\u2022]\s+", lines[i]):
                items.append(clean(re.sub(r"^\s*[-*\u2022]\s+", "", lines[i]))); i += 1
            for it in items:
                main.append(Paragraph(esc(it), ParagraphStyle(
                    "li", parent=st["body"], leftIndent=12, bulletIndent=2,
                    spaceAfter=4), bulletText="\u2013"))
            main.append(Spacer(1, 6))
            continue

        main.append(Paragraph(esc(clean(line)), st["body"]))
        i += 1

    flush(title_pending, num_pending)
    return story
