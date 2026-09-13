# Data directory

This directory is organized by workflow lifecycle rather than by a flat dump of files.

## Structure

- raw/
  - original scraped or imported job search data
  - examples: jobs, LinkedIn sample exports

- screened/
  - outputs from the filtering and rejection pipeline
  - examples: kept jobs, rejected jobs, filtered results

- targets/
  - target-company lists and shortlist artifacts
  - examples: active shortlist, target-company template, company seed lists

- workflow/
  - active tracking and application-state files
  - examples: role queue, apply queue, job-tracker state

- prompts/
  - reusable prompts and instructions for refreshing shortlists and job searches

## Active lanes

The current workflow intentionally separates target companies by lane:

- core healthcare lane
  - [targets/target_company_active_list.csv](targets/target_company_active_list.csv)
  - [prompts/refresh-target-company-list-prompt.md](prompts/refresh-target-company-list-prompt.md)

- global remote SaaS lane
  - [targets/company_targets.csv](targets/company_targets.csv)
  - [prompts/refresh-global-remote-saas-target-list-prompt.md](prompts/refresh-global-remote-saas-target-list-prompt.md)

- healthcare-adjacent lane
  - [targets/adjacent_lane_targets.csv](targets/adjacent_lane_targets.csv)
  - [prompts/refresh-healthcare-adjacent-target-list-prompt.md](prompts/refresh-healthcare-adjacent-target-list-prompt.md)

## Merge policy

When refreshing a target list, use append-and-update semantics:
- append new companies to the CSV
- update existing company rows in place if the company is already present
- do not overwrite the full CSV with a broad search dump
- keep each lane curated and intentionally small

## Working files

The current active workflow is:
- targets/target_company_active_list.csv
- targets/company_targets.csv
- targets/adjacent_lane_targets.csv
- workflow/role_queue.csv

Keep the data in this directory small and intentional. Only retain files that are useful for the current job-search cycle.
