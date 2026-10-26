#!/usr/bin/env python3
"""Newly issued business licenses from a city's open-data portal (Socrata). Standard library only.

  python3 new_licenses.py find "Chicago"
      → business-license datasets on public Socrata portals matching the place (domain, id, name, last updated)
  python3 new_licenses.py pull data.cityofchicago.org r5kz-chrr [--days 30] [--limit 200] [--match "food|salon"]
          [--where "application_type='ISSUE'"] [--out new.json]
      → the newest licenses: {name, category, date, address, home_based, raw_id}, newest first

The date / name / category / address columns are detected from the dataset's own column list. Check the printed
column choice the first time you use a dataset; override with --date-col / --name-col / --cat-col / --addr-col.
Rows that look home-based are flagged (home_based: true): never use a home address for outreach.
"""
import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import date, timedelta

UA = {"User-Agent": "local-client-finder/1.0 (+https://github.com/WordRocket/local-client-finder)"}

DATE_PREF = ["date_issued", "issue_date", "issued_date", "license_issue_date", "first_iss_dt", "license_start_date",
             "start_date", "business_start_date", "application_date", "creation_date", "created_date", "open_date"]
NAME_PREF = ["doing_business_as_name", "dba_name", "dba", "trade_name", "tradename", "business_name", "businessname",
             "legal_name", "name", "company_name"]
CAT_PREF = ["license_description", "licencetypes", "license_type", "licensetype", "business_activity", "category",
            "naics_description", "business_type", "description", "license_category"]
ADDR_PREF = ["address", "business_address", "street_address", "site_address", "location_address", "full_address"]
HOME_HINT = re.compile(r"home|residen", re.I)


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def find(place):
    q = urllib.parse.urlencode({"q": place + " business licenses", "only": "datasets", "limit": 20})
    res = get("https://api.us.socrata.com/api/catalog/v1?" + q).get("results", [])
    rows = []
    for r in res:
        name = r["resource"]["name"]
        if not re.search(r"licen[cs]e|business|registr", name, re.I):
            continue
        rows.append((r["metadata"]["domain"], r["resource"]["id"], name, (r["resource"].get("data_updated_at") or "")[:10]))
    if not rows:
        print("No Socrata dataset found. Web search '<city> open data business licenses' (the city may use another "
              "portal such as ArcGIS or CKAN), or use the other sources in references/sources.md.")
    for d in rows:
        print("%-32s %-10s %-60s updated %s" % d)


def pick(cols, prefs, types=None):
    by = {c["fieldName"]: c for c in cols}
    for p in prefs:
        if p in by and (types is None or by[p]["dataTypeName"] in types):
            return p
    for p in prefs:  # partial match
        for f, c in by.items():
            if p in f and (types is None or c["dataTypeName"] in types):
                return f
    return None


def pull(domain, ds, days, limit, match, out, overrides):
    meta = get("https://%s/api/views/%s.json" % (domain, ds))
    cols = [c for c in meta.get("columns", []) if not c["fieldName"].startswith(":")]
    date_col = overrides.date_col or pick(cols, DATE_PREF, {"calendar_date", "date", "floating_timestamp"}) \
        or next((c["fieldName"] for c in cols if c["dataTypeName"] in ("calendar_date", "floating_timestamp")), None)
    name_col = overrides.name_col or pick(cols, NAME_PREF, {"text"})
    cat_col = overrides.cat_col or pick(cols, CAT_PREF, {"text"})
    addr_col = overrides.addr_col or pick(cols, ADDR_PREF, {"text"})
    home_col = next((c["fieldName"] for c in cols if HOME_HINT.search(c["fieldName"])), None)
    print("dataset: %s | date=%s name=%s category=%s address=%s home=%s" % (
        meta.get("name"), date_col, name_col, cat_col, addr_col, home_col), file=sys.stderr)
    if not (date_col and name_col):
        sys.exit("Couldn't find a date and a name column. Columns: " + ", ".join(c["fieldName"] for c in cols))
    since = (date.today() - timedelta(days=days)).isoformat()
    where = "%s >= '%sT00:00:00'" % (date_col, since)
    if overrides.where:
        where += " AND (%s)" % overrides.where
    params = {"$where": where, "$order": "%s DESC" % date_col, "$limit": str(limit)}
    rows = get("https://%s/resource/%s.json?%s" % (domain, ds, urllib.parse.urlencode(params)))
    outrows, seen = [], set()
    for r in rows:
        name = (r.get(name_col) or "").strip()
        cat = (r.get(cat_col) or "") if cat_col else ""
        if isinstance(cat, list):
            cat = ", ".join(map(str, cat))
        cat = re.sub(r"\s+", " ", str(cat)).strip()
        if not name or name.lower() in seen:
            continue
        if match and not re.search(match, name + " " + str(cat), re.I):
            continue
        seen.add(name.lower())
        home = False
        if home_col:
            hv = str(r.get(home_col, "")).strip().lower()
            home = hv in ("y", "yes", "true", "1") or "home" in hv
        if HOME_HINT.search(str(cat)):
            home = True
        addr = r.get(addr_col, "") if addr_col else ""
        outrows.append({"name": name, "category": str(cat)[:120], "date": str(r.get(date_col, ""))[:10],
                        "address": "" if home else (addr if isinstance(addr, str) else ""), "home_based": home})
    for r in outrows[:60]:
        print("%s  %-45s %-45s %s" % (r["date"], r["name"][:45], r["category"][:45], "HOME-BASED" if r["home_based"] else ""))
    print("\n%d new licenses since %s%s" % (len(outrows), since, " matching /%s/" % match if match else ""), file=sys.stderr)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(outrows, f, indent=1)
        print(out, file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("find")
    f.add_argument("place")
    p = sub.add_parser("pull")
    p.add_argument("domain")
    p.add_argument("dataset")
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--limit", type=int, default=500)
    p.add_argument("--match", default="")
    p.add_argument("--out", default="")
    for c in ("date-col", "name-col", "cat-col", "addr-col"):
        p.add_argument("--" + c, default="")
    p.add_argument("--where", default="", help="extra SoQL filter, e.g. \"application_type='ISSUE'\" (Chicago: new, not renewals)")
    a = ap.parse_args()
    if a.cmd == "find":
        find(a.place)
    else:
        pull(a.domain, a.dataset, a.days, a.limit, a.match, a.out, a)


if __name__ == "__main__":
    main()
