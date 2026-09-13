# Career profile intake prompt

Use this as the intake form for the job-search system. Fill it out before running the lane refresh or the daily live filter.

## Instructions

1. Populate the profile in `data/workflow/career_profile_intake.yaml`.
2. Use the resume and current role context as the primary source of truth.
3. Keep the answers concrete and honest, not aspirational-only.
4. Prefer specific constraints over vague preferences.
5. Treat the profile as the operating profile for the search engine.

## Questions to answer

- What are your strongest technical areas and most relevant recent wins?
- Which role families do you want next: backend, platform, cloud, DevOps, SRE, integration, or something else?
- Do you want direct-hire, contract, consulting, or staff roles?
- Which industries matter most: healthcare, healthtech, remote SaaS, regulated SaaS, enterprise software, or something else?
- What is your preferred work pattern: remote, hybrid, onsite, or remote-first with occasional travel?
- Where do you want to live now or in the next 12–24 months?
- Are you open to relocation, international remote work, or expat-style lifestyle planning?
- What is your salary floor and target?
- What are your financial or life obligations that affect the search?
- What work conditions are non-negotiable: direct employer only, healthcare relevance, fully remote, team quality, compensation floor, or a certain employer size?
- What patterns should be auto-rejected: recruiters, staffing, vendor wrappers, MSPs, consulting-heavy roles, or low-signal generic jobs?
- What signals matter most for a role to be worth pursuing?

## Output contract

The intake data should be structured enough to drive:
- lane selection
- target-company prioritization
- job keyword filters
- role-fit score thresholds
- company exclusion rules
- application pacing and decision quality

## Important boundary: this is a prompt, not the runtime filter

This file is a prompt and intake document. It tells the human and the agent what information matters.

It does not directly reject jobs or write CSVs.

The actual enforcement happens in code, especially in [src/war_on_jobs/live_daily_search.py](../../src/war_on_jobs/live_daily_search.py), which reads the structured YAML output from [data/workflow/career_profile_intake.yaml](../workflow/career_profile_intake.yaml) and then decides what to keep or reject.

In other words:
- prompt = what the system should care about
- YAML = structured profile output
- code = what the system actually does with that profile
