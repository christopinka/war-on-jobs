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
    "sql",
    "healthcare",
    "saas",
    "platform",
    "engineer",
    "software",
]


def normalize(text):
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip().lower()


def location_allowed(row, allowed_locations=None):
    allowed = set((allowed_locations or DEFAULT_ALLOWED_LOCATIONS))
    location = normalize(row.get('location', ''))

    if not location or location in {"remote", "anywhere", "global"}:
        return True

    if "global" in allowed or "all" in allowed:
        return True

    if "us" in allowed:
        us_markers = ["us", "united states", "usa", "new york", "san francisco", "boston", "remote", "anywhere"]
        if any(marker in location for marker in us_markers):
            return True

    if "europe" in allowed:
        europe_markers = [
            "albania",
            "andorra",
            "austria",
            "belgium",
            "bosnia",
            "bulgaria",
            "croatia",
            "cyprus",
            "czech",
            "denmark",
            "estonia",
            "finland",
            "france",
            "germany",
            "greece",
            "hungary",
            "iceland",
            "ireland",
            "italy",
            "latvia",
            "liechtenstein",
            "lithuania",
            "luxembourg",
            "malta",
            "monaco",
            "netherlands",
            "norway",
            "poland",
            "portugal",
            "romania",
            "san marino",
            "slovakia",
            "slovenia",
            "spain",
            "sweden",
            "switzerland",
            "uk",
            "united kingdom",
            "london",
            "paris",
            "berlin",
            "amsterdam",
            "madrid",
            "lisbon",
            "rome",
            "stockholm",
            "remote",
            "anywhere",
        ]
        if any(marker in location for marker in europe_markers):
            return True

    if "uk" in allowed:
        if "uk" in location or "united kingdom" in location or "london" in location:
            return True

    if "remote" in allowed:
        if "remote" in location or "anywhere" in location:
            return True

    return False


def get_match_summary(row):
    text = normalize(
        f"{row.get('title', '')} {row.get('company', '')} {row.get('description', '')} {row.get('location', '')}"
    )
    good_hits = [kw for kw in GOOD_KEYWORDS if kw in text]
    bad_hits = [kw for kw in BAD_KEYWORDS if kw in text]
    return good_hits, bad_hits


def score_role(row):
    score = 0
    good_hits, bad_hits = get_match_summary(row)

    for kw in good_hits:
        score += 1

    for kw in bad_hits:
        score -= 2

    if not row.get('company') or len(normalize(row.get('company'))) < 2:
        score -= 3

    return score, good_hits, bad_hits


def should_reject(row, allowed_locations=None):
    text = normalize(
        f"{row.get('title', '')} {row.get('company', '')} {row.get('description', '')}"
    )
    if any(kw in text for kw in BAD_KEYWORDS):
        return True, "keyword_match"
    if not row.get('company') or len(normalize(row.get('company'))) < 2:
        return True, "missing_company"
    if not location_allowed(row, allowed_locations=allowed_locations):
        return True, "location_blocked"
    return False, "keep"


def process_rows(rows, allowed_locations=None):
    kept = []
    rejected = []

    for row in rows:
        score, good_hits, bad_hits = score_role(row)
        row['fit_score'] = score
        row['good_matches'] = ", ".join(good_hits) if good_hits else ""
        row['bad_matches'] = ", ".join(bad_hits) if bad_hits else ""

        reject, reason = should_reject(row, allowed_locations=allowed_locations)
        if reject:
            row['reason'] = reason
            rejected.append({**row, "reason": reason})
        else:
            row['reason'] = ""
            kept.append(row)

    kept.sort(key=lambda r: r.get('fit_score', 0), reverse=True)
    return kept, rejected


def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    if not rows:
        open(path, 'w').close()
        return
    fieldnames = list(rows[0].keys())
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == '__main__':
    source = Path('jobs.csv')
    if not source.exists():
        raise FileNotFoundError("Expected jobs.csv in the current directory.")

    rows = read_csv(source)
    allowed_locations = ["global", "remote", "europe", "uk", "us"]
    kept, rejected = process_rows(rows, allowed_locations=allowed_locations)

    write_csv('filtered_jobs.csv', kept)
    write_csv('rejected_jobs.csv', rejected)

    print(f"kept={len(kept)} rejected={len(rejected)}")
    print("Outputs: filtered_jobs.csv and rejected_jobs.csv")
    print(f"allowed_locations={allowed_locations}")
