# Career profile intake prompt

Use this as the intake form and operating checklist for the job-search system. Fill it out before running the lane refresh or the daily live filter.

## Purpose

This file is the human-facing instruction layer. It defines the search intent and the decision criteria. It is not the runtime filter.

The code that enforces the rules lives in:
- [src/war_on_jobs/target_lane_refresh.py](../../src/war_on_jobs/target_lane_refresh.py)
- [src/war_on_jobs/live_daily_search.py](../../src/war_on_jobs/live_daily_search.py)

The structured output must be written to:
- [data/workflow/career_profile_intake.yaml](../workflow/career_profile_intake.yaml)

## Required workflow

Follow this sequence in order:

1. Fill out the profile questionnaire below.
2. Write the answers into [data/workflow/career_profile_intake.yaml](../workflow/career_profile_intake.yaml).
3. Refresh the lane target lists using the ordered lane workflow in [src/war_on_jobs/target_lane_refresh.py](../../src/war_on_jobs/target_lane_refresh.py).
4. Confirm the output CSVs are in the target folder:
   - [data/targets/target_company_active_list.csv](../../data/targets/target_company_active_list.csv)
   - [data/targets/company_targets.csv](../../data/targets/company_targets.csv)
   - [data/targets/adjacent_lane_targets.csv](../../data/targets/adjacent_lane_targets.csv)
5. Back up the current working state before a live filtering run.
6. Run the local live filter in [src/war_on_jobs/live_daily_search.py](../../src/war_on_jobs/live_daily_search.py).
7. Review the results in:
   - [data/screened/live_jobs_kept.csv](../../data/screened/live_jobs_kept.csv)
   - [data/screened/live_jobs_rejected.csv](../../data/screened/live_jobs_rejected.csv)
8. Only keep the strongest matches in the active queue or application tracker.

## Hard requirements

- Use the resume and current role context as the primary source of truth.
- Keep the answers concrete and honest, not aspirational-only.
- Prefer specific constraints over vague preferences.
- Treat the profile as the operating profile for the search engine.
- Do not add broad, noisy, or low-signal job sources without filtering them.
- Do not treat agencies, staffing firms, MSPs, or vendor wrappers as valid direct-employer matches.

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

The YAML output should be structured enough to drive:
- lane selection
- target-company prioritization
- job keyword filters
- role-fit score thresholds
- company exclusion rules
- location rules
- application pacing and decision quality

The specific keys to populate include:
- `company_and_role_filters.keywords_to_prioritize`
- `company_and_role_filters.keywords_to_reject`
- `company_and_role_filters.minimum_fit_score`
- `location.preferred_locations`
- `career_goals.preferred_industries`
- `career_goals.target_role_families`

## Do not do this

- Do not skip the YAML update.
- Do not treat the markdown prompt as runtime logic.
- Do not directly edit the live CSV outputs without a backup.
- Do not broaden the search into a giant noisy list.
- Do not keep roles that fail the direct-employer or low-signal criteria.

## Prompt-to-code mapping

This file tells the agent what should matter.
The YAML is the structured profile.
The Python code is the enforcement layer.

In other words:
- prompt = intent and operational questions
- YAML = data model for the active search
- code = actual screening and CSV writing

The agent should not invent a different workflow. It should follow this repo sequence and work from the actual target and screened CSV files rather than improvising a new path.
