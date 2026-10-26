# Local Client Finder: a free Claude skill that finds businesses with no website

Tell Claude a niche and a city. It searches Google Maps, finds the businesses with **no website**, checks that they
really have none, scores them, writes the first message for each one, and helps you build a preview site for the
best lead so your pitch is "I already made you one".

Free, open source (MIT). Made by [RankSite](https://ranksite.ai).

```
You:    find me clients: pressure washing in Tulsa
Claude: Searched 72 Google Maps listings. 10 have no Website button; after checking each one
        and dropping the car washes, here are the leads, scored, with an opener for each…
```

## What you get
- **A verified lead list**: every business without a website, checked with a web search (NO SITE / FACEBOOK ONLY /
  SITE NOT LINKED), with rating, review count, phone and a Maps link.
- **A score out of 100** and one plain sentence on why each lead is worth a call.
- **Outreach that's specific to each business**: phone opener, voicemail, walk-in, email, follow-up, built on
  their real reviews.
- **A lead sheet** you can sort and click to call (`.html`) plus a `.csv` for your spreadsheet or CRM.
- **A preview site for your #1 lead**, built from their Google listing with RankSite (optional).

## Install

### Claude Code
```bash
claude plugin marketplace add WordRocket/local-client-finder
claude plugin install local-client-finder@local-client-finder
```
Then ask "find me clients: landscaping in Phoenix", or run `/local-client-finder:find-clients`.

### Claude.ai / Claude Desktop
1. Download [`dist/find-clients.zip`](dist/find-clients.zip).
2. In Claude: **Customize › Skills › + › Upload a skill** and pick the zip. (Older layouts: Settings › Capabilities › Skills.)
3. Make sure **Code execution and file creation** is on (Settings › Capabilities).

### Works best with
**Claude in Chrome**, so Claude can read the full Google Maps results list. Without a browser tool it falls back to
web search and tells you the list is partial.

## Build the preview site (the part that closes)
1. Google Maps › the business › **Share** › **Copy link**.
2. [app.ranksite.ai](https://app.ranksite.ai) › sign up (your first site is free) › **+ New Site** › paste the link.
3. RankSite builds the site from their Google listing: name, services, reviews, photos. Send the preview link with
   your opener.

On a RankSite plan with MCP access you can connect it to Claude (Settings › Connectors › Add custom connector ›
`https://app.ranksite.ai/mcp`) and the skill will create the site for you. It always asks before using a site slot or
publishing anything.

## Play fair
- Public business listing data only. Never use an owner's personal number, email or home address.
- One message per business, written for that business. No bulk texting or email blasts.
- Follow your local rules (CAN-SPAM / TCPA in the US, CASL in Canada, PECR / GDPR in the UK and EU). If they say no, stop.
- If Google asks you to prove you're human, solve it yourself; the skill won't try to get around it.

You set your own prices. Nothing here is a promise of income; results vary.

Not affiliated with Google or Anthropic.
