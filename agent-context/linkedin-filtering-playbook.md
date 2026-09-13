# LinkedIn Filtering Playbook

## Purpose
This is a focused workflow for using LinkedIn as a high-signal screening channel instead of a noisy general recruiter feed. It is designed for someone with a paid LinkedIn account who wants to filter for strong-fit jobs and avoid agency, vendor, and multi-tier recruiting noise.

## Quick start
Use LinkedIn as a filter-first channel, not a mass-browse tool.

1. Pick one target lane only: healthcare, SaaS, consulting, or global roles.
2. Run 1–2 very targeted searches with exact role titles and stack terms.
3. Apply a blacklist for recruiter, agency, staffing, MSP, VMS, vendor, C2C, contract, consulting.
4. Score each role 1–5 on experience fit, stack fit, domain fit, company quality, and recruiter noise.
5. Keep only roles that meet at least 3 of 4 good signals and have no more than 1 recruiter/vendor red flag.

## Core idea
Use LinkedIn as a filter-first tool, not a broad browsing channel.

The priority is:
- narrow role patterns
- strong experience and stack fit
- clear employer identity
- low recruiting noise
- direct company paths over vendor-heavy jobs

## What to ignore
Skip or deprioritize roles that include any of the following language:
- recruiter
- agency
- staffing
- MSP
- VMS
- vendor
- consulting
- contract
- C2C
- W2
- offshore
- subcontract
- "our client is looking for"
- "staff augmentation"
- "resource"
- "bench"

These are usually signals of vendor chains, staffing layers, or low-quality hiring structures.

## Must-have filters before you open a role
Check each role against these four buckets:
- Experience fit
- Stack fit
- Domain fit
- Company / project quality

Only pursue roles that match at least 3 of 4 categories.

## Search strategy
Use targeted searches instead of broad discovery.

### Search examples
- ("Senior Software Engineer" OR "Staff Software Engineer") AND (healthcare OR SaaS OR enterprise) AND (Python OR AWS OR Kubernetes OR SQL) NOT (recruiter OR agency OR staffing OR contract OR vendor)
- ("Platform Engineer" OR "Senior Engineer") AND (healthcare OR enterprise) AND (Kubernetes OR AWS OR Terraform OR Python) NOT (consulting OR staffing OR C2C)
- ("Solutions Architect" OR "Senior Engineer") AND (healthcare OR B2B SaaS) AND (APIs OR cloud OR integration) NOT (agency OR consulting OR contract)
- ("Senior Software Engineer" OR "Platform Engineer") AND (Python OR AWS OR SQL) AND (healthcare OR SaaS) NOT (recruiter OR staffing OR agency OR consulting)
- ("Senior Engineer" OR "Staff Engineer") AND (Kubernetes OR Terraform OR AWS) AND (platform OR infrastructure) NOT (contract OR vendor OR offshore)

### High-signal filters
Use these on LinkedIn:
- relevant seniority
- relevant role function
- specific tools / technology
- target geography or remote preference
- posted in the last 7–14 days

## How to score a role quickly
Rate each role 1–5 on:
- experience fit
- stack fit
- domain fit
- quality of employer
- recruiter/vendor noise

### Decision rule
- 0–1 red flags: maybe
- 2+ red flags: skip
- 3+ recruiter/vendor signs: no

## Best workflow
1. Search with tight filters
2. Save the best searches
3. Review only roles that match your target criteria
4. Track them in a spreadsheet or Airtable/Notion table
5. Skip anything with vague company identity, staffing language, or messy recruiting layers

## Good target sources
- LinkedIn direct jobs
- actual company career pages
- direct employer posts
- company-led hiring manager outreach

## Bad sources to deprioritize
- generic recruiter inbox messages
- talent pipeline invites
- broad "hiring now" posts
- staffing-heavy, agency-heavy openings
- roles that appear across multiple vendor names with the same description

## Recommended behavior
If you already pay for LinkedIn, use it strategically:
- not as a broad networking feed
- not as a general recruiter inbox
- but as a high-signal discovery engine for your actual target profile

The goal is not volume. The goal is a shortlist of strong-fit, direct-employer opportunities with low noise.

