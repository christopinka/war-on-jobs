# Contact Sourcing Prompt

Use this prompt to turn a high-signal role into a narrow set of direct hiring contacts or LinkedIn leads.

## Prompt

You are sourcing hiring contacts for a high-fit role at a direct-employer company.

Goal:
Identify a small set of likely hiring contacts who are relevant to the role and the team, without broad boilerplate outreach.

This is not a generic networking prompt. The output should be focused on the role and company already in the queue.

Output target file:
- Populate [data/workflow/contacts.csv](../workflow/contacts.csv) with the contact list.
- Append new rows rather than replacing the full file.
- If a contact already exists, update that row in place.
- Keep the list small and role-focused.

Output format:
company | contact_name | title | linkedin_url | email | role_title | source | notes

Rules:
1. Only include relevant hiring managers, recruiters, or engineers associated with the target role.
2. Prioritize direct-employer companies and real hiring contacts over broad networking noise.
3. Use LinkedIn company pages, the recruiting team page, or the team page to source small, credible leads.
4. Exclude generic recruiting aliases, spammy contacts, and broad vendor emails unless they are specifically tied to the role.
5. Keep only the strongest, most relevant leads.
6. Do not add random people who are not tied to the role.

Target contacts:
- hiring manager
- engineering manager
- recruiter for the team
- staff engineer or technical leader in the relevant domain

Do not include:
- generic careers inboxes unless they are the only route
- broad recruiting aliases without context
- network spam or random outreach lists
- contacts unrelated to the company or role

Return only the final contact list, sorted by relevance to the role.

## Practical use
Use this prompt after a role has already passed the queue review process. It should be used to capture only the high-priority leads for direct outreach.
