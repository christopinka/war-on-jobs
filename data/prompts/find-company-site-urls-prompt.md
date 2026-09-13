# Company site URL discovery prompt

Use this prompt when you need to find and validate the public company and careers URLs for the active allowlist.

## Goal

Convert the repo allowlist into a small, relevant set of company website URLs and careers URLs that can be used for direct company and role discovery.

Source of truth:
- [data/site_allowlist.yaml](../site_allowlist.yaml)

Output target:
- [data/workflow/company_site_urls.csv](../workflow/company_site_urls.csv)

## Workflow

1. Read the allowlist from [data/site_allowlist.yaml](../site_allowlist.yaml).
2. For each allowed company domain, find the primary company website and the most likely public careers page.
3. Prefer the company homepage and official careers URL over random or secondary pages.
4. Keep the output narrow and relevant; do not add unrelated domains.
5. Validate that each URL belongs to the company domain or its official careers subdomain.
6. Store the results in a CSV with a small, reviewable schema.
7. If a site is inaccessible or the page does not resolve, do not retry indefinitely. Record the domain and mark it as `site_unavailable` or `no_public_careers_page` and continue.
8. If a company has no public careers page or no relevant jobs page, stop the page-expansion step and do not ask for more input. Record the result and move on.
9. If a company page is valid but has no relevant jobs, do not treat that as a prompt failure. It is a valid empty result and should be logged as such.

## Output schema

company | domain | company_url | careers_url | source | notes

## Rules

1. Only include domains that match the repo allowlist.
2. Prefer official corporate pages and official careers or ATS pages.
3. If a company uses a careers subdomain, include both the homepage and the public careers page.
4. Do not add agencies, staffing firms, consulting shops, or unrelated vendor sites.
5. Keep the list compact and useful for direct browsing and role discovery.
6. If a company has no public careers page, keep the homepage only and flag it as `no_public_careers_page` in the notes.
7. If the company site is down, redirects unexpectedly, or does not resolve, record the domain and mark it as `site_unavailable`; do not keep looping on retries.
8. If the company has a valid page but no relevant jobs are visible, record it as `no_jobs_found` and move on; do not ask for permission to continue.
9. If a page fails validation, do not invent a replacement URL. Only keep the domain and a note.
10. Do not broaden the search beyond the allowlist without explicit approval.

## Failure handling

This is a strict no-loop workflow.

Failure cases must be handled as follows:
- `site_not_found` -> record the domain with a note and continue
- `site_unavailable` -> record the domain and continue
- `no_public_careers_page` -> keep the homepage only and continue
- `no_jobs_found` -> record the result and continue
- `domain_mismatch` -> reject the URL and do not keep it

The agent must never stall on a missing page and must never ask for more input just to continue with the next valid company.

## Example output

company | domain | company_url | careers_url | source | notes
Epic | epic.com | https://www.epic.com | https://careers.epic.com/ | public_site | Official careers page found.
Oracle | oracle.com | https://www.oracle.com | https://www.oracle.com/careers/ | public_site | Careers page present and publicly accessible.
athenahealth | athenahealth.com | https://www.athenahealth.com | https://careers.athenahealth.com/us/en/ | public_site | Public ATS page found.

## Practical use

Use this prompt before running a role-level company review. It provides the narrow public URL set that should be used for the subsequent role-discovery pass.
