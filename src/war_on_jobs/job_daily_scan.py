import csv
import re
from pathlib import Path

DEFAULT_ALLOWED_LOCATIONS = ["global", "remote", "europe", "uk", "us"]
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
    "terraform",
    "sql",
    "healthcare",
    "saas",
    "platform",
    "backend",
    "integration",
    "engineer",
    "software",
]


def normalize(text):
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip().lower()


def location_allowed(location, allowed_locations=None):
    allowed = set((allowed_locations or DEFAULT_ALLOWED_LOCATIONS))
    text = normalize(location)

    if not text or text in {"remote", "anywhere", "global"}:
        return True

    if "global" in allowed or "all" in allowed:
        return True

    if "us" in allowed:
        us_markers = [
            "us", "united states", "usa", "remote", "anywhere", "new york", "san francisco",
            "boston", "chicago", "seattle", "los angeles", "denver", "atlanta", "austin",
            "miami", "portland", "washington", "phoenix", "minneapolis"
        ]
        if any(marker in text for marker in us_markers):
            return True

    if "europe" in allowed:
        europe_markers = [
            "albania", "andorra", "austria", "belgium", "bosnia", "bulgaria", "croatia", "cyprus",
            "czech", "denmark", "estonia", "finland", "france", "germany", "greece", "hungary",
            "iceland", "ireland", "italy", "latvia", "liechtenstein", "lithuania", "luxembourg",
            "malta", "monaco", "netherlands", "norway", "poland", "portugal", "romania", "san marino",
            "slovakia", "slovenia", "spain", "sweden", "switzerland", "uk", "united kingdom",
            "london", "paris", "berlin", "amsterdam", "madrid", "lisbon", "rome", "stockholm",
            "remote", "anywhere"
        ]
        if any(marker in text for marker in europe_markers):
            return True

    if "uk" in allowed:
        if "uk" in text or "united kingdom" in text or "london" in text:
            return True

    return False


def should_reject(title, company, location, allowed_locations=None):
    title_text = normalize(title)
    company_text = normalize(company)
    location_text = normalize(location)
    candidate = f"{title_text} {company_text} {location_text}"

    if any(keyword in candidate for keyword in BAD_KEYWORDS):
        return True
    if not company_text:
        return True
    if not location_allowed(location_text, allowed_locations=allowed_locations):
        return True
    return False


def score_job(title, company, location):
    text = normalize(f"{title} {company} {location}")
    score = 0
    for kw in GOOD_KEYWORDS:
        if kw in text:
            score += 1
    if any(keyword in text for keyword in BAD_KEYWORDS):
        score -= 4
    return score


def parse_job_rows(rows):
    out = []
    for row in rows:
        title = row.get("title", "")
        company = row.get("company", "")
        location = row.get("location", "")
        score = score_job(title, company, location)
        reject = should_reject(title, company, location, allowed_locations=DEFAULT_ALLOWED_LOCATIONS)
        out.append({
            "title": title,
            "company": company,
            "location": location,
            "fit_score": score,
            "reject": reject,
            "reason": "vendor_or_blocked_location" if reject else "",
        })
    return out


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    if not rows:
        Path(path).write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    source = Path("job_target_tracker.csv")
    if not source.exists():
        raise FileNotFoundError("Expected job_target_tracker.csv in the current directory.")

    rows = read_csv(source)
    processed = parse_job_rows(rows)
    kept = [r for r in processed if not r["reject"]]
    rejected = [r for r in processed if r["reject"]]
    kept.sort(key=lambda r: r["fit_score"], reverse=True)

    write_csv("daily_jobs_kept.csv", kept)
    write_csv("daily_jobs_rejected.csv", rejected)
    print(f"kept={len(kept)} rejected={len(rejected)}")
    print("Outputs: daily_jobs_kept.csv and daily_jobs_rejected.csv")


if __name__ == "__main__":
    main()
