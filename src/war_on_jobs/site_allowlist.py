from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[2]
ALLOWLIST_PATH = ROOT / "data" / "site_allowlist.yaml"


def _parse_simple_yaml_allowlist(text: str) -> list[str]:
    items: list[str] = []
    in_allowed_sites = False

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if line == "allowed_sites:":
            in_allowed_sites = True
            continue

        if in_allowed_sites and line.startswith("-"):
            value = line[1:].strip()
            if value:
                items.append(value.strip().lower())
            continue

        if in_allowed_sites and line and not line.startswith("-"):
            in_allowed_sites = False

    return items


def load_site_allowlist(path: str | Path | None = None) -> list[str]:
    target = Path(path) if path is not None else ALLOWLIST_PATH
    if not target.exists():
        return []

    with target.open("r", encoding="utf-8") as handle:
        text = handle.read()

    if yaml is not None:
        try:
            data = yaml.safe_load(text) or {}
            if isinstance(data, dict):
                allowed = data.get("allowed_sites", [])
                if isinstance(allowed, list):
                    cleaned = []
                    for site in allowed:
                        if site is None:
                            continue
                        value = str(site).strip().lower()
                        if value and value not in cleaned:
                            cleaned.append(value)
                    return cleaned
        except Exception:
            pass

    cleaned = []
    for site in _parse_simple_yaml_allowlist(text):
        if site and site not in cleaned:
            cleaned.append(site)
    return cleaned


def is_allowed_site(url: str, allowlist: list[str] | None = None) -> bool:
    if not url:
        return False

    parsed = urlparse(url)
    host = (parsed.netloc or parsed.path or "").lower()
    if not host:
        return False

    host = host.replace("www.", "")
    candidates = {host}
    if host.startswith("careers."):
        candidates.add(host.replace("careers.", "", 1))
    if host.startswith("jobs."):
        candidates.add(host.replace("jobs.", "", 1))
    if host.startswith("www."):
        candidates.add(host.replace("www.", "", 1))

    configured = allowlist if allowlist is not None else load_site_allowlist()
    normalized = {str(item).strip().lower().replace("www.", "") for item in configured}
    return any(candidate in normalized for candidate in candidates)


if __name__ == "__main__":
    print(load_site_allowlist())
