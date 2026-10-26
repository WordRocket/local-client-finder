# Local Client Finder: 3 free Claude skills that find web design clients

Tell Claude a niche and a city. It finds local businesses that need a website **right now**, proves it, scores
them, writes the first message for each one, and helps you build a preview site so your pitch is "I already made
you one".

Free, open source (MIT). Made by [RankSite](https://ranksite.ai).

| skill | finds | ask Claude |
|---|---|---|
| **find-clients** | businesses on Google Maps with **no website** (checked one by one) | "find me clients: pressure washing in Tulsa" |
| **find-broken-sites** | businesses whose site is **broken, "Not secure", parked, showing errors or badly out of date** (© 2014, not mobile-friendly) | "find roofers in Hamilton with broken websites" |
| **find-new-businesses** | businesses that **just opened**, from city business-license data, Google Maps, Yelp "Hot and New" and grand-opening news | "who just opened in Chicago and has no website?" |

Real runs (Chicago, Oct 2026):
- `find-clients`: "handyman in Chicago IL" → 115 Google Maps listings, 32 with no Website button; the top ones checked by hand (e.g. 4.9★ from 76 reviews, no site anywhere).
- `find-broken-sites`: 70 Chicago handyman websites → 10 broken, each confirmed in a real browser: 7 domains that no longer exist, 1 "this domain isn't connected to a site", 1 that won't load, 1 full-page security warning. 2 more footers still say © 2019 / © 2020–2021.
- `find-new-businesses`: Chicago's open data → 264 new business licenses issued in 14 days. Spot check of 12 new shops and restaurants: 8 had no website or weren't on Google Maps.

## What you get
- **A verified lead list**: every lead checked (a web search, or a real browser for broken sites), with rating,
  reviews, phone and a link. No guesses.
- **A score out of 100** and one plain sentence on why each lead is worth a call.
- **Outreach written for each business**: phone, voicemail, walk-in, email and follow-up, built on their real
  details (their reviews, the exact problem on their site, their opening date).
- **A lead sheet** you can sort and click to call (`.html`) plus a `.csv`.
- **A preview site for your best lead**, built from their Google listing with RankSite (optional).

## Install

### Claude Code
```bash
claude plugin marketplace add WordRocket/local-client-finder
claude plugin install local-client-finder@local-client-finder
```
Then just ask, or run `/local-client-finder:find-clients`, `/local-client-finder:find-broken-sites`,
`/local-client-finder:find-new-businesses`. Already installed? Update with `claude plugin marketplace update local-client-finder`.

### Claude.ai / Claude Desktop
1. Download the skill zips you want from [`dist/`](dist/).
2. In Claude: **Customize › Skills › + › Upload a skill** and pick a zip. (Older layouts: Settings › Capabilities › Skills.)
3. Make sure **Code execution and file creation** is on (Settings › Capabilities).

### Works best with
**Claude in Chrome**, so Claude can read the full Google Maps list and check websites the way a customer sees them.
The website and license checks are small Python scripts (standard library only) that run in Claude Code; where code
can't reach the internet, Claude checks each site in the browser instead.

## Build the preview site (the part that closes)
1. Google Maps › the business › **Share** › **Copy link**.
2. [app.ranksite.ai](https://app.ranksite.ai) › sign up (your first site is free) › **+ New Site** › paste the link.
3. RankSite builds the site from their Google listing: name, services, reviews, photos. Send the preview with your
   opener.

On a RankSite plan with MCP access you can connect it to Claude (Settings › Connectors › Add custom connector ›
`https://app.ranksite.ai/mcp`) and the skills will create the site for you. They always ask before using a site slot
or publishing anything.

## Play fair
- Public business information only. Never an owner's personal number, email, home address or registered agent.
- Broken-site checks only load the public homepage, like a normal visitor. No scanning, no logins, no probing.
- One message per business, written for that business. No bulk texting or email blasts.
- Follow your local rules (CAN-SPAM / TCPA in the US, CASL in Canada, PECR / GDPR in the UK and EU). If they say no, stop.
- If Google asks you to prove you're human, solve it yourself; the skills won't try to get around it.

You set your own prices. Nothing here is a promise of income; results vary.

Not affiliated with Google, Yelp or Anthropic.
