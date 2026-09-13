# War on Jobs

A complete local system for narrowing the target-company search, screening away recruiter and vendor noise, and turning a small employer list into a disciplined role queue and application pipeline.

## Project goal

This repo is designed around a narrow operating model:

- keep each search lane explicit and high-signal
- favor direct employers over recruiters, staffing firms, and consulting wrappers
- maintain distinct target lists for the strongest job lanes
- convert those lists into a role queue and application workflow
- score job opportunities locally with a simple rule-based filter
- keep outputs in CSV format for easy review, iteration, and backup

## Current strategy

The workflow now separates the search into three lanes:

1. Core healthcare technology lane
   - healthcare SaaS, regulated software, payer/provider workflow, interoperability, and data-heavy healthtech
   - active file: [data/targets/target_company_active_list.csv](data/targets/target_company_active_list.csv)

2. Global remote SaaS lane
   - remote-first, direct-employer, product-company roles with strong devops, platform, backend, cloud, and infra fit
   - active file: [data/targets/company_targets.csv](data/targets/company_targets.csv)

3. Healthcare-adjacent lane
   - digital health, care navigation, patient engagement, value-based care, and related workflow software
   - active file: [data/targets/adjacent_lane_targets.csv](data/targets/adjacent_lane_targets.csv)

The system stays disciplined by treating each lane as a separate shortlist rather than one giant catch-all list.

## Repository layout

- `src/war_on_jobs/` — Python package for screening logic
- `tests/` — regression tests
- `data/` — organized workflow data by lifecycle: raw, screened, targets, workflow, prompts
- `docs/` — design and strategic planning documents
- `README.md` — repo overview

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m unittest -q
```

## Core flow

1. Refresh or regenerate the target-company shortlist for the appropriate lane.
2. Keep each lane in its own target CSV rather than mixing all companies together.
3. Append new candidates and update existing rows in place; never replace the whole file with a broad dump.
4. Convert the shortlist into a role queue.
5. Pull in raw job records or search results.
6. Run the screening script to reject recruiter/vendor noise.
7. Review kept and rejected outputs.
8. Prioritize and apply only to the strongest direct-employer matches.

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

## Notes

The markdown files in the repo are strategic context and planning documents rather than runtime code. They belong in `docs/` or under a notes folder, not at the repo root.
