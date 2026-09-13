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

## How to add a new lane

Use this sequence when creating a new target lane.

### 1. Decide whether the lane is primary or secondary

A primary lane should be a real direct-employer target list. A secondary lane should be a watchlist for consulting, recruiting, or adjacent opportunities that are useful but not core to the direct-hire strategy.

### 2. Add the prompt file

Create a new prompt under:

- data/prompts/

The prompt should define:
- the purpose of the lane
- the intended company types
- the explicit exclusions
- the output file target
- the ranking and quality rules

This is where the lane-specific judgment belongs.

### 3. Add the lane to the ordered refresh registry

Update:

- data/workflow/lane_refresh_order.csv

This file defines the operational order of the lane refresh workflow. Each lane entry needs:
- step number
- lane name
- prompt file path
- target CSV path
- trigger name
- status

This is the part that makes the lane active in the single refresh sequence.

### 4. Add the lane payload in the Python refresh logic

Update:

- src/war_on_jobs/target_lane_refresh.py

Add a new entry to the LANE_PAYLOADS dictionary. This is the actual seed list used by the refresh logic. It should include a small curated set of employers and a note explaining why they belong in the lane.

This is the code-side enforcement step.

### 5. Decide whether the lane needs profile or rule changes

The lane-specific rules may require updates to:

- data/workflow/career_profile_intake.yaml
- the reject/priority keywords in the live filter profile
- the direct-employer or staffing exclusions in the operating profile

For example, a consulting/recruiting lane should usually be marked as secondary and not treated as a direct-employer lane in the candidate profile.

### 6. Update tests and validation

Add or update the expected lane sequence in:

- tests/test_target_lane_refresh.py

This protects the lane registry and stops the repo from silently drifting.

### 7. Validate the workflow

Before claiming the lane is ready, run:

- python3 -m unittest discover -s tests -q

and then run the root workflow if needed:

- python3 workflow.py

### What we needed to add for the consulting/recruiting lane

For this project, the set of required additions was:

- a prompt file in data/prompts/
- a lane row in data/workflow/lane_refresh_order.csv
- a payload entry in src/war_on_jobs/target_lane_refresh.py
- a test update in tests/test_target_lane_refresh.py
- a decision to keep the lane secondary and explicit instead of mixing it into the primary direct-employer flows

The config file itself did not need a brand-new branch of logic unless the lane was intended to become a first-class target. In this case, the lane stayed as a watchlist, which kept the existing YAML and filtering rules intact while making the lane explicit and operational.

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
