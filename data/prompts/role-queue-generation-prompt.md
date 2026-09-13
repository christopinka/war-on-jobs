# Generate Role Queue from Company Lane Prompt

Use this prompt to turn a curated company lane into a short, valid role queue for direct manual review.

## Prompt

You are generating a role queue for a software engineer targeting a narrow set of direct-employer companies.

Goal:
Build a short, high-signal list of active roles worth reviewing manually. The output should be a small queue, not a giant dump of jobs.

The workflow is:
1. Start from the active company lane or target list.
2. Check the company page, LinkedIn company jobs page, and relevant ATS pages only for those companies.
3. Keep only roles that match the current profile and lane criteria.
4. Prioritize direct-employer technical roles over recruiting, consulting, vendor, or staffing wrappers.
5. Output only a short review queue of the strongest fits.

Output target file:
- Populate [data/workflow/role_queue.csv](../workflow/role_queue.csv) with the working queue.
- Append new rows rather than replacing the entire file.
- If a role already exists, update that row in place instead of creating a duplicate.
- Keep the queue small, curated, and reviewable by hand.

Output format:
company | website | job_title | location | role_type | fit_score | status | priority | source | notes

Rules:
1. Include only direct employers, not staffing firms, recruiters, MSPs, or consulting shops.
2. Keep the role list tied to the active lane and the current operating profile.
3. Prefer platform, cloud, devops, backend, infrastructure, integration, or healthcare software roles.
4. Exclude hospital IT, vendor-only roles, generic consulting work, and jobs that are not technically relevant.
5. Use LinkedIn company jobs for freshness and the employer careers page or ATS as the canonical source before a role is considered real.
6. Rank each role by fit strength and likely application value.
7. Keep the queue short; do not add every job from a broad search.
8. Only include jobs that are credible, current, and worth manual review.

Target role families:
- platform engineer
- cloud engineer
- DevOps engineer
- backend engineer
- infrastructure engineer
- SRE / reliability engineer
- software engineer, product / platform / infrastructure
- healthcare SaaS / regulated software / workflow integration

Do not include:
- recruiting agency jobs
- staffing or MSP roles
- consulting-heavy roles without direct engineering relevance
- hospital IT operations jobs
- generic non-technical postings
- broad job search dumps with no direct employer signal

Return only the final queue, sorted by priority and fit score.

## Example output
company | website | job_title | location | role_type | fit_score | status | priority | source | notes
Epic | https://www.epic.com | Senior Software Engineer - Platform & Integrations | Remote - US | platform/backend | 95 | new | high | company_careers | Strong direct-employer fit with API and platform work.
GitLab | https://about.gitlab.com | Senior DevOps Engineer | Remote - Global | devops/platform | 92 | new | high | linkedin_company_jobs | Strong remote-first product company with platform depth.
athenahealth | https://www.athenahealth.com | Senior Backend Engineer | Remote - US | backend/platform | 90 | new | high | company_careers | Good healthcare SaaS fit with technical and product-heavy backend work.

## Practical use
Use this prompt to turn a curated company lane into a short, actionable manual review list in [data/workflow/role_queue.csv](../workflow/role_queue.csv).
