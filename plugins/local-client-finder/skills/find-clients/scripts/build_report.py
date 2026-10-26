#!/usr/bin/env python3
"""Lead list (JSON) -> leads-<slug>.csv + leads-<slug>.html. Standard library only.

Usage: python3 build_report.py leads.json --title "pressure washing in Tulsa OK" [--out DIR]

leads.json: a list of rows (or {"rows": [...]}) with any of these fields:
  name, category, rating, reviews, phone, website, status, score, why, opener, maps_url
"""
import argparse
import csv
import html
import json
import os
import re
from datetime import date

FIELDS = ["score", "name", "status", "rating", "reviews", "category", "phone", "website", "why", "opener", "maps_url"]
STATUS_COLOR = {
    "NO SITE": "#c0392b",
    "FACEBOOK ONLY": "#d35400",
    "SITE NOT LINKED": "#2c7be5",
    "WEAK SITE": "#7f8c8d",
}


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "leads"


def load_rows(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    rows = data.get("rows", []) if isinstance(data, dict) else data
    rows = [r for r in rows if isinstance(r, dict) and r.get("name")]
    rows.sort(key=lambda r: (-(r.get("score") or 0), -(r.get("reviews") or 0)))
    return rows


def write_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})


def cell(value):
    return html.escape("" if value is None else str(value))


def write_html(rows, title, path):
    no_site = sum(1 for r in rows if (r.get("status") or "").upper() in ("NO SITE", "FACEBOOK ONLY"))
    body = []
    for i, r in enumerate(rows, 1):
        status = (r.get("status") or "").upper()
        color = STATUS_COLOR.get(status, "#555")
        phone = r.get("phone") or ""
        tel = re.sub(r"[^\d+]", "", phone)
        maps = r.get("maps_url") or ""
        site = r.get("website") or ""
        phone_html = '<a href="tel:%s">%s</a>' % (cell(tel), cell(phone)) if tel else ""
        links = [cell(site)] if site else []
        if maps:
            links.append('<a href="%s" target=_blank>Maps</a>' % cell(maps))
        links_html = " · ".join(links)
        opener_html = "<details><summary>Opener</summary>%s</details>" % cell(r.get("opener")) if r.get("opener") else ""
        body.append(
            "<tr>"
            f"<td class=n>{i}</td>"
            f"<td class=n><b>{cell(r.get('score'))}</b></td>"
            f"<td><b>{cell(r.get('name'))}</b><div class=sub>{cell(r.get('category'))}</div></td>"
            f"<td><span class=pill style='background:{color}'>{cell(status or '?')}</span></td>"
            f"<td class=n>{cell(r.get('rating'))}</td>"
            f"<td class=n>{cell(r.get('reviews'))}</td>"
            f"<td>{phone_html}</td>"
            f"<td>{links_html}</td>"
            f"<td class=why>{cell(r.get('why'))}{opener_html}</td>"
            "</tr>"
        )
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Leads: {cell(title)}</title>
<style>
:root{{--bg:#faf8f4;--ink:#1d1d1f;--muted:#6b6b70;--line:#e6e2da;--card:#fff}}
@media (prefers-color-scheme: dark){{:root{{--bg:#151517;--ink:#f2f2f2;--muted:#a1a1a6;--line:#2c2c30;--card:#1d1d20}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif}}
main{{max-width:1200px;margin:0 auto;padding:28px 16px 60px}}
h1{{margin:0 0 4px;font-size:26px}} .meta{{color:var(--muted);margin-bottom:20px}}
.wrap{{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:12px}}
table{{border-collapse:collapse;width:100%;min-width:900px}}
th,td{{padding:10px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}
th{{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);cursor:pointer;user-select:none;position:sticky;top:0;background:var(--card)}}
td.n{{text-align:right;white-space:nowrap}} .sub{{color:var(--muted);font-size:13px}}
.pill{{color:#fff;font-size:11px;font-weight:700;padding:3px 8px;border-radius:99px;white-space:nowrap}}
.why{{max-width:360px}} details{{margin-top:6px;color:var(--muted)}} summary{{cursor:pointer;color:var(--ink)}}
a{{color:#2c7be5}} footer{{color:var(--muted);font-size:13px;margin-top:16px}}
</style></head><body><main>
<h1>Leads: {cell(title)}</h1>
<div class=meta>{len(rows)} leads · {no_site} with no website or Facebook only · {date.today().isoformat()} · from public Google Maps listings</div>
<div class=wrap><table id=t><thead><tr>
<th>#</th><th>Score</th><th>Business</th><th>Status</th><th>Rating</th><th>Reviews</th><th>Phone</th><th>Links</th><th>Why + opener</th>
</tr></thead><tbody>
{''.join(body)}
</tbody></table></div>
<footer>Public business listing data only. Contact businesses one at a time and follow your local anti-spam rules.
Want a preview site to show your #1 lead? <a href="https://app.ranksite.ai" target=_blank>RankSite</a> builds one from their Google listing.</footer>
</main>
<script>
document.querySelectorAll('#t th').forEach((th,i)=>th.addEventListener('click',()=>{{
  const tb=document.querySelector('#t tbody'); const rows=[...tb.rows]; const asc=th.dataset.asc!=='1'; th.dataset.asc=asc?'1':'0';
  const v=r=>{{const t=r.cells[i].innerText.trim(); const n=parseFloat(t.replace(/,/g,'')); return isNaN(n)?t.toLowerCase():n}};
  rows.sort((a,b)=>{{const x=v(a),y=v(b); return (x>y?1:x<y?-1:0)*(asc?1:-1)}}); rows.forEach(r=>tb.appendChild(r));
}}));
</script></body></html>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(page)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("json_path")
    ap.add_argument("--title", default="local leads")
    ap.add_argument("--out", default=".")
    args = ap.parse_args()
    rows = load_rows(args.json_path)
    os.makedirs(args.out, exist_ok=True)
    slug = slugify(args.title)
    csv_path = os.path.join(args.out, f"leads-{slug}.csv")
    html_path = os.path.join(args.out, f"leads-{slug}.html")
    write_csv(rows, csv_path)
    write_html(rows, args.title, html_path)
    print(csv_path)
    print(html_path)


if __name__ == "__main__":
    main()
