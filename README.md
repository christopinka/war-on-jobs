# War on Jobs

A complete local system for narrowing the target-company search, screening away recruiter and vendor noise, and turning a small employer list into a disciplined role queue and application pipeline.

## Project goal

This repo is designed around a narrow operating model:

- keep each search lane explicit and high-signal
- favor direct employers over recruiters, staffing firms, and consulting wrappers
- maintain distinct target lists for the strongest job lanes
- convert those lists into a role queue and application workflow
- score job opportunities locally with a simple rule-based filter
- read the screening rules from the profile intake so reject lists and fit thresholds stay aligned with your actual goals
- keep outputs in CSV format for easy review, iteration, and backup

## Current strategy

The workflow separates the search into three explicit lanes:

1. Core healthcare technology lane
   - healthcare SaaS, regulated software, payer/provider workflow, interoperability, and data-heavy healthtech
   - active file: [data/targets/target_company_active_list.csv](data/targets/target_company_active_list.csv)

2. Global remote SaaS lane
   - remote-first, direct-employer, product-company roles with strong DevOps, platform, backend, cloud, and infra fit
   - active file: [data/targets/company_targets.csv](data/targets/company_targets.csv)

3. Healthcare-adjacent lane
   - digital health, care navigation, patient engagement, value-based care, and related workflow software
   - active file: [data/targets/adjacent_lane_targets.csv](data/targets/adjacent_lane_targets.csv)

The system stays disciplined by keeping each lane separate, validating company discovery against the repo allowlist, and using a small active queue rather than a noisy broad funnel.

## Repository layout

- `src/war_on_jobs/` — Python package for screening logic
- `tests/` — regression tests
- `data/` — organized workflow data by lifecycle: raw, screened, targets, workflow, prompts
- `docs/` — design and strategic planning documents
- `README.md` — repo overview

## Prompt vs code

This repo intentionally separates human intent from runtime behavior.

- Prompt files are guidance and configuration input. They ask the user for constraints and preferences, and they are stored as markdown or YAML. Examples: [data/prompts/profile-intake-questionnaire.md](data/prompts/profile-intake-questionnaire.md) and [data/workflow/career_profile_intake.yaml](data/workflow/career_profile_intake.yaml).
- Code files are the actual enforcement layer. They read the profile, score jobs, reject noise, and write the CSV outputs. Examples: [src/war_on_jobs/live_daily_search.py](src/war_on_jobs/live_daily_search.py) and [src/war_on_jobs/target_lane_refresh.py](src/war_on_jobs/target_lane_refresh.py).

The prompt is not the filter. The code is the filter.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m unittest -q
```

## Core flow

1. Refresh or regenerate the target-company shortlist across the relevant lanes.
2. Keep each lane in its own target CSV rather than mixing all companies together.
3. Validate potential company and careers URLs against the allowlist in [data/site_allowlist.yaml](data/site_allowlist.yaml) and the approved registry in [data/workflow/company_site_urls.csv](data/workflow/company_site_urls.csv).
4. Append new candidates and update existing rows in place; never replace the whole file with a broad dump.
5. Fill out the profile intake in [data/workflow/career_profile_intake.yaml](data/workflow/career_profile_intake.yaml) so the search is based on real constraints instead of vague intention.
6. Search only across the approved company and careers pages, collecting only relevant titles and role URLs.
7. Score and rank the collected roles by fit, company value, location, and strategic relevance.
8. Cut the full list down to the strongest top 10 as the active pursuit queue.
9. Move the rest into a watchlist or backlog rather than letting the pipeline become noisy.
10. Convert the shortlisted roles into the active role queue and contact plan.
11. Pull in raw job records or search results.
12. Run the screening script to reject recruiter/vendor noise using the configured keyword lists and the profile-defined minimum fit score.
13. Log each subflow write and trigger event to the JSONL workflow log.
14. Review kept and rejected outputs.
15. Apply or contact only to the strongest direct-employer matches in the active queue.

## Operational guidance

This repo intentionally avoids broad LinkedIn scraping as the primary workflow. The system is deliberately narrow, local, and high-signal.

The target design is now:
- healthcare platform / cloud / infrastructure roles as the main lane
- direct employers only
- remote-friendly or acceptable geography
- low recruiter/vendor noise
- a small, disciplined application queue rather than a noisy funnel
- a separate global remote SaaS lane for devops/platform-oriented product work
- a separate healthcare-adjacent lane for digital health and workflow-adjacent employers
- employer career pages and ATSs as the primary job source
- LinkedIn used only as a discovery and validation signal, not as the canonical job source
- company-scoped role discovery only: visit approved company/careers pages and capture only relevant titles and URLs
- repo-owned allowlist validation before the site is considered a valid discovery target
- explicit workflow logging for phase transitions, file updates, and failures
- no broad web scraping as the default operating model

If a company site is missing, no jobs are found, or the URL falls outside the approved allowlist, the workflow records the failure and continues without prompting endlessly or guessing at the next step.

## Tooling decision

This project intentionally follows a Python-first workflow.

- The canonical launch path is the Python script entrypoint in [src/war_on_jobs/target_lane_refresh.py](src/war_on_jobs/target_lane_refresh.py).
- Ruff is the active linting tool.
- Make is intentionally deferred and not part of the current workflow.
- The rationale and backlog are recorded in [docs/roadmap.md](docs/roadmap.md).

## Notes

The markdown files in the repo are strategic context and planning documents rather than runtime code. They belong in `docs/` or under a notes folder, not at the repo root.
