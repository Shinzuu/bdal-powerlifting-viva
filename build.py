#!/usr/bin/env python3
"""Build index.html: the BDAL powerlifting viva guide.

Source code shown on the page is read straight from the project repo at build time, so the
page can never drift from the code that actually ran. Line numbers in the explanations are
resolved by searching for a snippet, and the build fails if a snippet is not found.
"""
import html, json, re, sys
from pathlib import Path

PROJECT = Path.home() / "Documents/study/bdal-powerlifting-analysis"
OUT = Path(__file__).with_name("index.html")

sys.path.insert(0, str(Path(__file__).parent))
import content as C  # noqa: E402

esc = html.escape

# ---------------------------------------------------------------- syntax highlighting
JAVA_KW = set("""package import public private protected class extends implements static final
void return if else for try catch new throws throw null true false double long int boolean
String this super""".split())
JAVA_TYPES = set("""Mapper Reducer Context Text LongWritable Writable DataInput DataOutput IOException
InterruptedException NumberFormatException Configuration Job Path FileInputFormat FileOutputFormat
Iterable Override System MinMaxCountAvgTuple Exception""".split())
PIG_KW = set("""LOAD USING AS FILTER BY AND OR NOT FOREACH GENERATE GROUP ALL ORDER DESC ASC LIMIT
FLATTEN STORE INTO COUNT PigStorage chararray double int""".split())
TOKEN = re.compile(r'(//.*|--.*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\$\d+|@\w+|\b\d+(?:\.\d+)?\b|\b\w+\b|\s+|.)')


def highlight(line, lang):
    out = []
    for m in TOKEN.finditer(line):
        t = m.group(0)
        e = esc(t)
        if (lang == "java" and t.startswith("//")) or (lang == "pig" and t.startswith("--")):
            out.append(f'<span class="c-com">{e}</span>')
        elif t[:1] in "\"'" and len(t) > 1:
            out.append(f'<span class="c-str">{e}</span>')
        elif t.startswith("$") and len(t) > 1:
            out.append(f'<span class="c-pos">{e}</span>')
        elif t.startswith("@"):
            out.append(f'<span class="c-ann">{e}</span>')
        elif re.fullmatch(r"\d+(?:\.\d+)?", t):
            out.append(f'<span class="c-num">{e}</span>')
        elif lang == "java" and t in JAVA_KW:
            out.append(f'<span class="c-kw">{e}</span>')
        elif lang == "java" and t in JAVA_TYPES:
            out.append(f'<span class="c-type">{e}</span>')
        elif lang == "pig" and t in PIG_KW:
            out.append(f'<span class="c-kw">{e}</span>')
        else:
            out.append(e)
    return "".join(out)


def code_block(relpath, notes, title=None):
    """Render a real source file with numbered notes pinned to lines found by snippet."""
    path = PROJECT / relpath
    lines = path.read_text().splitlines()
    lang = "pig" if relpath.endswith(".pig") else "java"
    pinned = {}   # line number -> note index
    items = []
    for i, (snippet, note) in enumerate(notes, 1):
        hits = [n for n, l in enumerate(lines, 1) if snippet in l]
        if not hits:
            sys.exit(f"snippet not found in {relpath}: {snippet!r}")
        n = hits[0]
        pinned.setdefault(n, i)
        items.append(f'<li><span class="lnref">line {n}</span> {note}</li>')
    rows = []
    for n, l in enumerate(lines, 1):
        badge = f'<span class="pin">{pinned[n]}</span>' if n in pinned else '<span class="pin blank"></span>'
        cls = ' class="hl"' if n in pinned else ""
        rows.append(f'<span{cls}><span class="ln">{n}</span>{badge}{highlight(l, lang) or " "}</span>')
    head = esc(title or relpath)
    notes_html = f'<ol class="notes">{"".join(items)}</ol>' if items else ""
    return (f'<figure class="code"><figcaption><span class="file">{head}</span>'
            f'<span class="lang">{lang}</span></figcaption>'
            f'<pre><code>{"".join(rows)}</code></pre>{notes_html}</figure>')


def shell(cmds):
    """A terminal-style block. cmds: list of (command, comment)."""
    rows = []
    for cmd, note in cmds:
        c = f'<span class="c-com">  # {esc(note)}</span>' if note else ""
        rows.append(f'<span><span class="prompt">$</span> {esc(cmd)}{c}</span>')
    return f'<pre class="term"><code>{"".join(rows)}</code></pre>'


# ---------------------------------------------------------------- small SVG charts
def hbar(title, data, unit="", fmt="{:,}"):
    w, row, left, right = 640, 30, 170, 110
    h = 34 + row * len(data)
    mx = max(v for _, v in data)
    parts = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}" class="chart">',
             f'<text x="0" y="18" class="ch-title">{esc(title)}</text>']
    for i, (k, v) in enumerate(data):
        y = 34 + i * row
        bw = max(2, (w - left - right) * v / mx)
        parts.append(f'<text x="{left - 10}" y="{y + 18}" text-anchor="end" class="ch-lbl">{esc(k)}</text>')
        parts.append(f'<rect x="{left}" y="{y + 5}" width="{bw:.1f}" height="18" rx="4" class="ch-bar"/>')
        parts.append(f'<text x="{left + bw + 8:.1f}" y="{y + 18}" class="ch-val">{fmt.format(v)}{unit}</text>')
    parts.append("</svg>")
    return f'<div class="figwrap">{"".join(parts)}</div>'


# ---------------------------------------------------------------- page
def build():
    C.code_block, C.shell, C.hbar = code_block, shell, hbar
    sections = C.sections()
    nav = "".join(f'<a href="#{sid}">{esc(label)}</a>' for sid, label, _ in sections)
    body = "".join(f'<section id="{sid}">{inner}</section>' for sid, _, inner in sections)
    data = json.dumps({"mcq": C.MCQ, "blanks": C.BLANKS, "drill": C.DRILL}, ensure_ascii=False)
    page = (Path(__file__).with_name("template.html").read_text()
            .replace("{{NAV}}", nav).replace("{{BODY}}", body).replace("{{DATA}}", data)
            .replace("{{HERO}}", C.HERO))
    OUT.write_text(page)
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB, {len(sections)} sections)")


if __name__ == "__main__":
    build()
