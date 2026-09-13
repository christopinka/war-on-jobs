# Target employer assembly and role-queue design

## Purpose

This repo implements a bounded direct-employer job search system for healthcare, health-tech, regulated SaaS, and platform-heavy software roles.

The design objective is simple:
- keep the target set small and relevant
- keep lane boundaries explicit
- prioritize direct employers over recruiters and vendors
- use local CSV state as the system of record
- review a short active queue instead of a noisy broad funnel

## Scope

In scope:
- lane-based target generation
- ordered lane refresh and merge semantics
- live row screening and rejection logic
- site allowlist and approved company/careers URL validation
- top-10 active review queue for the best-fit roles
- workflow logging for phase transitions and file writes

Out of scope:
- uncontrolled open-web scraping as the default workflow
- broad LinkedIn browsing as the canonical job source
- staffing, MSP, or consulting-heavy roles treated as primary employment targets
- giant uncurated employer lists

## System architecture

### 1. Lane model

The system is organized into explicit lanes instead of a single mixed list.

Current lanes:
- core healthcare
- global remote SaaS
- healthcare-adjacent

Each lane maps to a curated target CSV and is refreshed in a deterministic order.

### 2. Discovery model

Discovery is deliberately bounded.

Rules:
- only approved company and careers URLs are valid sources
- only domains on the repo allowlist are considered eligible
- LinkedIn is secondary validation, not source of truth
- employer career pages and ATS pages are the primary job source
- no free-form open-web browsing is treated as the default behavior

### 3. Screening model

The screening engine reads the structured profile and rejects rows that fail fit logic.

Profile controls include:
- target role families
- geography and remote constraints
- keywords to prioritize
- keywords to reject
- minimum fit score
- direct-hire preference

### 4. Workflow logging model

Every operational phase and file-changing step is recorded to the JSONL workflow log.

This covers:
- phase start and completion
- lane refresh state
- backup creation
- live source selection
- screened output writes
- failure conditions and missing target states

### 5. Queue model

The strongest kept rows are converted into a short active queue for manual review and application work.

The queue should remain small enough to review personally and act on quickly, not large enough to create noise or drift.

## Active artifacts

- [data/targets/target_company_active_list.csv](../data/targets/target_company_active_list.csv)
- [data/targets/company_targets.csv](../data/targets/company_targets.csv)
- [data/targets/adjacent_lane_targets.csv](../data/targets/adjacent_lane_targets.csv)
- [data/workflow/job_target_tracker.csv](../data/workflow/job_target_tracker.csv)
- [data/workflow/career_profile_intake.yaml](../data/workflow/career_profile_intake.yaml)
- [data/site_allowlist.yaml](../data/site_allowlist.yaml)
- [data/workflow/company_site_urls.csv](../data/workflow/company_site_urls.csv)
- [data/logs/workflow_log.jsonl](../data/logs/workflow_log.jsonl)
- [data/screened/live_jobs_kept.csv](../data/screened/live_jobs_kept.csv)
- [data/screened/live_jobs_rejected.csv](../data/screened/live_jobs_rejected.csv)

## Runtime sequence

The canonical runtime sequence is:

1. Refresh target lanes in the configured order.
2. Back up the working state before live processing.
3. Select the live source CSV.
4. Screen rows against the current profile rules.
5. Write kept and rejected outputs.
6. Log workflow events and failure cases.
7. Review only the strongest kept rows in the active queue.

This is the operational loop the repo is built around.

## Qualification rules

A company is eligible only if it meets all of the following:

- direct employer, not a recruiter or vendor wrapper
- healthcare, health-tech, regulated SaaS, or adjacent platform-heavy software signal
- technical role patterns such as platform, cloud, DevOps, SRE, or infrastructure
- acceptable geographic fit
- credible current hiring signal

If any one of these fails, the company stays out of the active list.

## Exclusions

The system explicitly rejects:
- recruiting agencies
- staffing firms
- MSP or consulting wrappers
- generic SaaS companies without the target signal
- broad low-confidence job sources
- companies or sites outside the approved allowlist

## Failure handling

The workflow must not silently continue in ambiguous states.

Required behavior:
- missing company site -> log and stop that branch
- empty role result on an approved careers page -> log and move on
- non-allowlisted domain -> reject and log
- missing target file -> initialize or restore state explicitly and log it
- file-writing subflow -> log the path and the write outcome

This keeps the system bounded and auditable instead of repeatedly prompting or wandering into uncontrolled browsing.

## Operating model

The repo is designed to maintain a short disciplined pursuit list rather than a large noisy funnel.

Recommended working size:
- 5-10 strong direct employers in the core healthcare lane
- 5-10 strong direct employers in the global remote SaaS lane
- 5-10 strong direct employers in the healthcare-adjacent lane
- one active review queue of the best fits, capped by human review capacity

This keeps the process consistent and prevents the target list from becoming low-signal backlog.

## Final principle

A strong target employer list is not a list of possible companies. It is a list of credible, direct, relevant employers that are likely to hire for the role you want and can be reviewed without noise or drift.

That is the design standard for this repo.
