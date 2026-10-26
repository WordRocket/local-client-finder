---
name: find-new-businesses
description: |
  Find businesses that just opened (or just got their license) in a city, check which ones have no website or Google
  Business Profile yet, score them, write a "congrats on opening" outreach for each, and build a preview site with
  RankSite. Uses public city open-data business-license feeds, plus Google Maps, Yelp "Hot and New" and local
  grand-opening news. Use whenever the user wants: new business leads, newly registered / newly licensed businesses,
  "who just opened in [city]", grand openings, or clients for website / Google Business Profile / local SEO setup.
---

# Find new businesses that need a website

A business that opened this month needs everything at once: a website, a Google Business Profile, reviews, local
SEO. Nobody has pitched them yet. Your job: find who just opened in the user's area from PUBLIC sources, check what
they're missing online, and hand over a short, scored list with a friendly first message for each.

Never invent a business or a date. Every lead needs a source (dataset row, listing, or article).

---

## Step 0 — Intake (one message, skip what the user gave)
1. **City / area.**
2. **Niche filter** (optional): e.g. restaurants, salons, contractors, fitness. "Any" is fine.
3. **How recent**: default the last 30 days.
4. How they'll reach out (walk-in works best for brand-new storefronts).

## Step 1 — Pull new businesses (use every source that exists for the city)

**A. City open data (best: official, dated, free).** Many cities publish every new business license.
1. `python3 [skill_dir]/scripts/new_licenses.py find "<city>"` searches public Socrata portals (Chicago, Seattle,
   Calgary, Cincinnati, New Orleans, Norfolk, Berkeley, Winnipeg, Delaware and many more) for license datasets.
2. `python3 [skill_dir]/scripts/new_licenses.py pull <domain> <dataset-id> --days 30 --match "<niche regex>" --out new.json`
   returns `{name, category, date, address, home_based}`, newest first. Check the printed column choice; some
   datasets need a filter for NEW licenses only (Chicago: `--where "application_type='ISSUE'"`).
3. No Socrata dataset? Web search `"<city>" open data business licenses` (many cities use ArcGIS Hub or CKAN with a
   CSV download), and the state / province business registry if it publishes new registrations for free. See
   `references/sources.md`.

**B. Google Maps.** With a browser tool, search `<niche> in <city>` and run `scripts/maps-extract.js` (or read the list). Listings with 0–3 reviews, or marked "New" / "Recently
opened", are candidates. Confirm they're new (see Step 2); a listing with few reviews can also just be quiet.

**C. Yelp "Hot and New"** for restaurants, cafés and shops in the city.

**D. Local news and the chamber of commerce**: web search `"grand opening" <city>`, `"ribbon cutting" <city>`,
`"now open" <city>` limited to the last 30–60 days.

**Clean the list:** drop chains and franchises (Subway, Shell, pharmacy chains), add-on or renewal licenses (patio,
gaming, signage), holding companies and consultancies with no customers walking in, and anything that's just a
person's name. Drop or never contact HOME-BASED rows at their address; only reach them through a public business
channel (their own listing, page or business email).

## Step 2 — Check what they have online
For each business, search Google Maps and the web for `"<business name>" <city>`:
- **Google Business Profile?** none / exists (with or without the Website button).
- **Website?** none / Facebook or Instagram only / has one (if it has one, skip it or hand it to find-broken-sites).
- **Really new?** the license date, a "grand opening" post, first review date, or "Opened <month>" note. Write down
  the evidence.

Status: `NEW · NO SITE` (no website at all), `FACEBOOK ONLY`, or `NEW` (has a site; usually not a lead).

## Step 3 — Score (0–100)
| factor | points |
|---|---|
| **Online gap** | no website and no Google profile 40 · no website, has a Google profile 35 · Facebook/Instagram only 28 |
| **Recency** | opened / licensed in the last 14 days 20 · 15–30 days 15 · 31–60 days 8 |
| **Customer-facing storefront or service** (they need to be found) | yes 20 · partly 10 · no (wholesale, holding) 0 |
| **Reachable through a business channel** (listing phone, page, business email, storefront) | 10 |
| **Job size of the niche** (your judgement) | big-ticket 10 · mid 6 · small 3 |

One plain sentence per lead on WHY: "Licensed Oct 23 as a restaurant, no website and no Google profile yet: perfect
timing to set both up."

## Step 4 — Lead sheet
Add `status`, `score`, `why`, `opener`, keep `date` and the source, then run
`python3 [skill_dir]/scripts/build_report.py leads.json --title "new businesses in <city>"`.
It writes a sortable `.html` lead sheet + `.csv`. In chat lead with the count and source, e.g. "Chicago issued 264
new business licenses in the last 14 days; 80 are food, beauty, cleaning, fitness or auto. Here are the ones with no
website yet."

## Step 5 — Outreach
Use `references/outreach.md`: congratulate first, offer one useful thing (a preview site, or setting up their Google
Business Profile), keep it short. Walk-ins work best for new storefronts.

Rules: public business channels only; never use a home address or an owner's personal details from a registration;
one message per business; follow local anti-spam rules (CAN-SPAM / TCPA in the US, CASL in Canada, PECR / GDPR in
the UK and EU); stop on a no.

## Step 6 — The preview site (optional)
If they already have a Google Business Profile: Google Maps › the business › Share › Copy link ›
https://app.ranksite.ai › + New Site › paste. RankSite builds the site from the listing; the first site is free.
If they have no Google profile yet, offer to help them create one first (that's a service in itself), then build
the site from it. With the RankSite connector (plans with MCP access) you can `create_site` from the details you
found; confirm first, never publish without a yes.

You set your own prices; don't promise income or results.
