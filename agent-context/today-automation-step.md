# What You Can Start Today for Automation

## Best low-friction first step
Start a simple job-target tracking workflow in a local spreadsheet or markdown file.

### Why this is the right first step
- It creates structure without requiring a big build.
- It turns scattered job-search activity into something trackable and reusable.
- It gives you a foundation for later automation such as scoring, filtering, reminders, or summarization.

## Minimum viable version
Create a file or sheet with these columns:
- Company
- Role title
- Source
- Date found
- Fit score
- Status
- Notes
- Next action

## Email handling rule
If you publish a second email on your resume or a job board, expect it to get scraped and flooded very quickly. That is normal.

Use a dedicated job-search inbox only as a filtered relay, not as a public-facing identity:
- one alias for LinkedIn
- one alias for direct employer contact
- one alias for public boards only if you truly need it
- auto-filter recruiter, staffing, MSP, vendor, and generic spam
- keep your main inbox private and reserved for higher-signal communication

## Low-brain operating policy
This is the default rule set when you are tired or overloaded.

- One job-search inbox only
- One tracker only
- One target lane only
- Skip anything vague, vendor-led, or recruiter-heavy
- If it takes more than two minutes to decide, it is not a strong-enough fit

The goal is not to be clever. The goal is to reduce noise and avoid wasted brain cycles.

## Good next actions for today
1. Pick one target list: healthcare, SaaS, consulting, or global roles.
2. Add 10–20 companies or roles to the tracker.
3. For each one, note whether it is:
   - strong fit
   - medium fit
   - weak fit
4. Save one short note per company about why it matters.

## LinkedIn-specific workflow
LinkedIn search, anti-bot cautions, and screening behavior belong in the LinkedIn playbook, not this general automation note.

For the targeted search rules, the anti-bot guidance, and the daily LinkedIn operating policy, use [linkedin-filtering-playbook.md](linkedin-filtering-playbook.md).

This document stays focused on the broader automation and tracking layer: tracker setup, scoring, inbox handling, and simple local automation.

## Lightweight automation you can add next
- Add a simple score formula like:
  - strong match = 3
  - medium match = 2
  - weak match = 1
- Sort by score to see which roles deserve the most attention.
- Add a reminder column for follow-up dates.

## If you want a slightly more technical first step
Create a small local Python script that reads a CSV or markdown file and outputs:
- a ranked list of target companies
- a summary of high-fit roles
- a simple status report

## Existing services worth considering
### Cloud-based services
- Notion or Airtable for lightweight tracking and dashboards
- Zapier or Make for automating simple flows between services
- Teal, LoopCV, or similar job-search tools if you want more workflow automation without building from scratch
- Google Sheets or Microsoft Excel Online if you want easy collaboration and simple formulas

### Local or self-hosted options
- Obsidian or a local markdown-based system for notes and tracking
- A local Python workflow with CSV/JSON files and simple scripts
- Self-hosted tools such as n8n or Home Assistant-style automation stacks if you want more control
- Local AI tools such as Ollama plus a small script for summarizing and scoring opportunities

## Recommended path
- Today: build the tracker and populate it.
- Tomorrow: add a simple score or filter.
- Next: connect it to a basic local script, a cloud service, or a lightweight automation tool.

## Additional ideas from model and research
A simple but strong version of this system would be:
- a local tracker in CSV, Google Sheets, or Notion
- a lightweight AI layer for summarizing job descriptions and highlighting fit
- an automation layer such as n8n, Zapier, or Make for reminders and simple routing
- optional browser automation with Playwright or Selenium if you want to automate repetitive web interactions

A practical workflow would look like this:
1. Collect target companies and roles into the tracker.
2. Save the job description text and your notes in one place.
3. Use a local or cloud AI tool to generate a short fit summary, a tailored bullet, or a follow-up question.
4. Let the workflow remind you when a role needs a follow-up or a resume tweak.

Best-fit starting stack from the research:
- Lowest friction: Google Sheets or CSV + manual scoring + optional AI summaries
- Mid-level: Notion or Airtable + simple automations + reminders
- More technical: local Python + CSV/JSON + Ollama or another local LLM + n8n for orchestration

What to avoid at first:
- Overbuilding a full app before you have a repeatable process
- Automating application submission too early without a clear quality bar
- Using too many tools at once; one tracker and one automation path is enough to start

## Why this matters
This is the easiest way to move from manual job-search chaos to a repeatable process that can later become more automated.
