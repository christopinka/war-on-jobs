# War on Jobs

A small Python-based workflow for screening job leads, filtering recruiter/vendor noise, and focusing on a narrow direct-employer target lane.

## Project goal

This repo is designed around a specific operating model:

- keep the search lane narrow
- favor direct employers over recruiters and staffing firms
- track only relevant roles and locations
- score candidates locally with a simple rule-based filter
- keep outputs in CSV format for easy review and iteration

## Repository layout

- `src/war_on_jobs/` — Python package for screening logic
- `tests/` — regression tests
- `data/` — raw inputs and generated outputs
- `docs/` — strategy notes, research, and written planning
- `README.md` — repo overview

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m unittest -q
```

## Core flow

1. Maintain a tracker CSV with candidate role rows.
2. Run the screening script.
3. Review kept and rejected outputs.
4. Create a narrow apply queue from direct-employer matches.

## Operational guidance

This repo intentionally avoids broad LinkedIn scraping as the primary workflow. The job search system is deliberately narrow, local, and high-signal.

For the current lane, the target is:
- healthcare platform / cloud / infrastructure roles
- direct employers only
- remote-friendly or acceptable geography
- low recruiter/vendor noise

## Notes

The markdown files in the repo are strategic context and planning documents rather than runtime code. They belong in `docs/` or under a notes folder, not at the repo root.
