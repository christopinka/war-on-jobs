# Roadmap and backlog

## Current decision

We are keeping the project on a Python-native workflow and a backup-first operating model.

- The canonical refresh method is the ordered lane launcher in [src/war_on_jobs/target_lane_refresh.py](../src/war_on_jobs/target_lane_refresh.py), with the root convenience trigger in [target_lane_refresh.py](../target_lane_refresh.py).
- The live local screening path is [src/war_on_jobs/live_daily_search.py](../src/war_on_jobs/live_daily_search.py), launched via [live_daily_search.py](../live_daily_search.py).
- Every live processing run first creates a timestamped backup under [data/backups](../data/backups).
- Ruff remains the active linting and hygiene baseline.
- We are not introducing a Make-based workflow yet.

## Why this decision

- The project is intentionally small, local, and explicit.
- The actual workflow is already operational without build tooling.
- A backup-first approach reduces the risk of destructive overwrite during refreshes or live filtering.
- Ruff provides the quality gate without creating a heavier project structure.

## Current priority order

1. Keep the three-lane target-refresh workflow stable and explicit.
2. Maintain the three target CSV lanes:
   - core healthcare
   - global remote SaaS
   - healthcare-adjacent
3. Back up the data state before each live run.
4. Filter live or imported job rows locally using the rejection and fit-score logic.
5. Convert the strongest direct-employer matches into a role queue and application workflow.
6. Only add Make or other build tooling if the workflow becomes genuinely repetitive enough to justify it.

## Recommended operating pattern: broad lane search, then top 10

The current search workflow should be run in two passes:

1. Broad pass: review all relevant lanes and collect credible direct-employer roles
2. Rank and cut: score the roles and keep only the strongest 10 for active pursuit

This is the preferred operating model because it preserves optionality without allowing the backlog to become noisy or unreviewable.

### Execution rule

- Do not start by forcing a single company shortlist too early
- Do not keep every plausible role in the active queue
- Rank all credible results by fit, company value, location, and job quality
- Keep the top 10 as the active queue
- Keep the remainder in a lower-priority backlog or watchlist

### Why this matters

A broad lane search surfaces the best opportunities even when they are not obvious from the first company list. A top-10 cut is what turns the system into something a person can actually act on without drowning in low-signal roles.

This is the right balance between breadth and discipline.

## Phase 0: profile intake and decision inputs

Before we lean heavily on the agent context or start filtering jobs automatically, we need a compact intake layer that turns the current situation into structured search inputs.

This is the step that converts a general job-search plan into a real operating profile.

### Goal

Capture the person-level constraints that the search system should respect automatically:
- target roles and preferred technical lanes
- preferred industries and employer types
- desired location and relocation posture
- remote / hybrid / onsite preferences
- work authorization and visa constraints
- compensation floor, target, and financial pressure
- current debt, obligations, or lifestyle constraints
- willingness to travel or work across time zones
- decision factors around consulting, contracting, staff roles, and direct-hire work
- target company size, stage, and culture preferences

### Suggested intake questionnaire

1. Resume and background
   - upload resume and current role summary
   - list strongest technical areas
   - identify the role families you want to pursue
   - summarize most relevant experience and recent wins

2. Career goals
   - what kind of role do you want next?
   - are you optimizing for stability, growth, platform depth, healthcare relevance, or international flexibility?
   - do you want direct-hire, consulting, contract, or staff roles?
   - what is your preference for product engineering vs platform / infrastructure / DevOps work?

3. Role and company fit
   - healthcare / healthtech / regulated SaaS / enterprise infrastructure / remote SaaS
   - preferred seniority range
   - minimum skill alignment for each role family
   - list companies or verticals you actively want to avoid

4. Geography and lifestyle
   - current location and desired future location
   - remote / hybrid / onsite preference
   - willingness to relocate or work internationally
   - time-zone and async collaboration preferences
   - whether you are pursuing an expat or lower-cost lifestyle strategy

5. Financial and life constraints
   - desired salary floor and salary target
   - current debt or financial obligations
   - minimum stability requirements for a role
   - tolerance for lower pay in exchange for a better location, flexibility, or quality of life
   - appetite for shorter-term contract work vs longer-term durable employment

6. Work structure and constraints
   - are you open to async distributed teams?
   - do you prefer direct employers over agency or vendor arrangements?
   - what signals matter most: product maturity, engineering quality, healthcare domain fit, remote work, or strong compensation?
   - what would make a role a clear no for you?

7. Hiring filters
   - list job titles to prioritize
   - list keywords to include or reject
   - list recruiter, staffing, MSP, and vendor patterns to screen out
   - define the minimum level of company clarity needed before you apply

### Purpose in the system

This intake step will become the high-level source of truth for:
- the target lane selection
- the company shortlist priorities
- the job filter rules
- the screening rubric and role-fit scoring
- the minimum keep threshold, represented as `minimum_fit_score` in the YAML profile
- the agent context used to reason about the next job-search cycle

Once the questionnaire is captured, the repo can convert it into structured CSV or YAML inputs and then use that profile to steer the target refresh, the live job filter, and the company-ranking process.

## Deferred / optional work

- Add a Makefile only if the repeated commands become noisy enough to warrant a convenience wrapper.
- Package the workflow as a more formal Python CLI once several commands and subflows are standardized.
- Add a richer ranking or scoring layer for target-company prioritization and role queue sorting.
- Add a true external fetcher if the repo grows beyond the current local-data workflow.

## Status

- Status: active and operational
- Tooling philosophy: keep it simple, Python-first, low-overhead, backup-safe
- Make: deferred, not active
- Live automation: active via the daily search + backup workflow
