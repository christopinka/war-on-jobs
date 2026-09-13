# Target Company Shortlist Prompt

Use this prompt to generate a small, high-signal target-company list for a software engineer focused on healthcare technology, not hospitals or agency work.

## Prompt

You are building a target company list for a software engineer in healthcare technology.

Goal:
Build a shortlist of direct employers that fit this profile:
- healthcare SaaS / healthtech / regulated software / payer-provider software
- not hospitals, health systems, agencies, contractors, or consulting firms
- backend / platform / integration / cloud / devops / API role fit
- remote-friendly or relevant geography
- strong match for Java / Go / AWS / Kubernetes / APIs / healthcare workflows

Output format:
company | website | category | priority | direct_employer | geography | remote_ok | notes

Rules:
1. Exclude hospitals, health systems, staffing agencies, consulting firms, and generic contract roles.
2. Include only companies that clearly sell software to healthcare.
3. Prefer product/platform companies over provider IT shops.
4. Keep the list small and high-signal, not broad.
5. Rank by fit strength and likely hiring relevance.
6. Include only direct employers.

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

## Notes

This list is intentionally narrower than generic healthcare job searches and is designed to match a software engineer with healthcare platform, cloud, integration, and backend experience rather than hospital operations roles.
