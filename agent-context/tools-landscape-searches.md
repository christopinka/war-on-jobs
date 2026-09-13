# Tools Landscape and GitHub Search Results

## Purpose
This file expands the earlier tools overview into a broader landscape of tools relevant to job-search automation, local AI workflows, and lightweight orchestration.

## Search strategy
The following searches were run against GitHub repositories to gather real project examples and tool names.

### Search 1: job search ai
Results:
- santifer/career-ops — local job-search automation tool
- MadsLorentzen/ai-job-search — AI-assisted job search workflow
- Paramchoudhary/ResumeSkills — resume-related skills matching
- Gsync/jobsync — job sync and tracking workflow
- proficientlyjobs/proficiently-claude-skills — Claude-based job-search skills / prompts

### Search 2: resume tailoring ai
Results:
- santifer/career-ops — combines job search and tailoring workflow
- MadsLorentzen/ai-job-search — AI-driven job search with resume relevance logic
- feder-cr/Jobs_Applier_AI_Agent_AIHawk — AI agent for applying to jobs
- varunr89/resume-tailoring-skill — resume tailoring support
- proficientlyjobs/proficiently-claude-skills — prompt/skill-based tailoring workflow

### Search 3: job scraper python
Results:
- feder-cr/Jobs_Applier_AI_Agent_AIHawk — scraping and applying workflow
- PaulMcInnis/JobFunnel — job aggregation funnel
- oxylabs/how-to-scrape-google-jobs — Google Jobs scraping example
- eatmoreduck/boss-zhipin-scraper — scraper example for a specific platform
- feder-cr/resume_render_from_job_description — resume rendering from job descriptions

### Search 4: local llm agent
Results:
- unslothai/unsloth — local model optimization and fine-tuning support
- Mintplex-Labs/anything-llm — local LLM application framework
- chatchat-space/Langchain-Chatchat — local chatbot / LLM app framework
- khoj-ai/khoj — local AI assistant / knowledge tool
- Fosowl/agenticSeek — agent-oriented local AI tooling

### Search 5: n8n workflow automation
Results:
- n8n-io/n8n — workflow automation platform
- enescingoz/awesome-n8n-templates — automation templates
- nanobrowser/nanobrowser — browser automation / workflow automation
- wassupjay/n8n-free-templates — workflow templates
- n8n-io/n8n-docs — documentation for workflow automation

### Search 6: browser automation python github
Results:
- MarketingPipeline/Python-Selenium-Action — Selenium-based browser automation examples
- Hackingzone/winpirate — browser automation / utility example (not directly relevant)
- theNareshofficial/WinClearCache — utility example, not directly relevant
- BakkappaN/Playwright-JavaScript-TypeScript-CSharp-Python-Framework — Playwright automation examples
- Shubh2-0/backend-utility-tools — utility tooling examples

## Themes that show up
- Job-search automation and application agents
- Resume tailoring and matching
- Scraping and job aggregation
- Local LLM and agent tooling
- Workflow automation platforms
- Browser automation for repetitive web tasks

## Practical categories
### Job-search and application tools
- career-ops
- ai-job-search
- jobsync
- AIHawk-style applicator tools
- resume-tailoring utilities

### Local AI and agent tools
- Ollama-based workflows
- Anything-LLM
- Langchain-Chatchat
- Khoj
- agenticSeek

### Automation and orchestration tools
- n8n
- Zapier / Make
- browser automation with Playwright or Selenium

## What this suggests
The landscape is broad but the useful middle ground is usually:
- a tracker or database
- a local or cloud automation layer
- a lightweight AI layer for summarizing, scoring, or tailoring
- a browser or workflow automation layer for repetitive tasks

## Recommended starter stack
A practical starting architecture looks like this:
- Lowest friction: Google Sheets or CSV + manual scoring + optional AI summaries
- Mid-level: Notion or Airtable + simple automations + reminders
- More technical: local Python + CSV/JSON + Ollama or another local LLM + n8n for orchestration

## Tool evaluation criteria
Use these criteria to score tools against the direction in the other documents and the workflow discussed here. Each criterion uses a 1–5 scale, where 1 is weak fit and 5 is strong fit.

- Relevance to core workflow (weight 25%): Does it help with tracking, scoring, summarizing, or follow-up?
- Low friction / time to value (weight 20%): Can it deliver value quickly without too much setup?
- Local or self-hosted friendliness (weight 15%): Does it work well locally or without depending heavily on external services?
- Automation potential (weight 15%): Can it support reminders, routing, syncs, or repetitive actions?
- AI usefulness (weight 15%): Does it help with fit assessment, summarization, tailoring, or extraction?
- Extensibility / future-proofing (weight 10%): Will it still be useful if the workflow becomes more technical later?
- Paid-platform value and cost efficiency (weight 10%): Is the paid tool worth the subscription cost relative to the value it delivers?

Weighted score formula:
- Total score = sum(score × weight)
- On a 100-point scale, this becomes easy to compare across tools.

### Sample scorecard for candidate tools
| Tool | Relevance | Low friction | Local/self-hosted | Automation | AI usefulness | Extensibility | Cost/value | Weighted total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Google Sheets / CSV | 4 | 5 | 2 | 3 | 2 | 4 | 5 | 3.6/5 |
| Notion / Airtable | 5 | 4 | 1 | 4 | 3 | 4 | 3 | 3.7/5 |
| n8n | 4 | 3 | 4 | 5 | 2 | 5 | 4 | 3.8/5 |
| Ollama + local LLM | 4 | 2 | 5 | 2 | 5 | 4 | 4 | 3.5/5 |
| Playwright / Selenium | 3 | 2 | 3 | 4 | 1 | 4 | 4 | 2.9/5 |
| Obsidian | 4 | 4 | 4 | 2 | 2 | 3 | 4 | 3.3/5 |
| Teal / LoopCV / similar paid tools | 5 | 3 | 1 | 3 | 3 | 3 | 2 | 3.2/5 |

### Practical interpretation
- Highest value for the current stage: Google Sheets or a simple CSV tracker, plus a lightweight AI layer later.
- Best for a slightly more structured workflow: Notion or Airtable.
- Best for automation once the process is stable: n8n.
- Best for private local AI experiments: Ollama plus a local model.
- Paid job-search platforms can be useful, but they generally score lower here unless they are clearly superior at application support or workflow convenience.

A simple workflow that fits the research is:
1. Collect target companies and roles into a tracker.
2. Save job description text and notes in one place.
3. Use a local or cloud AI tool to generate a short fit summary, a tailored bullet, or a follow-up question.
4. Use automation to remind you when a role needs follow-up or a resume tweak.

What to avoid at first:
- Overbuilding a full app before the workflow is proven
- Automating applications too early without a clear quality bar
- Using too many tools at once; one tracker and one automation path is enough to start
