#!/usr/bin/env python3
"""Check business websites the way a normal visitor's browser would, and report hard, visible problems.

Usage:
  python3 check_sites.py leads.json [--out checked.json] [--workers 8]
  python3 check_sites.py example.com another.com

leads.json: a list of rows (or {"rows": [...]}) with a "website" field (hostname or URL); other fields are kept.
Only the public homepage is loaded (plus the plain-http version, to see if it redirects to https).
No scanning, no logins, no probing of other paths. Standard library only.

Each row gets "check": {issues: [...], severity, https, status, final_url, cert_error, copyright_year,
mobile_viewport, generator, powered_by, load_seconds}. Issue codes:
  DOWN        the domain doesn't resolve (expired or misconfigured domain)
  ERROR       the homepage returns an error (HTTP 5xx/4xx) or shows a PHP/WordPress/database error
  PARKED      parked, for sale, suspended or expired-hosting page
  NOT SECURE  no working https (browsers show "Not secure"), or the certificate is expired/invalid
  DATED       hard signs of age: old copyright year, no mobile viewport, Flash, EOL PHP, very old WordPress
  SLOW        homepage took more than 6 seconds to load
  BLOCKED     a firewall/bot check stopped us: unknown, check it in a real browser (never pitch on this)
  CHECK       the script couldn't load it (timeout, dropped connection): often a firewall; open it in a browser
"""
import argparse
import concurrent.futures as cf
import json
import re
import socket
import ssl
import sys
import time
import urllib.error
import urllib.request
from datetime import date

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
TIMEOUT = 15
MAX_BYTES = 400_000
THIS_YEAR = date.today().year

ERROR_SIGNS = [
    ("Error establishing a database connection", "database connection error"),
    ("There has been a critical error on this website", "WordPress critical error"),
    ("Fatal error</b>:", "PHP fatal error"), ("Fatal error: ", "PHP fatal error"),
    ("Parse error</b>:", "PHP parse error"),
    ("Warning</b>:", "PHP warning shown on the page"),
    ("Deprecated</b>:", "PHP deprecation notice shown on the page"),
    ("Notice</b>:  Undefined", "PHP notice shown on the page"),
    ("<title>Index of /", "raw file listing instead of a homepage"),
    ("Apache2 Ubuntu Default Page", "server default page, no site installed"),
    ("<title>Welcome to nginx!</title>", "server default page, no site installed"),
]
PARKED_SIGNS = [
    ("This domain is for sale", "domain for sale"), ("domain may be for sale", "domain for sale"),
    ("Buy this domain", "domain for sale"), ("is for sale!", "domain for sale"),
    ("Future home of something quite cool", "parked domain (no site)"),
    ("parkingcrew", "parked domain (no site)"), ("sedoparking", "parked domain (no site)"),
    ("This Account has been suspended", "hosting account suspended"),
    ("Account Suspended", "hosting account suspended"),
    ("Website Expired", "website/hosting expired"), ("This site has expired", "website/hosting expired"),
    ("domain has expired", "domain expired"),
    ("This domain isn't connected to a site", "domain not connected to any site (Wix)"),
    ("Reconnect Your Domain", "domain not connected to any site"),
]
BLOCK_SIGNS = ["Just a moment...", "cf-chl", "Attention Required! | Cloudflare", "captcha", "Access denied"]


def norm_host(website):
    w = (website or "").strip()
    w = re.sub(r"^https?://", "", w, flags=re.I)
    return w.split("/")[0].split("?")[0].strip().lower()


def fetch(url, verify=True):
    ctx = ssl.create_default_context()
    if not verify:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*;q=0.8",
                                               "Accept-Language": "en-US,en;q=0.8"})
    t0 = time.time()
    try:
        resp = urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx)
        status = resp.status
    except urllib.error.HTTPError as e:
        resp, status = e, e.code
    body = resp.read(MAX_BYTES).decode("utf-8", "replace")
    return {"status": status, "final_url": resp.geturl(), "headers": dict(resp.headers or {}),
            "body": body, "seconds": round(time.time() - t0, 1)}