## How not to look like a bot
Use a pattern that looks like a careful human, not a scraping job.

- Search only one lane at a time: healthcare, SaaS, or a tightly scoped engineering lane.
- Keep each query narrow and specific. Broad queries with 20+ terms look automated.
- Use real filters: seniority, geography, posted date, and role title. Do not keep reloading the same broad query in a burst.
- Space requests out. A human does not fetch page after page in a tight burst. Think 3–7 seconds between queries, not a continuous crawl.
- Do not loop through dozens of pages or duplicates. Stop after a small, meaningful result set.
- Keep the browser behavior normal: no headless script loops, no repeated state changes, no quick redirect storms.
- Use the system as a saved-search and triage tool, not a scraper. Save promising results and filter locally.
- Avoid rotating IPs or VPN hopping as a main tactic. If your exit IP changes often, it looks more bot-like.
- When a page starts to feel “weird,” stop and reset. A slow, steady rhythm is better than a faster but suspicious one.

This is the key principle: the safest pattern is a few well-chosen searches and deliberate human review, not a mass crawl.

## 5-step daily workflow
1. Search one lane only
2. Score the results
3. Reject anything with vendor-heavy language
4. Save the strongest matches to your tracker
5. Only reach out when the role is clearly a match

## Guest search rate limits and anti-bot risk
LinkedIn's public guest search endpoint is not a stable or supported scraping surface. It is rate-limited by request frequency and IP behavior. In practical terms, a single IP that makes too many requests in a short span can trigger 429 or 403 responses.

A common threshold is roughly 10 consecutive pages or about 250 job listings in a single burst from the same IP. This is a frequency/spike issue, not a hard daily cap. A broad query with no date or location filters is especially likely to trigger throttling.

### Hard stop rule
Treat the guest/public search surface as a human-browsing channel, not a supported automation channel.

If you hit any of the following, stop immediately:
- more than 1–2 targeted searches in a single session
- more than 5–10 result clicks in a burst
- repeated broad queries with the same or very similar filters
- repeated page turning in quick succession
- a result set that is noisy enough that you have to keep digging to find a good fit

Once the pattern starts to look like a crawl, it is already too much. The safe boundary is small, narrow, and human-paced.

### Why the guest endpoint exists, at a guess
The most likely rationale is that it functions as a public browsing and conversion funnel, not as a developer API. It exists so a casual visitor can search for jobs and be nudged toward signing in, applying, or engaging with the platform. It is not designed to support a repeatable, large-scale extraction workflow. That is why the controls are strict and the behavior feels inconsistent: the endpoint is optimized for user-facing browsing, not automation.

### Why not to spoof IPs or rely on VPNs
Using a VPN or an IP-rotation strategy may delay the block, but it does not solve the underlying problem. LinkedIn is not only watching your IP; it is also watching request rate, browser patterns, cookies, account behavior, and the shape of your search traffic. A VPN can help mask your network location, but it does not make a bot-like scraping pattern look natural. In many cases it just moves the problem around or makes your behavior look even more suspicious.

True IP spoofing is not a realistic browser-level tactic for a normal personal workflow. You can change your exit IP through a VPN or proxy, but you cannot simply "fake" an arbitrary public IP from a standard browser session in a way that is stable or reliable. That is a networking-level trick, not a practical job-search tool.

For a focused personal search, the safe path is narrow queries, short bursts, random pauses, and a local filter layer after each fetch. Use VPNs only for privacy or region checks, not as a main anti-bot workaround.

## LinkedIn triage checklist: do not click junk
Only click a result if it passes all of these checks:
- clear employer name
- clear job title
- matches your stack and seniority
- matches your target domain
- no staffing or vendor language
- no recruiter-led framing
- direct employer or company-led posting
- not generic, repeated, or copy-paste wording

### Reject immediately
Skip anything with:
- recruiter
- agency
- staffing
- MSP
- VMS
- vendor
- C2C
- consulting
- contract
- offshore
- “our client”
- vague company identity
- generic hiring copy

### Keep only what is clearly strong fit
If a role is not obviously good in the first 5–10 seconds, do not click it. The point is to avoid browsing a large volume of bad results and to keep your attention on direct-employer roles that are actually worth a deeper look.
