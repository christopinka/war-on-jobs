# Company-to-role listing workflow

This note captures the practical workflow for moving from a target company list to a usable role list without broad scraping or noisy job-board overload.

This workflow is intentionally narrow. It does not crawl the open web broadly. It visits only the approved company and careers URLs and captures only the relevant role titles and URLs needed for review.

## Goal

The goal is to convert a curated company lane into a short, valid list of direct-employer roles that are worth pursuing. The system should prefer signal over volume.

## Core principle

LinkedIn company posting freshness is real, but it should be treated as a discovery signal, not the system of record.

In practice:
- LinkedIn job posts are often fresher and more visible
- company careers pages are often more canonical for application flow
- ATS pages such as Greenhouse, Lever, or Ashby are often the direct application path

Use LinkedIn to discover and validate active hiring, but confirm the role against the employer's own hiring surface before treating it as a real target.

## Recommended workflow

### 1. Start from a lane

Use the existing lane structure:
- core healthcare
- global remote SaaS
- healthcare adjacent
- consulting / recruiting watchlist

Each lane should be a small, curated company list, not a giant dump.

### 2. Validate companies in the lane

For each target company, check:
- the company page
- LinkedIn company page
- career site or ATS page
- role titles relevant to the target profile

Only keep companies that meet the lane criteria and direct-employer rule.

### 3. Discover role listings narrowly

Focus on company + title searches rather than broad search pipelines.

Preferred signals:
- platform engineer
- cloud engineer
- DevOps engineer
- backend engineer
- infrastructure engineer
- SRE / reliability engineer
- software engineer, product / platform / infrastructure

Preferred company-level sources:
- company careers page
- Greenhouse / Lever / Ashby postings
- LinkedIn company jobs page

### 4. Score each role before adding it

Before a role enters the queue, ask:
- Is it a direct employer?
- Is it in a relevant lane?
- Is the title a strong match?
- Is the location acceptable?
- Is the work relevant to platform, cloud, backend, devops, or healthcare software?
- Is it high-signal enough to pursue?

If the answer is no, do not add it.

## Default rules

Treat these as rejection-worthy unless the role is a strong exception:
- staffing firms
- recruiting agencies
- vendor wrappers
- consulting-heavy roles without direct product engineering relevance
- hospital IT roles
- generic non-technical postings

## Practical sourcing hierarchy

Use this order:
1. LinkedIn company jobs page for fast signal on active hiring
2. Company careers page or ATS for canonical listing and application route
3. Local tracker / CSV as the system of record for the kept queue

This keeps the workflow efficient without relying on broad scraping or noisy job-board aggregation.

## Why this is the right boundary

The repo is designed to be a local, direct-employer targeting system. That means the role-finding path should be:
- narrow
- curated
- direct
- reviewable
- scoreable

It should not be a giant internet crawl.

## Recommended output shape

Each kept role should include:
- company
- role_title
- location
- job_url
- source
- lane
- fit_score
- status
- notes

This turns the role list into something that can be acted on by a human instead of just being a noisy data dump.

## Working policy

A real role is only worth keeping if it is both:
- fresh enough to matter
- strong enough to pursue

LinkedIn often gives freshness; the company source gives trust. The combination is the best practical workflow.

## Direct outreach: when and how to contact hiring staff

Direct outreach is useful, but it should be a second-pass move for already-strong fit roles. It works best when it is targeted and specific.

### Good outreach pattern

A direct message should be short, relevant, and role-specific.

Template:

Hi [Name],

I saw the [Role Title] opening at [Company] and my background lines up with [2-3 concrete skills / experience points]. I have experience with [relevant stack], and I would be very interested in learning more about the team or the role if it is still open.

I included the posting link below for reference. Thank you for your time, and I’d appreciate any guidance on the right team or hiring contact.

Best,
[Name]

### Best people to contact
- hiring manager
- engineering manager
- recruiter attached to the team
- team lead or staff engineer for the area

### What to avoid
- mass outreach without context
- generic “I’m interested” notes
- contacting multiple random people in the same company
- messaging before checking the actual job posting and fit

## Manual review workflow: how to get to a list you can actually act on

Yes, we can get to a list that is usable for manual review.

The process should be:
1. refresh the target lane companies
2. validate or discover active roles in those companies
3. keep only direct-employer, role-matched postings
4. score each role
5. write the kept rows to a role queue CSV
6. review the queued items manually
7. apply or contact only the top 5 to 10 strong fits

A good manual review list should be small and clearly prioritized.

Recommended CSV columns:
- company
- role_title
- location
- job_url
- lane
- source
- fit_score
- status
- applied
- follow_up_date
- notes

This creates a list that is narrow enough to manually work through without feeling like a giant backlog.

## Top-10 active review checklist

After collecting roles across all relevant lanes, use this checklist to cut down to the active list.

A role should stay in the active queue only if it passes most or all of these checks:

- direct employer, not staffing or consulting wrapper
- role title aligns closely with target profile and technical lane
- company is a meaningful strategic or tactical target
- location is acceptable for the current search posture
- role is recent enough to matter
- product or platform work is materially relevant
- the fit score is high enough to justify a real application or outreach
- there is a clear next action: apply, contact, or follow up

If the role fails more than one of these checks, it belongs in the backlog or watchlist instead of the top 10.

The active review list should be small enough to handle manually:
- top 10 at most for active pursuit
- remaining roles tracked but not actioned immediately
- follow-up dates and status kept current

## Bottom line

Use LinkedIn as a fast discovery layer, but keep the employer careers page / ATS as the trusted source of truth for application and follow-up. This is the most reliable pattern for turning companies into role listings without drowning in low-signal noise.

The practical end state is a short, curated manual list of real roles that are worth applying to or contacting directly.
