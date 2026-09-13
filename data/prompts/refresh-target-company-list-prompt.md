# Refresh Target Company List Prompt

Use this prompt to refresh the active shortlist for a software engineer focused on healthcare technology, not hospitals, consulting, or staffing work.

## Prompt

You are refreshing a target company list for a software engineer in healthcare technology.

Goal:
Build a small, high-signal shortlist of direct employers that fit this profile:
- healthcare SaaS / healthtech / regulated software / payer-provider software
- not hospitals, health systems, agencies, contractors, or consulting firms
- backend / platform / integration / cloud / devops / API role fit
- remote-friendly or relevant geography
- strong match for Python / Java / Go / AWS / Kubernetes / SQL / APIs / healthcare workflows

Output target file:
- Populate [data/targets/target_company_active_list.csv](../targets/target_company_active_list.csv) with the final shortlist for the core healthcare lane.
- If a company is explicitly adjacent or secondary, it may be moved to [data/targets/adjacent_lane_targets.csv](../targets/adjacent_lane_targets.csv) instead of the active list.
- Append new companies to the CSV rather than replacing the entire file.
- If a company already exists, update that row in place instead of creating a duplicate.
- Keep the list curated and small; do not overwrite the full file with a broad dump.

Output format:
company | website | category | priority | direct_employer | geography | remote_ok | notes

Rules:
1. Exclude hospitals, health systems, staffing agencies, consulting firms, and generic contract roles.
2. Include only companies that clearly sell software to healthcare.
3. Prefer product/platform companies over provider IT shops.
4. Keep the list small and high-signal, not broad.
5. Rank by fit strength and likely hiring relevance.
6. Include only direct employers.
7. Favor companies with a clear software product, platform, data, or interoperability story.
8. Do not include broad healthcare employers whose core work is hospital operations or internal IT.

Target categories:
- healthcare SaaS
- digital health
- payer software
- provider workflow software
- care coordination / care management software
- interoperability / HL7 / FHIR / API vendor software
- claims / revenue cycle / billing software
- telehealth / remote monitoring software
- clinical data / population health / analytics software

Do not include:
- hospitals
- health system employers
- hospital IT departments
- agencies or staffing firms
- consulting or contractor shops
- generic non-healthcare SaaS companies

Return only the final shortlist, sorted by priority.

## Example output
company | website | category | priority | direct_employer | geography | remote_ok | notes
Epic | https://epic.com | provider workflow / EHR adjacent | high | yes | us | maybe | healthtech software vendor
athenahealth | https://www.athenahealth.com | healthcare SaaS | high | yes | us | maybe | provider and payer workflow software
Change Healthcare | https://www.changehealthcare.com | claims / revenue cycle | high | yes | us | maybe | healthcare software vendor
Teladoc Health | https://www.teladoc.com | digital health | medium | yes | us | maybe | virtual care and health platform
Veeva | https://www.veeva.com | regulated SaaS | medium | yes | us | maybe | life sciences and healthcare software

## Practical use
Use this prompt to refresh the active target list in [data/targets/target_company_active_list.csv](data/targets/target_company_active_list.csv) and keep the queue tight and high-signal.
