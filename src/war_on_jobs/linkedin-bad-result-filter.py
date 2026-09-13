# Minimal LinkedIn job filter prototype
# Purpose: reject noisy, recruiter-heavy, and weak-fit jobs from a linked CSV or JSON list.

import csv
import re
from pathlib import Path

BAD_KEYWORDS = [
    "recruiter",
    "agency",
    "staffing",
    "msp",
    "vms",
    "vendor",
    "c2c",
    "consulting",
    "contract",
    "offshore",
    "our client",
    "resource",
    "bench",
    "staff augmentation",
    "talent acquisition",
]

GOOD_KEYWORDS = [
    "python",
    "aws",
    "kubernetes",
    "sql",
    "healthcare",
    "saas",
    "platform",
    "engineer",
    "software",
]

def normalize(text):
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.lower()).strip()


def score_role(title, company, description):
    text = normalize(f"{title} {company} {description}")
    score = 0

    for kw in GOOD_KEYWORDS:
        if kw in text:
            score += 1

    for kw in BAD_KEYWORDS:
        if kw in text:
            score -= 2

    # Mild penalty for vague employer names / generic wording
    if not company or len(company.strip()) < 2:
        score -= 3
    if "hiring now" in text and "direct" not in text:
        score -= 1

    return score


def is_reject(title, company, description):
    text = normalize(f"{title} {company} {description}")

    # Hard reject patterns
    if any(kw in text for kw in BAD_KEYWORDS):
        return True
    if not company or len(company.strip()) < 2:
        return True
    if "recruiter" in text and "direct hire" not in text:
        return True

    return False


def process_rows(rows):
    kept = []
    rejected = []

    for row in rows:
        title = row.get("title", "")
        company = row.get("company", "")
        description = row.get("description", "")

        if is_reject(title, company, description):
            rejected.append({**row, "reason": "rejected"})
            continue

        fit = score_role(title, company, description)
        row["fit_score"] = fit
        kept.append(row)

    kept.sort(key=lambda r: r.get("fit_score", 0), reverse=True)
    return kept, rejected


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    fieldnames = list(rows[0].keys()) if rows else []
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    source = Path("jobs.csv")
    if not source.exists():
        raise FileNotFoundError("Expected jobs.csv in the current directory.")

    rows = read_csv(source)
    kept, rejected = process_rows(rows)

    write_csv("filtered_jobs.csv", kept)
    write_csv("rejected_jobs.csv", rejected)
    print(f"Kept {len(kept)} jobs; rejected {len(rejected)} jobs.")
    print("Files created: filtered_jobs.csv and rejected_jobs.csv")
