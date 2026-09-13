# Company career site and job discovery

## Recommendation

Use the employer career site and ATS as the primary source of job listings.

Use LinkedIn as a secondary discovery signal only when it helps confirm that a company is active and relevant. Do not treat a logged-out or guest LinkedIn endpoint as a reliable jobs API.

This is the recommended direction for the repo and for the daily search workflow. The system should also enforce a repo-owned domain allowlist and company URL registry so the role-discovery pass stays bounded and auditable.

## What counts as a targeted role-discovery pass

This is not a broad scraper.

A targeted role-discovery pass means:
- visiting only the approved company and careers URLs from the allowlist
- collecting only role titles and relevant URLs for those companies
- keeping the crawl narrow to company pages, not an uncontrolled web crawl
- storing only a compact, reviewable role set in the local CSV workflow
- logging each file write, source selection, and failure case to the workflow log
- stopping cleanly when a site is unavailable or does not list jobs, rather than prompting back endlessly

This is a narrow extraction process, not a general-purpose scraping workflow.

## Why

A logged-out or guest LinkedIn page may provide some company-level metadata, such as:
- company name
- company description
- some public profile context
- a link to the company job page or a company lifecycle signal

But it is not a stable or comprehensive source for:
- active job listings
- a predictable job feed
- a trustworthy role inventory across companies
- a direct source of truth for application flow

The same is true for many public company pages: they can provide company context and hiring pages, but the real role inventory usually lives in the employer’s ATS or careers portal.

## Recommended source hierarchy

Use this order:
1. Target company list from the active lane
2. Company career page or ATS
3. LinkedIn company page / company jobs page for freshness and validation
4. Local CSV queue as the system of record

This keeps the workflow narrow, credible, and repeatable.

## Practical rule

If a job is not visible on the employer’s own career page or ATS, it should not be treated as a fully trusted target. LinkedIn can help confirm hiring activity, but it should not be the canonical record of a real open role.

## Evidence from current public company pages

We validated that the following company pages are publicly accessible without a logged-in LinkedIn session:

- Oracle Careers: public careers landing page accessible; job-search links are present and publicly navigable
- Epic Careers: public careers landing page is accessible; company mission and public career content are present
- athenahealth Careers: public careers page redirects to a public jobs site

This confirms that the employer-side path is the better route for real job collection and application tracking.

## Recommended workflow

1. Start from the active lane target list
2. Visit company public career pages or ATS pages for each relevant employer
3. Search for titles relevant to the target role profile
4. Keep only direct-employer jobs that match the lane and role criteria
5. Score and rank the results
6. Keep a top-10 active review queue
7. Store the accepted roles in the local CSV queue

## Operational stance

The repo should treat LinkedIn as a discovery and validation layer, not the job source of truth.

The system should keep a narrow, direct-employer focus and rely on public careers pages and ATSs for the actual role data.
