#!/usr/bin/env python3
"""Keep every page under dossier/ navigable on GitHub Pages.

The dossier was written for a host that served it from the site root, one
extensionless URL per page. Pages serves it from /rise-knowledge-base/dossier/
with one folder per page, so a link written for the old host either leaves the
site ("/rise-front-door") or resolves inside the wrong folder
("rise-graph-explorer.html" from inside rise-node-map/). Pages opened from the
maps also carried no route back to the dossier or to their own node.

    python3 dossier/nav/wayback.py repair   rewrite links that only worked on the old host
    python3 dossier/nav/wayback.py stamp    add or refresh the way back on every page
    python3 dossier/nav/wayback.py check    fail on any dead link or any page with no way back

repair and stamp are idempotent and write nothing if anything is unresolved.
Run check before every push.
"""
import os
import re
import sys
import urllib.parse
from pathlib import Path

DOSSIER = Path(__file__).resolve().parents[1]
REPO = DOSSIER.parent
FRONT = DOSSIER / "index.html"
SUITE = DOSSIER / "suite"
SUITE_SOURCE = REPO / "rise-ndis-package" / "suite"
BRIEFS_SOURCE = REPO / "rise-dossier-bundle"
NODE_MAP = DOSSIER / "rise-node-map" / "index.html"
ENGINE_MAP = DOSSIER / "rise-engine-map" / "index.html"

ATTR = re.compile(r"""\b(href|src)(\s*=\s*)(["'])(.*?)\3""", re.S)
NOT_LOCAL = re.compile(r"(?:[a-z][a-z0-9+.-]*:|//|#)", re.I)
BUILT_IN_SCRIPT = re.compile(r"""['"]\s*\+|\+\s*['"]|\$\{""")
BLOB = re.compile(r"data:[a-z]+/[a-z0-9.+-]+;base64,([A-Za-z0-9+/=]{200,})")
DOC_ID = re.compile(r"^([A-Za-z]{3}-[A-Za-z0-9]{2,4}-\d+)")

# Links the node map assembles in script, so no attribute scan can see them
# whole. Each pair is (as written for the old host, as Pages needs it).
SCRIPT_LINKS = {
    NODE_MAP: [
        ('const DOCBASE="suite/";', 'const DOCBASE="../suite/";'),
        ("<a href=\"index.html#doc-'+id+'\">", "<a href=\"../index.html#doc-'+id+'\">"),
        ("<a href=\"index.html#std-'+id+'\">", "<a href=\"../index.html#std-'+id+'\">"),
    ],
}

START, END = "<!-- wayback:start -->", "<!-- wayback:end -->"
STAMPED = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
# Sections of the front page a tool page can belong to, most specific first.
HOME_SECTIONS = ("ladder", "tools", "auditor", "how", "notes", "paths", "dev")


def pages():
    """Every dossier page, less the rendered views _kb/build_kb.py owns: those
    sit beside their source (build_map.py.html beside build_map.py)."""
    return sorted(
        p for p in DOSSIER.rglob("*.html")
        if not p.with_suffix("").is_file() and not p.with_suffix(".md").is_file()
    )


def read(page):
    return page.read_text(encoding="utf-8")


def split(value):
    path, _, frag = value.partition("#")
    return urllib.parse.unquote(path.partition("?")[0]), frag


def target_of(page, value):
    """The file a local link lands on when Pages serves it, or None if dead."""
    path, _ = split(value)
    if path == "":
        return page
    if path.startswith("/"):
        return None
    hit = (page.parent / path).resolve()
    if REPO not in hit.parents and hit != REPO:
        return None
    if hit.is_dir():
        hit = hit / "index.html"
    return hit if hit.is_file() else None


def link_to(page, target, frag=""):
    """Relative link from page to target, folder pages as folder URLs."""
    if target.name == "index.html" and target != FRONT:
        rel = os.path.relpath(target.parent, page.parent) + "/"
    else:
        rel = os.path.relpath(target, page.parent)
    return rel + ("#" + frag if frag else "")


