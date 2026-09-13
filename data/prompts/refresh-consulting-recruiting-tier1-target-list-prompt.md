# Refresh Consulting / Recruiting Tier 1 Target List Prompt

Use this prompt to refresh the watchlist for first-tier consulting and recruiting companies. This is a secondary lane, not a primary direct-employer lane.

## Prompt

You are refreshing a watchlist for a software engineer focused on direct-employer fit, but also tracking a limited set of first-tier consulting and recruiting organizations as secondary opportunities.

Goal:
Build a narrow, high-signal watchlist for 1st-tier consulting and recruiting organizations that may lead to real technical work, healthcare transformation work, or product-adjacent platform roles.

This lane is intentionally lower-priority than the core direct-employer lanes and should not crowd out strong healthcare or product-company targets.

Output target file:
- Populate [data/targets/consulting_recruiting_tier1_targets.csv](../targets/consulting_recruiting_tier1_targets.csv) with the final watchlist.
- Append new companies to the CSV rather than replacing the entire file.
- If a company already exists, update that row in place instead of creating a duplicate.
- Keep the list curated and small; do not overwrite the file with a broad dump.

Output format:
company | website | category | priority | direct_employer | geography | remote_ok | notes

Rules:
1. Keep this lane secondary and explicit.
2. Include only first-tier consulting firms, large staffing/recruiting organizations, or enterprise transformation vendors that may still surface technical work.
3. Do not treat this as a direct-employer lane.
4. Prefer companies that may place engineers into healthcare, platform, cloud, devops, or product-adjacent roles.
5. Exclude low-quality staffing and generic agencies unless they are clearly linked to stronger technical work.
6. Keep the list tight and watchlist-oriented, not broad or noisy.
7. Rank by likelihood of influential technical hiring and platform fit.

Target categories:
- tier-1 consulting
- enterprise transformation
- healthcare consulting
- recruiting / staffing
- systems integration

Do not include:
- boutique agencies with low technical signal
- generic contract shops
- broad staffing firms with weak product relevance
- companies that are not operationally relevant to platform or healthcare engineering work

Return only the final watchlist, sorted by priority.
