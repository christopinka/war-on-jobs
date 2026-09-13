# Target employer assembly and multi-lane role-queue design

This is the working design for the local job-search system. It is not only a company list; it is the first layer of a narrow, operational pipeline that moves from employer targeting to role screening and application tracking.

## Goal

Build a disciplined, direct-employer system for a software engineer with a strong preference for:
- healthcare or regulated software
- platform / cloud / DevOps / infrastructure engineering
- remote-friendly or geographically acceptable hiring
- technical roles that fit a product-company environment

The goal is not to collect a giant list. The goal is to collect a short list that is concrete, relevant, and actionable, then turn that list into a disciplined role queue.

## Current operating design

The working design is now intentionally structured as three lanes, each with its own CSV and refresh prompt:

1. Core healthcare technology lane
   - built around healthcare SaaS, regulated software, payer-provider workflow, interoperability, and data-heavy healthtech
   - active artifact: [data/targets/target_company_active_list.csv](data/targets/target_company_active_list.csv)
   - prompt: [data/prompts/refresh-target-company-list-prompt.md](data/prompts/refresh-target-company-list-prompt.md)

2. Global remote SaaS lane
   - built around remote-first, direct-employer product companies with strong devops, platform, backend, cloud, and infrastructure fit
   - active artifact: [data/targets/company_targets.csv](data/targets/company_targets.csv)
   - prompt: [data/prompts/refresh-global-remote-saas-target-list-prompt.md](data/prompts/refresh-global-remote-saas-target-list-prompt.md)

3. Healthcare-adjacent lane
   - built around digital health, patient engagement, care navigation, value-based care, and healthcare workflow software
   - active artifact: [data/targets/adjacent_lane_targets.csv](data/targets/adjacent_lane_targets.csv)
   - prompt: [data/prompts/refresh-healthcare-adjacent-target-list-prompt.md](data/prompts/refresh-healthcare-adjacent-target-list-prompt.md)

This system has three connected layers:
1. target-company generation
2. role queue and job review
3. screening and filtering logic

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
   - remote-first product SaaS with a strong technical platform story
   - healthcare-adjacent workflow software

3. Relevant role signal
   - platform engineer
   - cloud engineer
   - DevOps engineer
   - infrastructure engineer
   - SRE / reliability engineer
   - backend / distributed systems / observability engineer
   - software engineer in a product company with strong technical depth

4. Geographic fit
   - remote-friendly if remote is acceptable
   - or in a target geography that matches your constraints

5. Technical fit
   - AWS / Kubernetes / Terraform / CI/CD / Linux / observability / Python / SQL / backend systems / platform operations

If a company fails one of these tests, it should not be on the list.

## Source model

Use a three-source model:

### 1. Seed list from known direct employers
Start with a narrow list of companies you already know are direct employers and relevant to one of the lanes. Keep the seed list intentionally short and curated rather than broad.

### 2. Company pages from relevant searches
Use LinkedIn or company-careers pages only as a validation surface, not as the primary pipeline.

Search narrowly around:
- Platform Engineer healthcare kubernetes aws terraform
- DevOps Engineer healthcare
- Remote platform engineer SaaS
- Healthcare platform engineer
- Digital health software engineer

When a company appears in a relevant result, add it only if:
- it is clearly the employer
- the role is direct and technical
- it aligns with one of the active lanes

Do not add every company from a broad search. Only add the ones with a strong match.

### 3. Existing tracker and filtered shortlist
Use the local CSV workflow as a controlled database:
- [data/targets/target_company_active_list.csv](data/targets/target_company_active_list.csv)
- [data/targets/company_targets.csv](data/targets/company_targets.csv)
- [data/targets/adjacent_lane_targets.csv](data/targets/adjacent_lane_targets.csv)
- [data/workflow/role_queue.csv](data/workflow/role_queue.csv)

This keeps the employer list tied to actual jobs and avoids re-adding noisy or stale names.

## Company qualification checklist

For each company, answer these questions:

- Is it a direct employer?
- Is it in one of the active lanes?
- Does it have platform / cloud / infrastructure / DevOps / backend job patterns?
- Is the role technical enough to fit your background?
- Is the location acceptable?
- Is this a real, current hiring pattern rather than a generic corporate brand?

If the answer is no to any of these, exclude it.

## What to exclude

Exclude without hesitation:
- recruiting agencies
- staffing firms
- contract-only vendors
- generic SaaS companies with no technical or healthcare fit
- broad job sources with no direct employer evidence
- random platform companies that are not a fit for your target lane

## A simple target employer spreadsheet schema

Use a CSV with this shape:

- company
- website
- category
- priority
- direct_employer
- geography
- remote_ok
- notes
- target_roles
- apply_status

Example:

company,website,category,priority,direct_employer,geography,remote_ok,notes,target_roles,apply_status
GitLab,https://about.gitlab.com,global remote SaaS,high,yes,global,yes,"remote-first product company","platform, devops, backend",new
Epic,https://www.epic.com,healthcare platform,high,yes,us,maybe,"healthtech software vendor","backend, platform, API",new

## Recommended operating model

Keep the list small.

A good working size is:
- 5 to 10 strong direct employers in the core healthcare lane
- 5 to 10 strong direct employers in the global remote SaaS lane
- 5 to 10 strong direct employers in the healthcare-adjacent lane
- one active application queue that draws from all three when relevant

Do not maintain a giant list of 50+ names. That turns into a search black hole.

## Lane operating rule

For this phase, keep the lanes separate and explicit:
- healthcare core is the strongest signal
- remote SaaS is the overseas-friendly hedge
- healthcare-adjacent is the secondary context lane

This keeps your company list tight and your applications targeted.

## Practical workflow

1. Start from a seed list of known direct employers for the selected lane.
2. Validate each one using a narrow search or company-careers review.
3. Add only companies with direct-employer, technical, lane-aligned roles.
4. Track them in the relevant CSV.
5. Append new rows, and if a company already exists, update that row in place rather than duplicating it.
6. Keep only the best names active in that lane.
7. Apply to the closest role at each company.
8. Refresh weekly, not daily.

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

This should be a small, disciplined queue built around the best-fit roles rather than raw search volume. The objective is not to chase every result; the objective is to keep a short list of credible, relevant opportunities and work through them consistently.

## Final principle

A good target employer list is not a list of companies you vaguely like. It is a list of companies that are currently credible, direct, relevant, and likely to hire for the role you want.

That is the standard.
