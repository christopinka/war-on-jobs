from __future__ import annotations

from pathlib import Path

from src.war_on_jobs.live_daily_search import (
    SCREENED_DIR,
    backup_current_state,
    filter_live_rows,
    find_live_source,
    read_csv_rows,
    write_csv_rows,
)
from src.war_on_jobs.target_lane_refresh import ORDER_FILE, load_order, refresh_targets

ROOT = Path(__file__).resolve().parents[2]


def run_full_workflow() -> dict:
    print("PHASE 1: refreshing target lanes")
    rows = load_order(ORDER_FILE)
    refresh_targets(rows)
    print("PHASE 1 complete: target lane refresh finished")

    print("PHASE 2: backing up current working state and screening live rows")
    backup_dir = backup_current_state()
    source = find_live_source()
    input_rows = read_csv_rows(source)
    kept, rejected = filter_live_rows(input_rows)

    SCREENED_DIR.mkdir(parents=True, exist_ok=True)
    write_csv_rows(SCREENED_DIR / "live_jobs_kept.csv", kept, append_mode=False)
    write_csv_rows(SCREENED_DIR / "live_jobs_rejected.csv", rejected, append_mode=False)

    print(f"Backup created at: {backup_dir}")
    print(f"Source: {source}")
    print(f"kept={len(kept)} rejected={len(rejected)}")
    print("PHASE 2 complete: backup + live screening finished")
    return {"backup_dir": str(backup_dir), "kept": len(kept), "rejected": len(rejected)}
