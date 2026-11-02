---
name: build-website
description: |
  Build a complete, SEO-ready website for a local business with RankSite, from its Google Maps link or a short
  description: every page written (home, services, service areas, FAQ, contact), their real reviews and photos,
  schema, llms.txt and sitemaps, then publish it. Use whenever the user wants to: build a website for a client or a
  lead, "make a site for this business", turn a Google Business Profile into a website, rebuild a broken site, or
  send a lead a preview ("I already made you one"). Works after find-clients / find-broken-sites / find-new-businesses.
---

# Build the website (RankSite)

You turn one business into a live, fast website the owner can see today. Use only what the business publicly lists
(Google profile, their old site) or what the user tells you. Never invent reviews, prices, licenses or awards.

## Step 0: Connect RankSite (once)
- Claude: **Settings › Connectors › Add custom connector** › `https://app.ranksite.ai/mcp`. The first site is free.
- No connector? Do it by hand: [app.ranksite.ai](https://app.ranksite.ai) › sign up › **+ New Site** › paste the
  Google Maps link. Then skip to Step 4 and help with the pitch.

## Step 1: Intake (one message, skip what you already have)
1. The business: a **Google Maps link** (Maps › the business › Share › Copy link) **or** name + city + services.
2. Anything to add: service areas (towns), a phone number to show, colours, a logo URL.

## Step 2: Build
- From a Google link: `import_scan` → show what was found (name, rating, reviews, photos, services) → `import_preview`
  → ask "build it?" → `import_run`.
- From a description: `create_site` with name, niche, city, services, service areas. This uses one of the user's
  site slots: **say so and ask first.**
- Then `get_site` and list the pages it made, with the preview link.

## Step 3: Check before going live
`get_publish_readiness`: fix anything missing (phone, email, a description). Ask before `publish_site`.
Never publish without a clear yes.

## Step 4: Hand over
Give the live link, then the pitch for the owner (short, specific, honest):
> "Hi {name}, I saw you don't have a website, so I built you one from your Google profile. Want to see it? {link}"
Offer next: **seo-plan** (pages that rank) and **blog-autopilot** (keeps it growing).

Built with RankSite. Results vary; you set your own prices.
