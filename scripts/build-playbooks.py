#!/usr/bin/env python3
"""Turn a playbook .md into a styled .html and a Letter-size .pdf (headless Chrome). Standard library only.

  python3 scripts/build-playbooks.py playbooks/niche-and-offer-worksheet.md [more.md ...]

Handles the markdown the playbooks use: # / ## / ### headings, paragraphs, - and 1. lists, > quotes, | tables |,
---, **bold**, *italic*, `code`.
"""
import html
import os
import re
import subprocess
import sys

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CSS = """body{margin:0;background:#fff;font-family:Inter,-apple-system,Helvetica,Arial,sans-serif;color:#1d1d1f}
.page{max-width:760px;margin:0 auto;padding:44px 40px}
h1{font-size:32px;line-height:1.15;margin:0 0 12px;letter-spacing:-0.5px}
h2{font-size:20px;margin:30px 0 10px}
h3{font-size:16px;margin:22px 0 8px}
p,li{font-size:14.5px;line-height:1.55;color:#333}
ul,ol{padding-left:24px;margin:6px 0 12px}li{margin:0 0 6px}
blockquote{margin:12px 0;padding:10px 14px;background:#f4f7ff;border-left:4px solid #3b82f6;border-radius:6px}
blockquote p{margin:0;color:#1d1d1f}
table{border-collapse:collapse;width:100%;margin:10px 0 14px;font-size:13px}
th,td{border:1px solid #e3e3e3;padding:7px 8px;text-align:left;vertical-align:top;color:#333}
th{background:#f6f6f7;font-weight:700;color:#1d1d1f}
td:empty::after{content:"\\00a0";display:inline-block;height:18px}
code{font-family:ui-monospace,Menlo,monospace;font-size:12.5px;background:#eef8f4;color:#0b6b52;border-radius:4px;padding:1px 5px}
hr{border:none;border-top:1px solid #e5e5e5;margin:26px 0}
.foot p{font-size:12px;color:#777}
@page{size:Letter;margin:14mm}"""


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![*\w])\*([^*]+)\*(?![*\w])", r"<i>\1</i>", t)
    return t


def convert(md):
    lines = md.split("\n")
    out, i, title = [], 0, ""
    para = []

    def flush():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            flush(); i += 1; continue
        m = re.match(r"^(#{1,3}) (.*)", ln)
        if m:
            flush()
            lvl = len(m.group(1))
            if lvl == 1 and not title:
                title = m.group(2)
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>"); i += 1; continue
        if ln.strip() == "---":
            flush(); out.append("<hr>"); i += 1; continue
        if ln.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                is_sep = any(c for c in cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c)
                if not is_sep:
                    rows.append(cells)
                i += 1
            t = ["<table><tr>" + "".join(f"<th>{inline(c)}</th>" for c in rows[0]) + "</tr>"]
            for r in rows[1:]:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            out.append("".join(t) + "</table>"); continue
        if ln.startswith(">"):
            flush()
            paras, cur = [], []
            while i < len(lines) and lines[i].startswith(">"):
                t = lines[i].lstrip(">").strip()
                if t:
                    cur.append(t)
                elif cur:
                    paras.append(cur); cur = []
                i += 1
            if cur:
                paras.append(cur)
            out.append("<blockquote>" + "".join('<p style="margin:0 0 8px">' + inline(" ".join(c)) + "</p>" for c in paras)
                       + "</blockquote>"); continue
        m = re.match(r"^(\s*)(- |\d+\. )(.*)", ln)
        if m:
            flush()
            ordered = m.group(2)[0].isdigit()
            items = []
            while i < len(lines):
                mm = re.match(r"^(\s*)(- |\d+\. )(.*)", lines[i])
                if mm:
                    items.append(mm.group(3)); i += 1
                elif lines[i].startswith("  ") and lines[i].strip() and items:
                    items[-1] += " " + lines[i].strip(); i += 1
                else:
                    break
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>"); continue
        para.append(ln.strip()); i += 1
    flush()
    body = "\n".join(out)
    # the text after the last <hr> is the footer
    if "<hr>" in body:
        head, _, foot = body.rpartition("<hr>")
        body = head + '<hr><div class="foot">' + foot + "</div>"
    return title, body


def build(md_path):
    md = open(md_path, encoding="utf-8").read()
    title, body = convert(md)
    base = os.path.splitext(md_path)[0]
    page = (f'<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title>'
            f"<style>{CSS}</style></head><body><div class=\"page\">{body}</div></body></html>")
    with open(base + ".html", "w", encoding="utf-8") as f:
        f.write(page)
    pdf = os.path.abspath(base + ".pdf")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", "file://" + os.path.abspath(base + ".html")],
                   check=True, capture_output=True)
    print(f"{base}.html + .pdf ({os.path.getsize(pdf) / 1024:.0f} KB)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for p in sys.argv[1:]:
        build(p)
