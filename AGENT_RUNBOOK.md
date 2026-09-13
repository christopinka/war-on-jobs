# Agent runbook

This repo is meant to be run from the root via the single canonical launcher:

- python3 workflow.py

That is the operational entrypoint. It is the human-facing version of the actual runtime flow and should be treated as the default procedure.

## What the root command does

Running the root launcher executes this exact sequence:

1. Refresh the target-company lanes
2. Back up the current working state
3. Screen the active job tracker rows against the current profile
4. Write the kept and rejected outputs
5. Stop with the current review set ready for human triage

This is the repo’s real workflow, and it is the workflow this runbook describes.

## Required profile input

Before the active job review is useful, fill in the working definition of fit in:

- data/workflow/career_profile_intake.yaml

This is the source of truth for:
- role families to target
- geography and remote preference
- direct-hire preference
- keywords to prioritize
- keywords to reject
- minimum fit score

## Important files

- Prompt guidance: data/prompts/profile-intake-questionnaire.md
- Structured profile: data/workflow/career_profile_intake.yaml
- Root launcher: workflow.py
- Full workflow implementation: src/war_on_jobs/workflow.py
- Lane refresh logic: src/war_on_jobs/target_lane_refresh.py
- Live filtering logic: src/war_on_jobs/live_daily_search.py
- Target lane outputs:
  - data/targets/target_company_active_list.csv
  - data/targets/company_targets.csv
  - data/targets/adjacent_lane_targets.csv
- Screened outputs:
  - data/screened/live_jobs_kept.csv
  - data/screened/live_jobs_rejected.csv
- Backup directory:
  - data/backups/

## Guardrails

- Treat the prompt file as guidance, not enforcement.
- Treat the YAML as the structured operating profile.
- Treat the Python code as the enforcement layer.
- Do not overwrite working data without a backup.
- Do not mix lanes into one giant list.
- Do not add staffing, recruiting, or vendor wrappers to the active list.
- Do not broad-scrape as the default path.
- Only review the kept rows unless you need to inspect rejected rows for tuning.

## Typical review criteria

Keep the best-fit direct-employer roles and reject:
- recruiters
- staffing firms
- vendor wrappers
- MSPs
- consulting-heavy roles
- low-signal generic jobs
- blocked or disallowed locations

## Validation

Before claiming the repo is green, run:

- python3 -m unittest discover -s tests -q

This confirms the screening and lane behavior still match the intended operating rules.

## Short version

If you need the smallest possible operating instruction, use this:

1. Fill in the profile in data/workflow/career_profile_intake.yaml
2. Run python3 workflow.py
3. Review the kept rows
4. Keep the strongest direct-employer matches moving forward

That is the current standard operating flow.
