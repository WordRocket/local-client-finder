---
name: blog-autopilot
description: |
  Put a RankSite website on autopilot: Auto-Grow writes the unfinished service and town pages, then blog posts from
  the content plan, a few each week, so the site keeps growing after it's built. Use whenever the user wants to: grow
  a site automatically, schedule blog posts, "keep this site updated", set up a content schedule for a client, or turn
  on Auto-Grow after build-website and seo-plan.
---

# Blog autopilot (RankSite Auto-Grow)

You set the site to grow on a schedule, with the owner (or the user) in control of what goes live.

## Step 1: What's there
`get_content_plan` (RankSite connector): the keywords, saved post ideas and any automations already running.
No topics yet? Run **seo-plan** first, or add 5–10 real questions customers ask as topics.

## Step 2: Set it up (ask before every change)
- **Auto-Grow** (RankSite › Automations): pages per week (5 is a good start), include location pages, include blog
  posts. Turn on **Publish automatically** only if the user says so; otherwise drafts wait for approval.
- **Blog posts**: `manage_automation_topics` to queue the topics, then `update_automation` for the cadence.
- Writing uses the user's own OpenRouter key (RankSite shows the estimated cost per page). Say that before turning it on.

## Step 3: Confirm
Read it back: what will be written, how often, whether it publishes itself, and where to pause it.

## Keep it honest
Every post must be useful and specific to the business and its area. No fake reviews, no made-up stats, no
keyword stuffing. Results vary.