def classify_exc(e):
    text = str(getattr(e, "reason", e))
    if isinstance(getattr(e, "reason", None), ssl.SSLCertVerificationError) or "CERTIFICATE_VERIFY_FAILED" in text:
        m = re.search(r"certificate verify failed: ([^(]+)", text)
        return "cert", (m.group(1).strip() if m else "invalid certificate")
    if isinstance(getattr(e, "reason", None), socket.gaierror) or "Name or service not known" in text \
            or "nodename nor servname" in text or "getaddrinfo" in text:
        return "dns", "domain doesn't resolve"
    if "timed out" in text or isinstance(e, socket.timeout):
        return "timeout", "timed out"
    if "refused" in text:
        return "refused", "connection refused"
    if isinstance(e, ssl.SSLError) or "SSL" in text:
        return "ssl", "https handshake failed"
    return "other", text[:120]


def check(website):
    host = norm_host(website)
    out = {"host": host, "issues": [], "notes": []}
    if not host:
        out["issues"].append("NO URL")
        return out
    page = None
    # 1) https, verified like a browser
    try:
        page = fetch("https://" + host + "/")
        out["https"] = True
    except Exception as e:  # noqa: BLE001
        kind, msg = classify_exc(e)
        out["https"] = False
        if kind == "cert":
            out["cert_error"] = msg
            out["issues"].append("NOT SECURE")
            out["notes"].append("https certificate problem: %s (browsers show a full-page security warning)" % msg)
        elif kind in ("dns",):
            out["issues"].append("DOWN")
            out["notes"].append("domain doesn't resolve (expired or misconfigured domain)")
            return finish(out)
    # 2) plain http: does it redirect to https? (and fallback page if https failed)
    try:
        plain = fetch("http://" + host + "/")
        if not plain["final_url"].lower().startswith("https://"):
            if not out.get("https"):
                if "NOT SECURE" not in out["issues"]:
                    out["issues"].append("NOT SECURE")
                out["notes"].append("site only works on http: browsers mark it \"Not secure\"")
            else:
                out["notes"].append("http version doesn't redirect to https")
        if page is None:
            page = plain
    except Exception as e:  # noqa: BLE001
        kind, msg = classify_exc(e)
        # http redirecting to a broken-certificate https page = the visitor gets a full-page warning (NOT SECURE)
        if page is None and kind != "cert":
            # Only a dead domain is a sure DOWN. Timeouts / dropped connections are often a firewall
            # blocking scripts: the site may load fine in a browser, so it must be checked by hand.
            out["issues"].append("CHECK")
            out["notes"].append("didn't load for the script (%s): open it in a browser before saying anything" % msg)
            return finish(out)
    if page is None and out.get("cert_error"):
        try:
            page = fetch("https://" + host + "/", verify=False)
        except Exception:  # noqa: BLE001
            pass
    if page is None:
        out["issues"].append("CHECK")
        out["notes"].append("couldn't load the page: open it in a browser")
        return finish(out)

    body, status = page["body"], page["status"]
    out.update(status=status, final_url=page["final_url"], load_seconds=page["seconds"])
    low = body.lower()
    if status in (401, 403, 429, 503) and any(s.lower() in low for s in BLOCK_SIGNS):
        out["issues"].append("BLOCKED")
        out["notes"].append("a bot check blocked the test: open it in a browser before saying anything")
        return finish(out)
    if 520 <= status <= 530:
        # Cloudflare's own error codes: usually the firewall refusing a script, not the real site
        out["issues"].append("CHECK")
        out["notes"].append("Cloudflare returned %d to the script: open it in a browser" % status)
        return finish(out)
    if status >= 500:
        out["issues"].append("ERROR")
        out["notes"].append("homepage returns HTTP %d (server error)" % status)
    elif status >= 400:
        out["issues"].append("ERROR")
        out["notes"].append("homepage returns HTTP %d" % status)
    for needle, label in ERROR_SIGNS:
        if needle.lower() in low:
            if "ERROR" not in out["issues"]:
                out["issues"].append("ERROR")
            out["notes"].append(label)
            break
    for needle, label in PARKED_SIGNS:
        if needle.lower() in low:
            out["issues"].append("PARKED")
            out["notes"].append(label)
            break
    if "PARKED" in out["issues"] or "ERROR" in out["issues"]:
        return finish(out)

    # Dated: only hard, visible facts
    years = [int(y) for y in re.findall(r"(?:©|&copy;|&#169;|copyright)\s*(?:\d{4}\s*[-–]\s*)?((?:19|20)\d{2})", body, re.I)]
    if years:
        out["copyright_year"] = max(years)
        if out["copyright_year"] <= THIS_YEAR - 4:
            out["notes"].append("footer still says © %d" % out["copyright_year"])
    out["mobile_viewport"] = bool(re.search(r"<meta[^>]+name=[\"']viewport", body, re.I))
    if not out["mobile_viewport"] and len(body) > 2000:
        out["notes"].append("no mobile viewport tag: likely hard to use on a phone")
    gen = re.search(r"<meta[^>]+name=[\"']generator[\"'][^>]+content=[\"']([^\"']+)", body, re.I)
    if gen:
        out["generator"] = gen.group(1)[:60]
        wp = re.search(r"WordPress (\d+)\.(\d+)", out["generator"])
        if wp and int(wp.group(1)) < 6:
            out["notes"].append("runs WordPress %s.%s (released 4+ years ago)" % wp.groups())
        if re.search(r"FrontPage|Dreamweaver|iWeb", out["generator"], re.I):
            out["notes"].append("built with %s (discontinued)" % out["generator"])
    if re.search(r"\.swf[\"'?]|application/x-shockwave-flash", body, re.I):
        out["notes"].append("uses Flash (browsers stopped supporting it in 2021)")
    pw = page["headers"].get("X-Powered-By") or page["headers"].get("x-powered-by") or ""
    if pw:
        out["powered_by"] = pw[:40]
        m = re.search(r"PHP/(\d+)\.(\d+)", pw)
        if m and (int(m.group(1)) < 7 or (int(m.group(1)) == 7)):
            out["notes"].append("server runs PHP %s.%s (no security updates since 2022 or earlier)" % m.groups())
    dated_hits = [n for n in out["notes"] if n.startswith(("footer still", "no mobile", "runs WordPress", "built with", "uses Flash", "server runs PHP"))]
    if dated_hits:
        out["issues"].append("DATED")
    if page["seconds"] > 6:
        out["issues"].append("SLOW")
        out["notes"].append("homepage took %.1f s to load" % page["seconds"])
    return finish(out)


