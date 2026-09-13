import csv
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from src.war_on_jobs.process_logging import log_event

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
TARGET_DIR = DATA_DIR / "targets"
BACKUP_ROOT = DATA_DIR / "backups"
RAW_SOURCE = DATA_DIR / "raw" / "live_jobs.csv"
JOB_TRACKER_FALLBACK = DATA_DIR / "workflow" / "job_target_tracker.csv"
SCREENED_DIR = DATA_DIR / "screened"

DEFAULT_ALLOWED_LOCATIONS = ["global", "remote", "europe", "uk", "us"]
DEFAULT_MINIMUM_FIT_SCORE = 2
DEFAULT_BAD_KEYWORDS = [
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
DEFAULT_GOOD_KEYWORDS = [
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
PROFILE_PATH = DATA_DIR / "workflow" / "career_profile_intake.yaml"


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
            "us",
            "united states",
            "usa",
            "remote",
            "anywhere",
            "new york",
            "san francisco",
            "boston",
            "chicago",
            "seattle",
            "los angeles",
            "denver",
            "atlanta",
            "austin",
            "miami",
            "portland",
            "washington",
            "phoenix",
            "minneapolis",
        ]
        if any(marker in text for marker in us_markers):
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
        if any(marker in text for marker in europe_markers):
            return True
    if "uk" in allowed:
        if "uk" in text or "united kingdom" in text or "london" in text:
            return True
    return False


def load_profile(profile_path: Path | str | None = None):
    path = Path(profile_path) if profile_path else PROFILE_PATH
    if yaml is None or not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return data if isinstance(data, dict) else {}


def merge_keyword_lists(*groups):
    values = []
    for group in groups:
        if not group:
            continue
        for item in group:
            if item is None:
                continue
            cleaned = str(item).strip().lower()
            if cleaned and cleaned not in values:
                values.append(cleaned)
    return values


def score_job(title, company, location, good_keywords=None, bad_keywords=None):
    text = normalize(f"{title} {company} {location}")
    good_keywords = good_keywords or DEFAULT_GOOD_KEYWORDS
    bad_keywords = bad_keywords or DEFAULT_BAD_KEYWORDS
    score = 0
    for keyword in good_keywords:
        if keyword in text:
            score += 1
    if any(keyword in text for keyword in bad_keywords):
        score -= 4
    return score


def filter_live_rows(rows: Iterable[dict], profile_path: Path | str | None = None):
    profile = load_profile(profile_path)
    filters = profile.get("company_and_role_filters", {})
    location_section = profile.get("location", {})

    allowed_locations = location_section.get("preferred_locations") or DEFAULT_ALLOWED_LOCATIONS
    good_keywords = merge_keyword_lists(DEFAULT_GOOD_KEYWORDS, filters.get("keywords_to_prioritize"))
    bad_keywords = merge_keyword_lists(DEFAULT_BAD_KEYWORDS, filters.get("keywords_to_reject"))
    minimum_fit_score = filters.get("minimum_fit_score", DEFAULT_MINIMUM_FIT_SCORE)
    if minimum_fit_score is None:
        minimum_fit_score = DEFAULT_MINIMUM_FIT_SCORE

    kept = []
    rejected = []
    for row in rows:
        title = row.get("title", "")
        company = row.get("company", "")
        location = row.get("location", "")
        combined = normalize(f"{title} {company} {location}")

        if not company:
            rejected.append({"title": title, "company": company, "location": location, "fit_score": 0, "reject": True, "reason": "missing_company"})
            continue

        if any(keyword in combined for keyword in bad_keywords):
            rejected.append({"title": title, "company": company, "location": location, "fit_score": 0, "reject": True, "reason": "vendor_or_recruiter"})
            continue

        if not location_allowed(location, allowed_locations=allowed_locations):
            rejected.append({"title": title, "company": company, "location": location, "fit_score": 0, "reject": True, "reason": "blocked_location"})
            continue

        score = score_job(title, company, location, good_keywords=good_keywords, bad_keywords=bad_keywords)
        if score >= minimum_fit_score:
            kept.append({"title": title, "company": company, "location": location, "fit_score": score, "reject": False, "reason": ""})
        else:
            rejected.append({"title": title, "company": company, "location": location, "fit_score": score, "reject": True, "reason": "low_fit_score"})
    kept.sort(key=lambda row: row["fit_score"], reverse=True)
    return kept, rejected


def read_csv_rows(path: Path):
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def merge_unique_rows(existing_rows, new_rows, dedupe_key="company"):
    merged = {}
    for row in list(existing_rows) + list(new_rows):
        key = row.get(dedupe_key) or f"{row.get('title', '')}|{row.get('company', '')}|{row.get('location', '')}"
        if key not in merged:
            merged[key] = row
    return list(merged.values())


def write_csv_rows(path: Path, rows, append_mode: bool = False):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        if append_mode and path.exists():
            return
        path.write_text("", encoding="utf-8")
        return

    fieldnames = list(rows[0].keys())
    if append_mode and path.exists():
        existing_rows = read_csv_rows(path)
        rows = merge_unique_rows(existing_rows, rows)
        fieldnames = list(rows[0].keys()) if rows else fieldnames

    with path.open("w" if not append_mode else "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def backup_current_state(target_dir: Path = TARGET_DIR, backup_root: Path = BACKUP_ROOT) -> Path:
    if not target_dir.exists():
        raise FileNotFoundError(f"Target dir not found: {target_dir}")

    backup_root.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_dir = backup_root / f"backup_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=False)

    for name in ["targets", "workflow", "prompts", "raw", "screened"]:
        source = DATA_DIR / name
        destination = backup_dir / name
        if source.exists():
            shutil.copytree(source, destination)

    log_event("backup_created", path=str(backup_dir), note="timestamped backup created before live screening")
    return backup_dir


def find_live_source():
    candidates = [RAW_SOURCE, JOB_TRACKER_FALLBACK]
    for candidate in candidates:
        if candidate.exists():
            log_event("live_source_selected", source=str(candidate), note="live source chosen for screening")
            return candidate
    raise FileNotFoundError("No live source CSV found in data/raw or data/workflow.")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run the backup-aware live job filter.")
    parser.add_argument("--append", action="store_true", help="Append merged kept/rejected rows to the existing screened outputs instead of replacing them.")
    parser.add_argument("--profile", type=Path, default=PROFILE_PATH, help="Path to the YAML profile intake for keyword and location rules.")
    args = parser.parse_args()

    backup_dir = backup_current_state()
    source = find_live_source()
    rows = read_csv_rows(source)
    kept, rejected = filter_live_rows(rows, profile_path=args.profile)

    SCREENED_DIR.mkdir(parents=True, exist_ok=True)
    write_csv_rows(SCREENED_DIR / "live_jobs_kept.csv", kept, append_mode=args.append)
    write_csv_rows(SCREENED_DIR / "live_jobs_rejected.csv", rejected, append_mode=args.append)
    log_event("screen_write_complete", kept=len(kept), rejected=len(rejected), path=str(SCREENED_DIR), note="screened output files written")

    print(f"Backup created at: {backup_dir}")
    print(f"Source: {source}")
    print(f"kept={len(kept)} rejected={len(rejected)}")
    mode = "append" if args.append else "replace"
    print(f"mode={mode}")
    print("Outputs: data/screened/live_jobs_kept.csv and data/screened/live_jobs_rejected.csv")


if __name__ == "__main__":
    main()
