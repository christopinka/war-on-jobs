# War on Jobs

A complete local system for narrowing the healthcare-tech job search, screening away recruiter and vendor noise, and turning a small target-company list into a disciplined role queue and application pipeline.

## Project goal

This repo is designed around a specific operating model:

- keep the search lane narrow and high-signal
- favor direct employers over recruiters and staffing firms
- define a targeted employer list for healthcare technology
- convert that list into a role queue and application workflow
- score job opportunities locally with a simple rule-based filter
- keep outputs in CSV format for easy review, iteration, and backup

## Repository layout

- `src/war_on_jobs/` — Python package for screening logic
- `tests/` — regression tests
- `data/` — organized workflow data by lifecycle: raw, screened, targets, workflow, prompts
- `docs/` — design and strategic planning documents
- `README.md` — repo overview

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m unittest -q
```

## Core flow

1. Generate or refresh a narrow target-company shortlist.
2. Convert the shortlist into a role queue.
3. Pull in raw job records or search results.
4. Run the screening script to reject recruiter/vendor noise.
5. Review kept and rejected outputs.
6. Prioritize and apply only to the strongest direct-employer matches.

## Operational guidance

This repo intentionally avoids broad LinkedIn scraping as the primary workflow. The job search system is deliberately narrow, local, and high-signal.

For the current lane, the target is:
- healthcare platform / cloud / infrastructure roles
- direct employers only
- remote-friendly or acceptable geography
- low recruiter/vendor noise
- a small, disciplined application queue rather than a noisy funnel

## Notes

The markdown files in the repo are strategic context and planning documents rather than runtime code. They belong in `docs/` or under a notes folder, not at the repo root.