def repaired(page, value):
    """Where a dead link was meant to go, or None if no rule knows."""
    path, frag = split(value)
    name = Path(path).name
    if path == "/":
        # Suite pages label this link "Rise Knowledge Base": that is the repo index.
        home = REPO / "index.html" if SUITE in page.parents else FRONT
        return os.path.relpath(home, page.parent) + ("#" + frag if frag else "")
    if path == "../kb.css" and SUITE in page.parents:
        return link_to(page, SUITE / "kb.css")
    if path.endswith(".md"):
        if SUITE in page.parents:
            folder = page.relative_to(SUITE).parts[0]
            source = SUITE_SOURCE / folder / name
        else:
            source = BRIEFS_SOURCE / (Path(name).stem + ".html")
        return link_to(page, source, frag) if source.is_file() else None
    flat = path.startswith("/") or "/" not in path
    if flat:
        stem = path.strip("/")
        stem = stem[:-5] if stem.endswith(".html") else stem
        home = DOSSIER / stem / "index.html"
        if stem and home.is_file():
            return link_to(page, home, frag)
    return None


def assert_blobs_untouched(page, before, after):
    if BLOB.findall(before) != BLOB.findall(after):
        sys.exit(f"REFUSED {page.relative_to(REPO)}: an embedded image would have changed")


def repair():
    plan, unresolved = {}, []
    for page in pages():
        before = read(page)
        changed = 0

        def fix(m):
            nonlocal changed
            attr, eq, quote, value = m.groups()
            if not value or NOT_LOCAL.match(value) or BUILT_IN_SCRIPT.search(value):
                return m.group(0)
            if target_of(page, value):
                return m.group(0)
            better = repaired(page, value)
            if better is None:
                unresolved.append((page, value))
                return m.group(0)
            changed += 1
            return f"{attr}{eq}{quote}{better}{quote}"

        after = ATTR.sub(fix, before)
        for old, new in SCRIPT_LINKS.get(page, []):
            if after.count(new) == 1 and after.count(old) == 0:
                continue
            if after.count(old) != 1:
                unresolved.append((page, f"script link, expected once: {old}"))
                continue
            after = after.replace(old, new)
            changed += 1
        if changed:
            assert_blobs_untouched(page, before, after)
            plan[page] = (after, changed)
    if unresolved:
        for page, value in unresolved:
            print(f"UNRESOLVED {page.relative_to(REPO)}: {value}")
        sys.exit(f"{len(unresolved)} links have no repair rule. Nothing written.")
    for page, (after, _) in plan.items():
        page.write_text(after, encoding="utf-8")
    print(f"repaired {sum(n for _, n in plan.values())} links in {len(plan)} pages")


def doc_id(page):
    name = page.parent.name if page.name == "index.html" else page.name
    m = DOC_ID.match(name)
    return m.group(1).upper() if m else None


def home_section(page, front):
    folder = page.parent.name
    for section in HOME_SECTIONS:
        m = re.search(rf'<section id="{section}".*?</section>', front, re.S)
        if m and re.search(rf'href="(?:\./)?{re.escape(folder)}/"', m.group(0)):
            return section
    return ""


def way_back(page, front):
    """The stamped block for a page, or None if the page needs none."""
    if page in (FRONT, ENGINE_MAP):
        return None  # the front page is home; the engine map carries its own
    if SUITE in page.parents:
        did = doc_id(page)
        if did is None:
            return None
        # Labels are unbreakable so the breadcrumb wraps between links, not inside one.
        node = link_to(page, NODE_MAP) + "index.html#focus=" + did
        engine = link_to(page, ENGINE_MAP) + "index.html#focus=" + did
        return (
            f'{START}<a href="{link_to(page, FRONT, "doc-" + did)}" target="_top">&#8592;&nbsp;The&nbsp;dossier</a>'
            f'<span class="sep">/</span><a href="{node}" target="_top">Show&nbsp;on&nbsp;the&nbsp;node&nbsp;map</a>'
            f'<span class="sep">/</span><a href="{engine}" target="_top">Show&nbsp;on&nbsp;the&nbsp;engine&nbsp;map</a>'
            f'<span class="sep">/</span>{END}'
        )
    css = os.path.relpath(DOSSIER / "nav" / "wayback.css", page.parent)
    home = link_to(page, FRONT, home_section(page, front))
    # A page with no .wrap column of its own runs edge to edge, like the node map.
    column = "wrap" if re.search(r"\.wrap\s*[,{]", read(page)) else "wayback-edge"
    return (
        f'{START}<link rel="stylesheet" href="{css}">'
        f'<nav class="wayback" aria-label="Way back"><div class="{column}">'
        f'<a href="{home}" target="_top">&#8592; The dossier</a></div></nav>{END}'
    )


