from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOG_DIR = ROOT / "data" / "logs"


def ensure_log_dir(path: str | Path | None = None) -> Path:
    target = Path(path) if path is not None else DEFAULT_LOG_DIR
    target.mkdir(parents=True, exist_ok=True)
    return target


def log_event(
    status: str,
    *,
    company: str | None = None,
    domain: str | None = None,
    url: str | None = None,
    note: str | None = None,
    path: str | Path | None = None,
    **extra: Any,
) -> Path:
    log_dir = ensure_log_dir(path.parent if path is not None and isinstance(path, Path) else DEFAULT_LOG_DIR)
    log_path = Path(path) if path is not None else log_dir / "workflow_log.jsonl"

    if log_path.suffix == "":
        log_path = log_path.with_suffix(".jsonl")

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "company": company,
        "domain": domain,
        "url": url,
        "note": note,
        **extra,
    }

    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")

    print(json.dumps(record, sort_keys=True))
    return log_path


if __name__ == "__main__":
    log_event("ok", company="Epic", domain="epic.com", note="sample log entry")
