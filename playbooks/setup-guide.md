# The full setup guide: RankSite + Claude, in 5 minutes

Build, rank and run local business websites from Claude, with the 7 free Local Client Finder skills and RankSite.
No code, no WordPress, no hosting to set up. RankSite is our own tool; your first site is free. Results vary.

## 1. Connect RankSite to Claude (1 minute)
1. Open Claude (claude.ai or the desktop app) and go to **Settings › Connectors**.
2. Click **Add custom connector** and paste: `https://app.ranksite.ai/mcp`
3. Sign in to RankSite when asked (free account; your first site is free).

## 2. Install the 7 free skills (2 minutes)
**Claude Code:** run these two commands:
`claude plugin marketplace add WordRocket/local-client-finder`
`claude plugin install local-client-finder@local-client-finder`

**Claude.ai / desktop:** download the skill zips from github.com/WordRocket/local-client-finder (the dist folder), then
**Customize › Skills › + › Upload a skill** for each one. Turn on **Code execution and file creation** in Settings ›
Capabilities. For best results, add Claude in Chrome so Claude can read Google Maps the way you see it.

## 3. What each skill does, and what to ask
1. **website-maxing** (the whole playbook). Claude: "Run the website maxing playbook for roofers in Tulsa"
2. **find-clients**: businesses on Google Maps with great reviews and no website. Claude: "Find me clients: pressure washing in Tulsa"
3. **find-broken-sites**: businesses whose website is down, insecure or out of date. Claude: "Find roofers in Hamilton with broken websites"
4. **find-new-businesses**: businesses that just opened (city licence data). Claude: "Who just opened in Chicago and has no website?"
5. **build-website**: builds the whole site from a Google profile with RankSite. Claude: "Build a website for this business: [Google Maps link]"
6. **seo-plan**: a page for every service in every town, readable by Google and ChatGPT. Claude: "Plan the SEO for this site"
7. **blog-autopilot**: turns on Auto-Grow, so new town pages and blog posts go up every week. Claude: "Put this site on autopilot"

## 4. Your first day
1. Run find-clients for one trade in your town. Pick the lead with the most reviews and no website.
2. Build their site as a preview (never publish without the owner's yes).
3. Call them with the preview link: "I built you a website, want to see it?"
4. Charge for the site, then monthly for hosting and SEO. You set your prices.

Next: read "50 ways to land website clients, ranked S tier to C tier" (in this folder).

---
Free skills: github.com/WordRocket/local-client-finder · RankSite: app.ranksite.ai. Follow anti-spam laws (CAN-SPAM, CASL)
when you reach out. Never publish a business's site or send a message without their yes. Results vary.
