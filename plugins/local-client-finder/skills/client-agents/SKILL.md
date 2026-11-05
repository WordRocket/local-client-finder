---
name: "client-agents"
description: "Six Claude agents find your next web design client at the same time: five finders (just opened this month · people asking online for a website · Google reviews that complain about a site or booking · broken or outdated websites · busy businesses with no website), one critic that throws out weak leads, then a vote. You get the top 3 with the proof behind each one, a preview website for #1 built with RankSite, and the first email waiting as a draft in your Gmail. Use whenever the user says \"find me a paying client\", \"run the client agents\", \"find my next client\", \"who should I pitch today\", or wants the best few leads in a city, not a long list. Works best in Claude Code (agents run in parallel) with Claude in Chrome, the RankSite connector and a Gmail connector; on Claude.ai the agents run one after another."
---

# Client agents: six Claudes, one job each, then a vote

Tell Claude a trade (or "any local business") and a city. Five finder agents each look at the city through ONE lens,
a critic picks every lead apart, and all six vote. The user gets three leads they can pitch today, each with real proof,
a preview site for the winner and a first email ready to send. Nothing is invented: every lead has a public source.

## Before you start (one message, only what's missing)
1. The city (plus 1–2 nearby smaller towns) and the trades, or "any storefront business".
2. Who they are, for the email: name, business, phone, business address (anti-spam laws need it), website.
3. Optional: is the RankSite connector connected (Claude › Settings › Connectors › Add custom connector ›
   `https://app.ranksite.ai/mcp`, first site free)? Is a Gmail connector connected?

## 1. The five finders (run them at the same time)
In Claude Code, start **five agents in parallel** (one Task/Agent call each, in a single message), each with the
city, the trades and its lens below, and ask each for up to 8 candidates as JSON:
`{name, category, area, maps_url, phone, website, evidence: [{fact, source_url}], lens}`.
On Claude.ai (no parallel agents), run the five lenses one after another yourself, same output.

| agent | lens | how (public sources only) |
|---|---|---|
| **New** | businesses that opened in the last 30–45 days | city open-data business licenses (see the find-new-businesses skill: `new_licenses.py find "<city>"`), Google Maps listings with few, recent reviews, "now open" / grand-opening news. Skip home-based licenses. |
| **Asking** | people asking online for a website or a web designer | search public posts: `site:reddit.com "<city>" (website OR "web designer") (need OR looking OR recommend)`, local subreddits, public Facebook groups and Nextdoor pages Google shows, Craigslist gigs. Keep posts from the last 6 months, the business must be identifiable. |
| **Reviews** | reviews that complain about the website, booking, ordering or wrong info online | Google / Yelp reviews mentioning "website", "online booking", "couldn't book", "wrong hours", "menu online", "no website". Quote ≤ 15 words, never the reviewer's name. |
| **Broken** | websites that are down, "Not secure", parked, erroring or badly outdated | the find-broken-sites method (`check_sites.py`, then confirm every one in a real browser). |
| **No site** | busy businesses (many good reviews) with no website at all | the find-clients method: Google Maps search per trade, verify every "no website" row with a web search. |

## 2. The critic (one more agent, its only job is to say no)
Merge all candidates, remove duplicates (same phone, or same name + area), then for each one check and throw out:
- permanently closed, or no Google listing you can confirm;
- a chain or franchise (the website is handled by head office);
- home-based or a person's name at a home address (never use it);
- no public business contact (phone, business email, contact form);
- weak proof: the "need" isn't visible to a customer today (re-check the site, the post date, the review).
Keep a one-line reason for every lead thrown out; the user sees them.

## 3. The vote
Each of the six agents votes on every surviving lead: 1 if it would pitch this business today, 0 if not, with one
sentence. Score = votes out of 6. Ties: more independent proof (two lenses agree) wins, then more reviews.

## 4. The top 3
For each: name, category, area, score (e.g. 6/6), three proof chips that are all TRUE ("Opened Oct 22 · No website ·
4.8★ from 41 reviews"), the source links, and one plain sentence on why now. Save `clients/top3-<city>-<date>.md`.

## 5. A preview site for #1 (RankSite, ask first)
"Shall I build a preview site for <business> in RankSite? It uses one site slot and stays unpublished." On yes:
`import_scan` with their Google Maps link → `import_preview` → `import_run` (no Google link: `create_site` with their
public details). Note the preview link. **Never publish** a lead's site; it isn't theirs until they say yes.

## 6. The first email, as a Gmail draft (never sent by you)
Only to a business email listed publicly (their Google profile, website or social page). If there's none, write the
call / walk-in / DM version instead.
- Subject: short and specific ("I made a website preview for <business>").
- Body (≤ 120 words): one true, specific line about them (the opening, their reviews, the exact problem), the preview
  link, one tiny ask ("want me to put it on your own domain this week?"), the user's name, business, phone, **business
  address**, and "Reply 'no thanks' and I won't email again."
- With a Gmail connector: create it as a **draft** in the user's Gmail. Never send. Tell the user it's waiting in Drafts.
  No connector: give the text to copy.
- Optional video: a 30-second Loom script that walks through the preview (their name, the problem, the new site, the
  ask). The user records it in Loom and pastes the link into the draft.

## Hand-off
The top 3 table, the leads the critic threw out (with reasons), the preview link, and "your email to #1 is in Gmail
Drafts". Next: follow up once after 3–4 days, then stop unless they reply.

## Rules
- Real, public, today: every fact has a source. No guessed revenue, budgets or "ready to pay".
- Public business information only. Never owners' personal phones, emails or home addresses; never reviewers' names.
- One message per business, written for them. Drafts only: the user sends. Follow CAN-SPAM (US), CASL (Canada),
  PECR/GDPR (UK/EU). In Canada, only email a published business address about something relevant to that business.
- Google CAPTCHA or "unusual traffic": stop and let the user solve it. Never get around it.
- Never promise the user income or a number of clients. Results vary.
