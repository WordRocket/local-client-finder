---
name: find-broken-sites
description: |
  Find local businesses whose website is broken, insecure or badly out of date: "Not secure" / expired https
  certificates, sites that are down or parked, homepages showing errors, and hard signs of age (a footer that still
  says © 2014, no mobile layout, Flash, end-of-life PHP). Verifies each one in a real browser, scores the leads,
  writes outreach that leads with the problem, and helps rebuild the site with RankSite. Use whenever the user wants
  to: find businesses with broken websites, find sites with no SSL / "not secure", find outdated websites to redesign,
  get web design or website maintenance clients, or "find me clients whose website is broken in [city]".
---

# Find businesses with broken or outdated websites

These are the warmest web-design leads there are: the business already believes in having a website, and theirs is
visibly letting them down. Your job is to find them from a Google Maps search, PROVE each problem the way a customer
would see it, and hand the user a short list with the evidence and the first message to send.

Only report what a normal visitor can see. Load the public homepage like a browser does; never scan ports, try
logins, probe other paths or test for vulnerabilities. Never invent a problem.

---

## Step 0 — Intake (one message, skip what the user already gave)
1. **Niche** and **area** (e.g. "dentists in Mississauga", "roofers in Hamilton").
2. **How many leads** (default 15 verified).
3. How they'll reach out (phone, email, walk-in).

## Step 1 — Pull the businesses that HAVE a website
With a browser tool (Claude in Chrome or similar):
1. Open `https://www.google.com/maps/search/<niche>+in+<city>`.
2. Run `scripts/maps-extract.js` in the tab with the browser tool's JavaScript action (paste the file; prefix the last
   line with `await` if needed). Keep the rows where `website` is NOT empty, drop `sponsored` rows and other trades.
3. Need more? Repeat for neighbouring towns or a sister niche.

Without a browser tool: web search `<niche> <city>` and collect the businesses' own websites. Say the list is partial.

## Step 2 — Check every website
Save the rows as `sites.json` and run:
`python3 [skill_dir]/scripts/check_sites.py sites.json --out checked.json`
(`[skill_dir]` = the folder this SKILL.md is in. Standard library only. If your environment can't reach the internet
from code, skip to Step 3 and check each site in the browser instead.)

It loads each homepage (https first, then http) and adds `check.issues`:

| code | means | how strong a lead |
|---|---|---|
| **DOWN** | the domain doesn't resolve (expired or misconfigured) | strongest: they're losing every visitor |
| **PARKED** | domain for sale, parked, suspended or expired hosting | strongest |
| **ERROR** | the homepage shows an error (HTTP 4xx/5xx, database / PHP / WordPress critical error) | very strong |
| **NOT SECURE** | no working https, or an expired / invalid certificate: Chrome shows "Not secure" or a full-page warning | strong |
| **DATED** | hard signs of age: © year 4+ years old, no mobile viewport, Flash, discontinued builder, end-of-life PHP, WordPress older than 6.0 | good |
| **SLOW** | homepage took over 6 s | weak on its own |
| **CHECK** / **BLOCKED** | the script couldn't load it (often a firewall that blocks scripts) | unknown: check in a browser, never pitch on this alone |

## Step 3 — Verify in a real browser (never skip)
For every site with an issue (and every CHECK/BLOCKED), open it in the browser tool, as a customer would:
- Confirm the problem is real and visible: the "Not secure" label or warning page, the error text, the © year in the
  footer, the layout on a phone-width window.
- Take a screenshot of the problem as evidence (it goes in the pitch).
- If it loads fine and looks fine, drop it. A false alarm in a pitch kills trust.
- Also confirm it's really their site (the business name or phone is on it).

## Step 4 — Score (0–100)
| factor | points |
|---|---|
| **Worst verified problem** | DOWN / PARKED 40 · ERROR 36 · NOT SECURE 32 · DATED 22 · SLOW 10 |
| **Reviews** (busy and real) | 100+ → 25 · 50–99 → 20 · 20–49 → 15 · 5–19 → 8 · 0–4 → 3 |
| **Rating** | 4.5+ → 10 · 4.0–4.4 → 7 · under 4.0 → 3 |
| **Reachable** | phone listed → 10 |
| **Job size of the niche** (your judgement) | big-ticket 15 · mid 10 · small 5 |

Write one plain sentence per lead: "Their site shows Chrome's 'Not secure' warning, and they have 210 reviews: busy
business, scaring off new customers at the door."

## Step 5 — Lead sheet
Give each lead `status` = its worst verified issue (e.g. `NOT SECURE`), plus `score`, `why`, `opener`, then run
`python3 [skill_dir]/scripts/build_report.py leads.json --title "<niche> in <city>: broken sites"`.
It writes a sortable `.html` lead sheet and a `.csv`. In chat, lead with the count: e.g. "Checked 30 roofing websites
in Hamilton. 2 have a visible problem; here they are, with proof."

## Step 6 — Outreach
Use `references/outreach.md`. Lead with the problem in plain words and the evidence, never with jargon or fear.
Be kind: the owner probably has no idea. Offer to send the screenshot.

Rules: public business contact details only; one message per business, written for them; follow local anti-spam
rules (CAN-SPAM / TCPA in the US, CASL in Canada, PECR / GDPR in the UK and EU); stop if they say no.

## Step 7 — The fix (optional)
- **Rebuild:** RankSite can build a modern, fast, secure site from their Google listing in minutes: Google Maps ›
  the business › Share › Copy link › https://app.ranksite.ai › + New Site › paste. The first site is free. Show the
  owner the preview next to their current site.
- **Repair:** for an expired certificate or a parked domain, the fix may be small (renew the certificate or domain).
  Say so honestly; a quick fix is a great way to earn the bigger job.

You set your own prices; don't promise income or results.
