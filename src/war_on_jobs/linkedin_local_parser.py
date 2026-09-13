import csv
import re
from pathlib import Path

from bs4 import BeautifulSoup

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
    return re.sub(r"\s+", " ", text).strip().lower()


def extract_jobs_from_html(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    jobs = []

    candidates = soup.select("li, article, .jobs-search-results__list-item, .job-card-container")
    if not candidates:
        candidates = soup.select("body *")

    for card in candidates:
        title = card.select_one("h3, .base-search-card__title, .job-card-container__title")
        company = card.select_one("h4, .base-search-card__subtitle, .job-card-container__company")
        location = card.select_one(
            ".job-search-card__location, .artdeco-entity-lockup__caption, .job-card-container__location"
        )

        if not title or not company:
            continue

        title_text = title.get_text(" ", strip=True)
        company_text = company.get_text(" ", strip=True)
        location_text = location.get_text(" ", strip=True) if location else ""
        combined = f"{title_text} {company_text} {location_text}".lower()

        bad = any(word in combined for word in BAD_KEYWORDS)
        if bad:
            continue

        score = 0
        for kw in GOOD_KEYWORDS:
            if kw in combined:
                score += 1

        jobs.append({
            "title": title_text,
            "company": company_text,
            "location": location_text,
            "fit_score": score,
        })

    jobs.sort(key=lambda j: j["fit_score"], reverse=True)
    return jobs


def write_csv(rows, out_path):
    fieldnames = ["title", "company", "location", "fit_score"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    html_path = Path("linkedin_page.html")
    if not html_path.exists():
        raise FileNotFoundError("Expected linkedin_page.html in the current directory.")

    html_text = html_path.read_text(encoding="utf-8", errors="ignore")
    jobs = extract_jobs_from_html(html_text)
    write_csv(jobs, "linkedin_filtered_jobs.csv")
    print(f"Found {len(jobs)} candidate jobs.")
    print("Saved to linkedin_filtered_jobs.csv")