SEVERITY = {"DOWN": 100, "PARKED": 95, "ERROR": 90, "NOT SECURE": 80, "DATED": 50, "SLOW": 30, "BLOCKED": 0, "CHECK": 0, "NO URL": 0}


def finish(out):
    out["severity"] = max([SEVERITY.get(i, 0) for i in out["issues"]] or [0])
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="leads.json, or one or more websites")
    ap.add_argument("--out", default=None)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    if len(args.inputs) == 1 and args.inputs[0].endswith(".json"):
        with open(args.inputs[0], encoding="utf-8") as f:
            data = json.load(f)
        rows = data.get("rows", []) if isinstance(data, dict) else data
    else:
        rows = [{"name": w, "website": w} for w in args.inputs]
    todo = [r for r in rows if r.get("website")]
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for r, res in zip(todo, ex.map(lambda r: check(r["website"]), todo)):
            r["check"] = res
    todo.sort(key=lambda r: -r["check"]["severity"])
    flagged = [r for r in todo if r["check"]["severity"] > 0]
    for r in todo:
        c = r["check"]
        print("%-4s %-40s %-22s %s" % (c["severity"], (r.get("name") or c["host"])[:40], ",".join(c["issues"]) or "ok", "; ".join(c["notes"])[:150]))
    print("\n%d checked · %d with problems · %d blocked (check by hand)" % (
        len(todo), len(flagged), sum(1 for r in todo if set(r["check"]["issues"]) & {"BLOCKED", "CHECK"})), file=sys.stderr)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(todo, f, indent=1)
        print(args.out, file=sys.stderr)


if __name__ == "__main__":
    main()
