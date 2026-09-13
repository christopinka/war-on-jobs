# Target employer assembly and role-queue design

This is the working design for the healthcare/platform job-search system. It is not only a company list; it is the first layer of a narrow, operational pipeline that moves from employer targeting to role screening and application tracking.

## Goal

Build a small, direct-employer system for a software engineer in the healthcare technology lane:
- healthcare or regulated software
- platform / cloud / DevOps / infrastructure engineering
- remote-friendly or geographically acceptable hiring
- technical roles that fit your background and interests

The goal is not to collect a giant list. The goal is to collect a short list that is concrete, relevant, and actionable, then turn that list into a disciplined role queue.

## Current operating design

The working design is now intentionally narrow, multi-lane, and automation-friendly:

- keep the search organized into explicit target lanes instead of one giant mixed list
- filter aggressively against hospital IT, agencies, consultants, vendor wrappers, and generic recruiting noise
- use a small local CSV workflow as the system of record rather than broad LinkedIn browsing as the primary workflow
- maintain a curated active shortlist and convert it into a role-level queue for real review and application activity
- back up the repo state before each live run so the current curated data is never silently clobbered

This system has five connected layers:
1. target-company generation by lane
2. ordered lane refresh and update semantics
3. live job ingestion or tracker review
4. real-time local screening and fit scoring
5. role queue and application tracking

The active artifacts are:
- [data/targets/target_company_active_list.csv](../data/targets/target_company_active_list.csv)
- [data/targets/company_targets.csv](../data/targets/company_targets.csv)
- [data/targets/adjacent_lane_targets.csv](../data/targets/adjacent_lane_targets.csv)
- [data/workflow/job_target_tracker.csv](../data/workflow/job_target_tracker.csv)
- [data/workflow/career_profile_intake.yaml](../data/workflow/career_profile_intake.yaml)
- [data/screened/live_jobs_kept.csv](../data/screened/live_jobs_kept.csv)
- [data/screened/live_jobs_rejected.csv](../data/screened/live_jobs_rejected.csv)

The screening engine reads from the profile intake before deciding whether a job is kept or rejected. In practice, the active profile controls:
- keyword filters for relevant and reject-worthy terms
- the minimum acceptable fit score
- allowed geography preferences
- the working definition of direct-employer signal

### Exact runtime sequence

The current implementation has a single canonical workflow with two explicit phases:

1. Refresh the target-company lanes with the ordered lane registry
2. Back up the current working state and run the live screen against the tracker rows

The root user entrypoint is:

- python3 workflow.py

This is the actual launch sequence reflected in the repo. It refreshes the three target CSVs first, then creates the backup and writes the kept/rejected live screen outputs.

The design is not "search everywhere." The design is "search a few lanes deeply, keep only the highest-signal employers and roles, and protect the working data with backups before each live pass."

## Rule set

Only add a company if it meets all of the following:

1. Direct employer
   - not a recruiting agency
   - not a vendor
   - not a staffing firm
   - not a contract wrapper

2. Relevant industry signal
   - healthcare
   - health-tech
   - regulated SaaS
   - healthcare software / claims / interoperability / patient workflows
   - adjacent platform-heavy or infrastructure-heavy software environments

3. Relevant role signal
   - platform engineer
   - cloud engineer
   - DevOps engineer
   - infrastructure engineer
   - SRE / reliability engineer
   - site reliability / operations engineering in a software-heavy environment

4. Geographic fit
   - remote-friendly if remote is acceptable
   - or in a target geography that matches your constraints

5. Technical fit
   - AWS / Kubernetes / Terraform / CI/CD / Linux / observability / Python / SQL / backend systems / platform operations

If a company fails one of these tests, it should not be on the list.

## Source model

Use a four-part model that matches the current implementation:

### 1. Seed lane list from known direct employers
Start with a curated list of direct employers for each lane:
- core healthcare lane: Epic, athenahealth, Oracle Health, Change Healthcare, Veeva, Optum, Surescripts, etc.
- global remote SaaS lane: GitLab, Datadog, Cloudflare, HashiCorp, Atlassian, Snyk
- healthcare-adjacent lane: Teladoc, Cedar, Phreesia, Aledade, Mend, Arcadia

These are the active seeds for the three-lane structure.

### 2. Ordered lane refresh workflow
Use the ordered lane launcher to refresh each lane in a predictable sequence:
- core_healthcare
- global_remote_saas
- healthcare_adjacent