def stamp():
    front = read(FRONT)
    plan, unresolved = {}, []
    for page in pages():
        block = way_back(page, front)
        if block is None:
            continue
        before = read(page)
        bare = STAMPED.sub("", before)
        anchor = r'<div class="kbbar">' if SUITE in page.parents else r"<body[^>]*>"
        found = re.findall(anchor, bare)
        if len(found) != 1:
            unresolved.append((page, f"expected one {anchor}, found {len(found)}"))
            continue
        after = re.sub(anchor, lambda m: m.group(0) + block, bare, count=1)
        if after != before:
            assert_blobs_untouched(page, before, after)
            plan[page] = after
    if unresolved:
        for page, why in unresolved:
            print(f"UNRESOLVED {page.relative_to(REPO)}: {why}")
        sys.exit(f"{len(unresolved)} pages could not be stamped. Nothing written.")
    for page, after in plan.items():
        page.write_text(after, encoding="utf-8")
    print(f"stamped {len(plan)} pages")


def anchors(page, cache={}):
    if page not in cache:
        cache[page] = set(re.findall(r"""\b(?:id|name)\s*=\s*["']([^"']+)["']""", read(page)))
    return cache[page]


def map_ids():
    node = set(re.findall(r'<g\b[^>]*\bclass="nd\b[^"]*"[^>]*\bid="([^"]+)"', read(NODE_MAP)))
    engine = set(re.findall(r'"id":\s*"([^"]+)"', read(ENGINE_MAP)))
    return {NODE_MAP: node, ENGINE_MAP: engine}


def check():
    faults = []
    focusable = map_ids()
    for page in pages():
        text = read(page)
        where = page.relative_to(REPO)
        for _, _, _, value in ATTR.findall(text):
            if not value or NOT_LOCAL.match(value):
                continue
            built = BUILT_IN_SCRIPT.search(value)
            if built:
                value = value[: built.start()].rstrip("'\"")
                if not value:
                    continue
            hit = target_of(page, value)
            if hit is None:
                faults.append(f"{where}: dead link {value}")
                continue
            _, frag = split(value)
            if not frag or built or hit.suffix != ".html":
                continue
            if frag.startswith("focus="):
                if frag[6:] not in focusable.get(hit, ()):
                    faults.append(f"{where}: {hit.parent.name} has no node {frag[6:]}")
            elif frag not in anchors(hit):
                faults.append(f"{where}: {value} names an anchor that is not on the page")
        if page not in (FRONT, ENGINE_MAP) and START not in text:
            faults.append(f"{where}: no way back")
    text = read(NODE_MAP)
    base = re.search(r'const DOCBASE="([^"]*)"', text).group(1)
    for did, source in re.findall(r'"([A-Z]{3}-[A-Z0-9]{2,4}-\d+)":"(\d\d-[^"]+\.md)"', text):
        doc = base + source[:-3] + ".html"
        if target_of(NODE_MAP, doc) is None:
            faults.append(f"{NODE_MAP.relative_to(REPO)}: node {did} opens a dead page {doc}")
        if "doc-" + did not in anchors(FRONT):
            faults.append(f"{NODE_MAP.relative_to(REPO)}: node {did} has no register row on the front page")
    for doc in set(re.findall(r'"doc":\s*"([^"]+)"', read(ENGINE_MAP))):
        if target_of(ENGINE_MAP, "../" + doc) is None:
            faults.append(f"{ENGINE_MAP.relative_to(REPO)}: opens a dead page {doc}")
    for fault in faults:
        print(fault)
    if faults:
        sys.exit(f"{len(faults)} faults in {len(pages())} pages")
    print(f"ok: {len(pages())} pages, every local link lands, every page has a way back")


if __name__ == "__main__":
    commands = {"repair": repair, "stamp": stamp, "check": check}
    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        sys.exit(__doc__)
    commands[sys.argv[1]]()
