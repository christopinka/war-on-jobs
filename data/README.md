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

## Working files

The current active workflow is:
- targets/target_company_active_list.csv
- workflow/role_queue.csv
- prompts/refresh-target-company-list-prompt.md

Keep the data in this directory small and intentional. Only retain files that are useful for the current job-search cycle.
