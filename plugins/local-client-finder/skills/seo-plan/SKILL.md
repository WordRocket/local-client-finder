---
name: seo-plan
description: |
  Plan the SEO for a local business website built with RankSite: the searches people really type in their area, a
  page for every service in every town they serve, and the content plan to rank on Google and get quoted by ChatGPT
  and Google's AI answers (GEO). Use whenever the user wants to: do keyword research for a local business, rank a new
  site, plan service area / town pages, "what should this site rank for", or grow a client's site after build-website.
---

# SEO plan for a local site (SEO + GEO)

You find what this business's customers search for and turn it into pages. Real searches only: never invent search
volumes. If you don't have a volume, say "people search this" and show where you saw it.

## Step 1: Know the business
`get_site` (RankSite connector) or ask: services, the main city, the towns they serve.

## Step 2: Research (free, real data)
For each service: web search "{service} {city}" and note Google's autocomplete ideas, "People also ask" questions,
what the map pack and the top 3 results cover, and the questions customers ask in reviews. Group them:
- **money searches**: "{service} {town}" → one page each
- **questions**: "how much does {service} cost in {city}", "do I need a permit for…" → FAQs + blog posts
- **trust**: reviews, licensed / insured, response time → on the home page

## Step 3: Build the plan in RankSite
- Towns: `update_towns` with the real service area (ask before changing anything).
- Pages: every service × every town becomes a location page (RankSite's Grow My Site shows "N pages not created
  yet"). Write the best ones first: the biggest town and the most-asked service.
- Questions → `manage_automation_topics` as blog topics (blog-autopilot writes them).

## Step 4: GEO (so AI answers can quote it)
Check the site has: a clear one-line answer at the top of each page, FAQs, LocalBusiness + Service schema, llms.txt,
and robots.txt that allows GPTBot / ClaudeBot / PerplexityBot. RankSite sites ship with these; confirm, don't assume.

## Hand over
A short table: page → the search it targets → why. Then offer **blog-autopilot**.

Results vary. Never promise rankings.
