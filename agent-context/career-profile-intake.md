# Career profile intake

This is the operating-profile intake for the job-search system. It is meant to be filled out once and then reused to steer target-company selection, filtering, role ranking, and job-search priorities.

## Why this exists

The repo works better when it is configured with a real operating profile instead of broad, vague search intent. The intake captures the stuff that changes which jobs are worth pursuing and which ones should be auto-rejected.

## Intake fields

### 1. Resume and history
- Current resume or resume summary
- Current role and recent wins
- Strongest technical areas
- Most relevant experience in backend, platform, integration, migration, cloud, DevOps, healthcare, or enterprise systems
- Years of experience and seniority target

### 2. Career goals
- Desired role families: backend, platform, cloud, DevOps, SRE, integration, data, quality, or software engineering
- Preferred industry: healthcare, healthtech, regulated SaaS, remote SaaS, enterprise software, or consulting
- Direct hire vs contract / consulting / staff / advisory
- Stability vs growth vs lifestyle optimization vs international flexibility

### 3. Work arrangement
- Remote, hybrid, or onsite preference
- Current location and desired future location
- Relocation openness
- International or expat-friendly path
- Work authorization or visa constraints
- Time-zone and async collaboration preferences

### 4. Financial and lifestyle constraints
- Salary floor
- Salary target
- Debt or financial obligations
- Minimum stability needed in a role
- Tolerance for lower pay in exchange for remote work, better team fit, or better geography
- Willingness to accept a shorter-term contract or only durable full-time roles

### 5. Company and role filters
- Prefer direct employers over vendors, agencies, or MSPs
- Company size and maturity preferences
- Product company vs platform company vs enterprise / consulting preference
- Industries or company types to avoid
- Job titles to prioritize
- Job keywords to prioritize and reject

### 6. Deal-breakers
- No agency or staffing roles
- No low-signal generic roles
- No roles without clear employer or domain relevance
- No role below a minimum compensation threshold
- No role that is too far from the core technical lane

## Example answers

- I want direct-hire backend or platform roles in healthcare or remote SaaS.
- I prefer remote-first, but am open to hybrid in the US or international remote if the role is durable and well-compensated.
- I want a salary floor of X and a target of Y.
- I am not interested in staffing, MSP, or vendor-wrapper roles.
- I want product or platform engineering with clean engineering maturity and durable team structure.

## How the system uses it

The intake should feed:
- lane choice for target-company refresh
- the filter rules used by the live job screen
- role-fit scoring thresholds
- company shortlist ranking
- application prioritization and quality bar

This is the working input layer that turns the repo from ad hoc job searching into a structured decision system.
