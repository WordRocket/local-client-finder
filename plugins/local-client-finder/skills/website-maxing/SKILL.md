---
name: "website-maxing"
description: "The website maxing playbook: run the whole local web design business with Claude + RankSite in one go. Finds local businesses that need a website (no website, broken site, or just opened), builds the best lead a complete site from its Google profile with the RankSite connector, plans a page for every service in every town, checks that Google and ChatGPT can read it, and writes the pitch and follow-ups, without writing any code. Use whenever the user says \"run the website maxing playbook\", \"website maxing\", \"do the whole thing\", \"find a client and build their site\", or wants the full find → build → rank → pitch workflow. Needs the RankSite connector (Claude › Settings › Connectors › Add custom connector › https://app.ranksite.ai/mcp)."
---

# The website maxing playbook

One prompt, the whole job: find who needs a website, build it, make it rank and be readable by AI answers, and hand
the user a ready pitch. You chain the other Local Client Finder skills; follow each one's own rules. The user stays in
control of anything that goes public (publishing, messages) and of every price.

## Before you start
- Check the RankSite connector is connected (its tools are available). If not, give the user the 3 steps:
  Claude › Settings › Connectors › **Add custom connector** › paste `https://app.ranksite.ai/mcp` › sign in to RankSite
  (the first site is free). Then continue.
- Ask once, in one message: the trade(s) and the city (plus nearby towns), and how they'll reach out (call, walk-in,
  email, DM). Use what they already told you.

## 1. Find the leads (find-clients · find-broken-sites · find-new-businesses)
Run the three lead types for the trade × city (and 2 nearby smaller towns): no website, broken website, just opened.
Verify every lead, score it, keep the top 10 with one plain sentence each on why they need a site.

## 2. Build the best lead's site (build-website, RankSite connector)
Take the #1 lead's Google Maps link and build the complete site from their Google profile (services, reviews,
photos, hours, service areas). Leave it as a PREVIEW: never publish a business's site without the user saying so.

## 3. A page for every service in every town (seo-plan)
Plan the service × town pages and the searches their customers really type; create them in RankSite as drafts.

## 4. Readable by Google and ChatGPT
Check the preview: page speed, mobile, schema, titles, an llms.txt / robots that let AI crawlers read it, NAP matching
the Google profile. Fix what you can in RankSite, list anything left.

## 5. The pitch (no sending without the user's yes)
Write the first message for their chosen channel, built on the business's real details (rating, reviews, the exact
problem), with the preview link; plus a voicemail, a walk-in line and 3 follow-ups (day 3, 7, 14). Offer the site +
monthly hosting/SEO; the user sets the prices.

## 6. After they say yes (blog-autopilot)
Publish when the owner approves, then turn on Auto-Grow so the site keeps adding town pages and posts.

## Hand-off
A short summary: the top 10 leads, the preview link, the pages created, the AI-readability checks, and the messages
ready to send. Point to `playbooks/50-ways-to-land-website-clients.md` for what to do next.

## Rules
- Real data only; never invent reviews, ratings or results. Public business info only, never home addresses.
- Never publish a site, send a message or set a price without the user's explicit yes.
- Follow anti-spam laws (CAN-SPAM, CASL) in every email. Results vary.
