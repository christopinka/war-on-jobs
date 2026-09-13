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

The working design is now intentionally narrow and local:

- keep the search lane limited to direct-employer healthcare technology companies
- filter aggressively against hospital IT, agencies, consultants, vendor wrappers, and generic recruiting noise
- use a small local CSV workflow as the system of record rather than broad LinkedIn browsing as the primary workflow
- maintain a curated active shortlist and convert it into a role-level queue for real review and application activity

This system has three connected layers:
1. target-company generation
2. role queue and job review
3. screening and filtering logic

The current active artifact is the shortlist in [data/targets/target_company_active_list.csv](data/targets/target_company_active_list.csv). The operational job queue lives in [data/workflow/role_queue.csv](data/workflow/role_queue.csv).

The design is not "search everywhere." The design is "search a few lanes deeply and keep only the highest-signal employers and roles."

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

Use a three-source model:

### 1. Seed list from known direct employers
Start with a narrow list of companies you already know are direct employers and relevant:
- UST
- Veterans United Home Loans
- Tebra
- EquipmentShare
- MI Softech Inc
- Intuitive.ai
- Snapsheet Inc
- Jobot
- Respondus
- thatDot
- Haystack

This is the starter universe.

### 2. Company pages from relevant LinkedIn searches
Use LinkedIn only as a validation surface, not as the pipeline.

Search narrowly around:
- Platform Engineer healthcare kubernetes aws terraform
- DevOps Engineer healthcare
- Cloud Engineer healthcare
- Healthcare platform engineer

When a company appears in a relevant result, add it only if:
- it is clearly the employer
- the role is direct and technical
- it aligns with healthcare/platform

Do not add every company from a broad search. Only add the ones with a strong match.

### 3. Existing tracker and filtered shortlist
Use the local CSV workflow as a controlled database:
- job_target_tracker.csv
- healthcare_platform_shortlist.csv
- company_targets.csv
- apply_queue.csv

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

Keep the list small.

A good working size is:
- 5 to 10 strong direct employers
- 2 to 3 highly targeted lanes
- one active application queue

Do not maintain a giant list of 50+ names. That turns into a search black hole.

## One-lane operating rule

For this phase, operate in one lane only:
- healthcare platform / cloud / DevOps jobs

Everything else is noise for now.

This keeps your company list tight and your applications targeted.

## Practical workflow

1. Start from a seed list of known direct employers.
2. Validate each one using a narrow LinkedIn or company-careers search.
3. Add only companies with direct-employer, platform-heavy, healthcare-aligned roles.
4. Track them in a local CSV.
5. Keep only the best 5 to 10 names active.
6. Apply to the closest role at each company.
7. Refresh weekly, not daily.

## Next step

The next step is to convert the active company list into a role queue, not just a company queue.

For each company in the active list, track:
- company
- job title
- location
- direct employer signal
- fit score
- apply status
- follow-up date
- notes

This should be a small, disciplined queue built around the best-fit roles rather than raw search volume. The objective is not to chase every healthtech result; the objective is to keep a short list of credible, relevant opportunities and work through them consistently.

## Final principle

A good target employer list is not a list of companies you vaguely like. It is a list of companies that are currently credible, direct, relevant, and likely to hire for the role you want.

That is the standard.