This makes the refresh process deterministic and protects the repo from accidental overwrite behavior.

### 3. Company pages and direct validation only
Use LinkedIn or company-careers pages only as a validation surface, not as the primary pipeline.

Search narrowly around:
- platform engineer healthcare kubernetes aws terraform
- devops engineer healthcare
- healthcare backend integration engineer
- remote platform engineer SaaS

When a company appears in a relevant result, add it only if:
- it is clearly the employer
- the role is direct and technical
- it aligns with one of the active lanes

Do not add every company from a broad search. Only add the ones with a strong match.

### 4. Local tracker and filtered shortlist
Use the local CSV workflow as a controlled database:
- [data/targets/target_company_active_list.csv](../data/targets/target_company_active_list.csv)
- [data/targets/company_targets.csv](../data/targets/company_targets.csv)
- [data/targets/adjacent_lane_targets.csv](../data/targets/adjacent_lane_targets.csv)
- [data/workflow/job_target_tracker.csv](../data/workflow/job_target_tracker.csv)
- [data/screened/live_jobs_kept.csv](../data/screened/live_jobs_kept.csv)
- [data/screened/live_jobs_rejected.csv](../data/screened/live_jobs_rejected.csv)

This keeps the employer list tied to actual jobs and avoids re-adding noisy or stale names.

## Company qualification checklist

For each company, answer these questions:

- Is it a direct employer?
- Is it in healthcare, health-tech, regulated SaaS, or adjacent platform-heavy tech?
- Does it have platform / cloud / infrastructure / DevOps job patterns?
- Is the role technical enough to fit your background?
- Is the location acceptable?
- Is this a real, current hiring pattern rather than a generic corporate brand?

If the answer is no to any of these, exclude it.

## What to exclude

Exclude without hesitation:
- recruiting agencies
- staffing firms
- contract-only vendors
- generic SaaS companies with no healthcare/platform signal
- broad job sources with no direct employer evidence
- random platform companies that are not a fit for your target lane

## A simple target employer spreadsheet schema

Use a CSV with this shape:

- company
- website
- priority
- category
- notes
- direct_employer
- healthcare_signal
- platform_signal
- geography_fit
- source

Example:

company,website,priority,category,direct_employer,healthcare_signal,platform_signal,geography_fit,source
UST,https://www.ust.com,high,healthcare_platform,true,true,true,true,seed
Veterans United Home Loans,https://www.veteransunited.com,high,healthcare_platform,true,true,true,true,linkedin

## Recommended operating model

Keep the list small and lane-specific.

A good working size is:
- 5 to 10 strong direct employers in the core healthcare lane
- 5 to 10 strong direct employers in the global remote SaaS lane
- 5 to 10 strong direct employers in the healthcare-adjacent lane
- one active application queue driven by fit and signal rather than raw volume

Do not maintain a giant list of 50+ names. That turns into a search black hole.

## Lane operating rule

Keep the lanes separate and explicit:
- healthcare core is the strongest signal
- remote SaaS is the hedge for remote-friendly product roles
- healthcare-adjacent is the secondary context lane

This keeps your company list tight and your applications targeted.

## Practical workflow

1. Back up the current data state before any live processing run.
2. Refresh the target-company list for the active lane using the ordered Python workflow.
3. Validate only the strongest direct-employer matches using a narrow LinkedIn or company-careers search.
4. Add only companies with direct-employer, technical, lane-aligned roles.
5. Track the results in the local CSV system.
6. Run the live filtering pass against the current job tracker.
7. Keep only the best-fit rows in the live jobs kept file and reject noise in the rejected file.
8. Apply to the closest role at each company.
9. Refresh the target lists and re-run the live filter on a consistent cadence.

## Next step

The next step is to convert the active company list into a role queue and keep a disciplined live-filtering loop.

For each company in the active list, track:
- company
- job title
- location
- direct employer signal
- fit score
- apply status
- follow-up date
- notes

This should be a small, disciplined queue built around the best-fit roles rather than raw search volume. The objective is not to chase every result; the objective is to keep a short list of credible, relevant opportunities and work through them consistently.

The current live workflow already does the first operational step: a timestamped backup and a filtered kept/rejected pass over the active tracker. That is the working local loop for now.

## Final principle

A good target employer list is not a list of companies you vaguely like. It is a list of companies that are currently credible, direct, relevant, and likely to hire for the role you want.

That is the standard.
