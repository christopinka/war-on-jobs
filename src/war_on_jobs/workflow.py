from __future__ import annotations

import csv
from pathlib import Path

from src.war_on_jobs.live_daily_search import (
    SCREENED_DIR,
    backup_current_state,
    filter_live_rows,
    find_live_source,
    read_csv_rows,
    write_csv_rows,
)
from src.war_on_jobs.process_logging import log_event
from src.war_on_jobs.target_lane_refresh import ORDER_FILE, load_order, refresh_targets

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_DIR = ROOT / "data" / "workflow"
BACKUP_ROOT = ROOT / "data" / "backups"
ROLE_QUEUE_PATH = WORKFLOW_DIR / "role_queue.csv"
TOP_ROLES_PATH = WORKFLOW_DIR / "top_roles_output.csv"
COMPANY_SITE_URLS_PATH = WORKFLOW_DIR / "company_site_urls.csv"


def _lane_for_company(company: str) -> str:
    company_key = (company or "").strip().lower()
    if company_key in {"gitlab", "datadog", "cloudflare", "hashicorp", "atlassian", "snyk"}:
        return "global_remote_saas"
    if company_key in {"deloitte", "accenture", "pwc", "ey", "slalom", "capgemini"}:
        return "consulting_recruiting"
    return "healthcare_core"


def populate_role_queue_from_company_sites(
    source_path: Path | str = COMPANY_SITE_URLS_PATH,
    target_path: Path | str = ROLE_QUEUE_PATH,
) -> list[dict[str, str]]:
    source = Path(source_path)
    target = Path(target_path)

    if not source.exists():
        log_event("role_queue_missing_company_source", path=str(source), note="company site CSV input was not found")
        return []

    with source.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    queue_rows: list[dict[str, str]] = []
    for row in rows:
        company = (row.get("company") or "").strip()
        careers_url = (row.get("careers_url") or "").strip()
        if not company or not careers_url:
            continue

        queue_rows.append(
            {
                "company": company,
                "website": row.get("company_url") or row.get("careers_url") or "",
                "job_title": "Target role pending review",
                "location": "Targeted by company lane",
                "role_type": "platform / backend / infrastructure",
                "fit_score": "85",
                "status": "new",
                "priority": "high" if company.lower() not in {"deloitte", "accenture", "pwc", "ey"} else "medium",
                "source": "company_site_urls",
                "notes": f"Approved company site discovered from company list; review {careers_url} for active roles.",
                "careers_url": careers_url,
            }
        )

    fieldnames = [
        "company",
        "website",
        "job_title",
        "location",
        "role_type",
        "fit_score",
        "status",
        "priority",
        "source",
        "notes",
        "careers_url",
    ]

    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(queue_rows)

    log_event("role_queue_written", path=str(target), rows=len(queue_rows), note="company list populated into a working role queue")
    return queue_rows


def build_top_roles_output(
    source_path: Path | str = ROLE_QUEUE_PATH,
    target_path: Path | str = TOP_ROLES_PATH,
    limit: int = 10,
) -> list[dict[str, str]]:
    source = Path(source_path)
    target = Path(target_path)

    if not source.exists():
        log_event("top_roles_missing_source", path=str(source), note="role queue input was not found")
        return []

    with source.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    lane_targets = {
        "healthcare_core": 5,
        "global_remote_saas": 3,
        "consulting_recruiting": 2,
    }

    lane_rankings = {lane: [] for lane in lane_targets}
    for row in rows:
        lane = _lane_for_company(row.get("company", ""))
        if lane in lane_rankings:
            lane_rankings[lane].append(row)

    for lane in lane_rankings:
        lane_rankings[lane].sort(key=lambda row: int(row.get("fit_score", "0") or 0), reverse=True)

    selected: list[dict[str, str]] = []
    for lane, lane_target in lane_targets.items():
        selected.extend(lane_rankings.get(lane, [])[:lane_target])

    remaining_slots = max(0, limit - len(selected))
    if remaining_slots > 0:
        all_rows = sorted(rows, key=lambda row: int(row.get("fit_score", "0") or 0), reverse=True)
        for row in all_rows:
            if row in selected:
                continue
            if len(selected) >= limit:
                break
            selected.append(row)

    if not selected:
        log_event("top_roles_empty", path=str(target), note="no ranked rows available for top roles output")
        return []

    selected = selected[:limit]

    fieldnames = [
        "company",
        "website",
        "job_title",
        "location",
        "role_type",
        "fit_score",
        "status",
        "priority",
        "source",
        "notes",
    ]

    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        backup_root = target.parent / "backups"
        backup_root.mkdir(parents=True, exist_ok=True)
        timestamp = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup_path = backup_root / f"top_roles_output_{timestamp}.csv"
        backup_path.write_bytes(target.read_bytes())

    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(selected)

    log_event("top_roles_written", path=str(target), rows=len(selected), limit=limit, note="top roles output generated with explicit lane quotas")
    return selected


def run_full_workflow() -> dict:
    print("PHASE 1: refreshing target lanes")
    log_event("workflow_phase_started", phase="refresh_targets", note="refreshing target lanes")
    rows = load_order(ORDER_FILE)
    refresh_targets(rows)
    log_event("workflow_phase_completed", phase="refresh_targets", note="target lane refresh finished")
    print("PHASE 1 complete: target lane refresh finished")

    print("PHASE 2: building top roles output from the active role queue")
    log_event("workflow_phase_started", phase="top_roles", note="building top roles output from the active role queue")
    top_roles = build_top_roles_output()
    print(f"Top roles output: {len(top_roles)} rows")
    log_event("workflow_phase_completed", phase="top_roles", rows=len(top_roles), note="top roles output generated")
    print("PHASE 2 complete: top roles output generated")

    print("PHASE 3: backing up current working state and screening live rows")
    log_event("workflow_phase_started", phase="live_screen", note="backing up current working state and screening live rows")
    backup_dir = backup_current_state()
    source = find_live_source()
    input_rows = read_csv_rows(source)
    kept, rejected = filter_live_rows(input_rows)

    SCREENED_DIR.mkdir(parents=True, exist_ok=True)
    write_csv_rows(SCREENED_DIR / "live_jobs_kept.csv", kept, append_mode=False)
    write_csv_rows(SCREENED_DIR / "live_jobs_rejected.csv", rejected, append_mode=False)

    log_event("backup_created", path=str(backup_dir), source=str(source), kept=len(kept), rejected=len(rejected))
    log_event("screen_results_written", kept=len(kept), rejected=len(rejected), path=str(SCREENED_DIR))
    print(f"Backup created at: {backup_dir}")
    print(f"Source: {source}")
    print(f"kept={len(kept)} rejected={len(rejected)}")
    print("PHASE 3 complete: backup + live screening finished")
    log_event("workflow_phase_completed", phase="live_screen", kept=len(kept), rejected=len(rejected), note="backup + live screening finished")
    return {"backup_dir": str(backup_dir), "kept": len(kept), "rejected": len(rejected), "top_roles": len(top_roles)}
