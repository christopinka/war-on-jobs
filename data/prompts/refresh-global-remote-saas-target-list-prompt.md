# Refresh Global Remote SaaS Target List Prompt

Use this prompt to refresh the non-healthcare SaaS lane for a software engineer who wants remote-friendly, direct-employer, product-company roles with strong devops, platform, backend, cloud, and infrastructure fit.

## Prompt

You are refreshing a target company list for a software engineer in remote-first, globally operating SaaS companies.

Goal:
Build a small, high-signal shortlist of direct employers that fit this profile:
- product / B2B SaaS company
- remote-friendly or international hiring
- direct employer, not consulting or staffing
- strong match for platform, cloud, devops, infrastructure, backend, distributed systems, or developer tooling
- not healthcare-specific unless the company is a software vendor with a strong platform or workflow product
- good fit for overseas or globally distributed work

Output target file:
- Populate [data/targets/company_targets.csv](../targets/company_targets.csv) for the global remote SaaS lane.
- If a company is a strong healthcare-related SaaS fit, it may also be copied into [data/targets/target_company_active_list.csv](../targets/target_company_active_list.csv) only if it is still relevant to the core healthcare lane.
- Append new companies to the CSV rather than replacing the entire file.
- If a company already exists, update that row in place instead of creating a duplicate.
- Keep the list curated and small; do not overwrite the full file with a broad dump.

Output format:
company | website | category | priority | direct_employer | geography | remote_ok | notes

Rules:
1. Include only direct employers with real product-company operations.
2. Prefer remote-first or globally distributed companies.
3. Exclude agencies, staffing firms, MSPs, VMS, consulting firms, and contractor wrappers.
4. Favor product companies with strong developer/platform engineering culture.
5. Keep the list small, curated, and relevant; do not dump broad SaaS lists.
6. Rank by fit strength and likely hiring relevance for devops/platform/backend work.
7. Favor companies where the role is likely to be technical and product-oriented rather than service-heavy.
8. Do not include local-only companies, hospital IT shops, or generic consumer SaaS with no clear technical fit.

Target categories:
- devops / platform engineering / SRE
- cloud infrastructure / Kubernetes / AWS / GCP / Azure
- backend / distributed systems / reliability
- developer tooling / internal platform / observability
- security / networking / infra automation
- B2B SaaS with strong international remote hiring

Do not include:
- consulting firms
- agencies or staffing shops
- MSP/VMS firms
- contractor-heavy employers
- local-only employers with no global hiring pattern
- random consumer SaaS without strong technical product fit

Return only the final shortlist, sorted by priority.

## Example output
company | website | category | priority | direct_employer | geography | remote_ok | notes
GitLab | https://about.gitlab.com | devops / platform SaaS | high | yes | global | yes | strong remote-first engineering culture
Datadog | https://www.datadoghq.com | observability / platform | high | yes | global | yes | strong devops and platform fit
Cloudflare | https://www.cloudflare.com | infra / networking / platform | high | yes | global | yes | good remote-friendly infrastructure company
HashiCorp | https://www.hashicorp.com | devops / infra | medium | yes | global | yes | platform and automation-heavy
Atlassian | https://www.atlassian.com | SaaS / devtools | medium | yes | global | yes | global SaaS with strong product engineering culture

## Practical use
Use this prompt to refresh the non-healthcare global SaaS lane in the target list and keep it focused on direct employers with genuine product and infrastructure work.
