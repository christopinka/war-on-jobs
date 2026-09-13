# Refresh Healthcare-Adjacent Target List Prompt

Use this prompt to refresh the adjacent healthcare lane for companies that are not strictly healthcare-only vendors but are still highly relevant to healthcare workflows, operations, patient engagement, care coordination, or digital health product work.

## Prompt

You are refreshing a target company list for a software engineer in healthcare-adjacent technology.

Goal:
Build a small, high-signal shortlist of direct employers that fit this profile:
- healthcare-related workflow software
- digital health / care operations / patient engagement
- payer-provider workflow tools
- value-based care or care navigation tools
- healthcare analytics / population health / care coordination
- software vendors adjacent to healthcare, but not generic SaaS

Output target file:
- Populate [data/targets/adjacent_lane_targets.csv](../targets/adjacent_lane_targets.csv) for the healthcare-adjacent lane.
- Keep only the strongest companies in the active healthtech list in [data/targets/target_company_active_list.csv](../targets/target_company_active_list.csv); use the adjacent lane for secondary, adjacent-fit names.
- Append new companies to the CSV rather than replacing the entire file.
- If a company already exists, update that row in place instead of creating a duplicate.
- Keep the list curated and small; do not overwrite the full file with a broad dump.

Output format:
company | website | category | priority | direct_employer | geography | remote_ok | notes

Rules:
1. Include only direct employers with a credible product or software business.
2. Exclude hospitals, health systems, internal hospital IT departments, and pure healthcare delivery operations unless the company is clearly a software vendor.
3. Prefer companies with a strong product engineering or platform story.
4. Favor workflow, data, interoperability, patient experience, or care operations products.
5. Keep the list small and high-signal, not broad.
6. Rank by fit strength and likely hiring relevance.
7. Prefer companies with technical product teams rather than consulting-heavy delivery teams.
8. Exclude generic non-healthcare SaaS unless the company is clearly serving healthcare processes or workflows.

Target categories:
- digital health / telehealth / care delivery software
- care navigation / care coordination / patient support platforms
- payer workflow / claims / billing / revenue cycle software
- provider workflow / operations / scheduling / revenue software
- population health / analytics / care management tools
- value-based care / patient engagement / digital front door software

Do not include:
- hospitals
- clinic systems or provider networks with no software product
- agencies / staffing / consulting firms
- generic enterprise SaaS unrelated to healthcare workflows
- pure local operations companies with no real healthcare product focus

Return only the final shortlist, sorted by priority.

## Example output
company | website | category | priority | direct_employer | geography | remote_ok | notes
Teladoc Health | https://www.teladoc.com | digital health / telehealth | high | yes | us | maybe | strong digital health platform
Cedar | https://www.cedar.com | patient financing / revenue cycle | high | yes | us | maybe | healthcare operations software
Phreesia | https://www.phreesia.com | patient intake / engagement | high | yes | us | maybe | healthcare workflow and patient experience
Aledade | https://www.aledade.com | value-based care / provider operations | medium | yes | us | maybe | healthcare operations and analytics software
Mend | https://www.mend.com | care navigation / patient support | medium | yes | us | maybe | digital health and care coordination

## Practical use
Use this prompt to refresh the healthcare-adjacent lane in the target list while keeping it focused on direct employers and genuine healthcare workflow software rather than generic SaaS or hospital-only employers.
