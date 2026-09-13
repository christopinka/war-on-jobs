#!/usr/bin/env python3
"""Single-entry workflow for the ordered target-company refresh sequence."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_DIR = ROOT / "data" / "workflow"
ORDER_FILE = WORKFLOW_DIR / "lane_refresh_order.csv"

LANE_PAYLOADS = {
    "core_healthcare": [
        {
            "company": "Epic",
            "website": "https://www.epic.com",
            "category": "provider workflow / EHR adjacent",
            "priority": "high",
            "direct_employer": "yes",
            "geography": "us",
            "remote_ok": "maybe",
            "notes": "Strong direct-employer fit; healthcare product and engineering platform relevance is very high.",
        },
        {
            "company": "athenahealth",
            "website": "https://www.athenahealth.com",
            "category": "healthcare SaaS",
            "priority": "high",
            "direct_employer": "yes",
            "geography": "us",
            "remote_ok": "maybe",
            "notes": "Strong product and platform fit for healthcare workflow and billing systems.",
        },
        {
            "company": "Oracle Health",
            "website": "https://www.oracle.com/health/",
            "category": "EHR / healthcare platform",
            "priority": "high",
            "direct_employer": "yes",
            "geography": "us",
            "remote_ok": "maybe",
            "notes": "Large healthcare platform employer with strong cloud and integration work.",
        },
        {
            "company": "Change Healthcare",
            "website": "https://www.changehealthcare.com",
            "category": "claims / revenue cycle",
            "priority": "high",
            "direct_employer": "yes",
            "geography": "us",
            "remote_ok": "maybe",
            "notes": "Claims, billing, and operational healthcare software with technical integration fit.",
        },
        {
            "company": "Veeva",
            "website": "https://www.veeva.com",
            "category": "regulated SaaS / life sciences",
            "priority": "high",
            "direct_employer": "yes",
            "geography": "us",
            "remote_ok": "maybe",
            "notes": "Excellent fit for regulated SaaS and data-heavy product infrastructure.",
        },
        {
            "company": "Surescripts",
            "website": "https://surescripts.com",
            "category": "interoperability / e-prescribing",
            "priority": "medium",
            "direct_employer": "yes",
            "geography": "us",
            "remote_ok": "maybe",
            "notes": "Excellent API and interoperability work in healthcare data exchange.",
        },
    ],
    "global_remote_saas": [
        {
            "company": "GitLab",
            "website": "https://about.gitlab.com",
            "category": "devops / platform SaaS",
            "priority": "high",
            "direct_employer": "yes",
            "geography": "global",
            "remote_ok": "yes",
            "notes": "Strong remote-first engineering culture with devops and platform work.",
        },
        {
            "company": "Datadog",
            "website": "https://www.datadoghq.com",
            "category": "observability / platform",
            "priority": "high",
            "direct_employer": "yes",
            "geography": "global",
            "remote_ok": "yes",
            "notes": "Very strong observability, cloud, and platform engineering match.",
        },
        {
            "company": "Cloudflare",
            "website": "https://www.cloudflare.com",
            "category": "infra / networking / platform",
            "priority": "high",
            "direct_employer": "yes",
            "geography": "global",
            "remote_ok": "yes",
            "notes": "Strong infrastructure and platform engineering fit for remote global roles.",
        },
        {
            "company": "HashiCorp",
            "website": "https://www.hashicorp.com",
            "category": "devops / infra",
            "priority": "medium",
            "direct_employer": "yes",
            "geography": "global",
            "remote_ok": "yes",
            "notes": "Excellent fit for infra automation, platform, and devops engineering.",
        },
        {
            "company": "Atlassian",
            "website": "https://www.atlassian.com",
            "category": "SaaS / devtools",
            "priority": "medium",
            "direct_employer": "yes",
            "geography": "global",
            "remote_ok": "yes",
            "notes": "Global product company with good developer tooling and platform culture.",
        },
        {
            "company": "Snyk",
            "website": "https://snyk.io",
            "category": "security / platform SaaS",
            "priority": "medium",
            "direct_employer": "yes",
            "geography": "global",
            "remote_ok": "yes",
            "notes": "Good fit for product company security and platform engineering work.",
        },
    ],
    "healthcare_adjacent": [
        {
            "company": "Teladoc Health",
            "website": "https://www.teladoc.com",
            "category": "digital health / telehealth",
            "priority": "high",
            "direct_employer": "yes",
            "geography": "us",
            "remote_ok": "maybe",
            "notes": "Strong digital health platform and product engineering fit.",
        },
        {
            "company": "Cedar",
            "website": "https://www.cedar.com",
            "category": "patient financing / revenue cycle",
            "priority": "high",
            "direct_employer": "yes",
            "geography": "us",
            "remote_ok": "maybe",
            "notes": "Healthcare operations and workflow product company with relevant platform work.",
        },
        {
            "company": "Phreesia",
            "website": "https://www.phreesia.com",
            "category": "patient intake / engagement",
            "priority": "high",
            "direct_employer": "yes",
            "geography": "us",
            "remote_ok": "maybe",
            "notes": "Healthcare workflow and patient experience software with technical product depth.",
        },
        {
            "company": "Aledade",
            "website": "https://www.aledade.com",
            "category": "value-based care / provider operations",
            "priority": "medium",
            "direct_employer": "yes",
            "geography": "us",
            "remote_ok": "maybe",
            "notes": "Healthcare operations and analytics software in a value-based care context.",
        },
        {
            "company": "Mend",
            "website": "https://www.mend.com",
            "category": "care navigation / patient support",
            "priority": "medium",
            "direct_employer": "yes",
            "geography": "us",
            "remote_ok": "maybe",
            "notes": "Digital health and care coordination software with product-focused engineering.",
        },
        {
            "company": "Arcadia",
            "website": "https://www.arcadia.io",
            "category": "health analytics / value-based care",
            "priority": "medium",
            "direct_employer": "yes",
            "geography": "us",
            "remote_ok": "maybe",
            "notes": "Healthcare analytics and provider performance software with platform and data work.",
        },
    ],
    "consulting_recruiting_tier1": [
        {
            "company": "Accenture",
            "website": "https://www.accenture.com",
            "category": "tier-1 consulting / systems integration",
            "priority": "medium",
            "direct_employer": "watch",
            "geography": "global",
            "remote_ok": "yes",
            "notes": "Useful as a consulting watch lane for enterprise software and healthcare transformation work; not a primary direct-employer target.",
        },
        {
            "company": "Deloitte",
            "website": "https://www.deloitte.com",
            "category": "tier-1 consulting / advisory",
            "priority": "medium",
            "direct_employer": "watch",
            "geography": "global",
            "remote_ok": "yes",
            "notes": "Strong consulting lane for enterprise and healthcare transformation; keep as a secondary watchlist only.",
        },
        {
            "company": "PwC",
            "website": "https://www.pwc.com",
            "category": "tier-1 consulting / digital transformation",
            "priority": "medium",
            "direct_employer": "watch",
            "geography": "global",
            "remote_ok": "yes",
            "notes": "Enterprise transformation lane; keep only when roles are clearly product or platform adjacent.",
        },
        {
            "company": "EY",
            "website": "https://www.ey.com",
            "category": "tier-1 consulting / advisory",
            "priority": "medium",
            "direct_employer": "watch",
            "geography": "global",
            "remote_ok": "yes",
            "notes": "Consulting watchlist for healthcare and transformation work; not a first-priority direct-employer target.",
        },
        {
            "company": "Slalom",
            "website": "https://www.slalom.com",
            "category": "tier-1 consulting / product engineering",
            "priority": "medium",
            "direct_employer": "watch",
            "geography": "us",
            "remote_ok": "yes",
            "notes": "Useful consulting lane with product and cloud work; watch for better fit than generic staffing roles.",
        },
        {
            "company": "Capgemini",
            "website": "https://www.capgemini.com",
            "category": "tier-1 consulting / systems integration",
            "priority": "medium",
            "direct_employer": "watch",
            "geography": "global",
            "remote_ok": "yes",
            "notes": "Consulting watchlist; useful only when the role is clearly technical and directly aligned to platform work.",
        },
        {
            "company": "TEKsystems",
            "website": "https://www.teksystems.com",
            "category": "recruiting / staffing",
            "priority": "low",
            "direct_employer": "watch",
            "geography": "us",
            "remote_ok": "yes",
            "notes": "Recruiting and staffing lane to capture middle-market placement work; not a direct-employer target.",
        },
        {
            "company": "Robert Half",
            "website": "https://www.roberthalf.com",
            "category": "recruiting / staffing",
            "priority": "low",
            "direct_employer": "watch",
            "geography": "us",
            "remote_ok": "yes",
            "notes": "Recruiting and staffing watchlist; useful only when a direct placement leads to a real technical role.",
        },
    ],
}


def load_order(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def merge_rows(existing_rows: list[dict[str, str]], new_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    merged = {row.get("company", ""): row for row in existing_rows if row.get("company")}

    for row in new_rows:
        company = row.get("company")
        if not company:
            continue
        if company in merged:
            merged[company].update(row)
        else:
            merged[company] = row

    return list(merged.values())


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def append_to_target(target_path: Path, new_rows: list[dict[str, str]]) -> None:
    existing_rows = load_csv_rows(target_path)
    merged = merge_rows(existing_rows, new_rows)

    fieldnames = []
    for row in merged:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)

    if not fieldnames:
        fieldnames = [
            "company",
            "website",
            "category",
            "priority",
            "direct_employer",
            "geography",
            "remote_ok",
            "notes",
        ]

    with target_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(merged)


def print_order(rows: list[dict[str, str]]) -> None:
    for row in rows:
        print(f"{row['step']}. {row['lane']}")
        print(f"   prompt: {row['prompt_file']}")
        print(f"   target: {row['target_csv']}")
        print(f"   trigger: {row['trigger_name']}")
        print()


def refresh_targets(rows: list[dict[str, str]]) -> None:
    for row in rows:
        target_path = ROOT / row["target_csv"]
        lane_name = row["lane"]
        print(f"Refreshing {lane_name} -> {target_path}")

        payload_rows = LANE_PAYLOADS.get(lane_name, [])
        if not payload_rows:
            print(f"No payload rows defined for {lane_name}")
            continue

        append_to_target(target_path, payload_rows)
        print(f"Updated {target_path} with {len(payload_rows)} rows")
        print()


def run_order(rows: list[dict[str, str]]) -> None:
    print("Target refresh workflow launch")
    print("=" * 32)
    print_order(rows)
    print("Use the above prompt order as the refresh sequence for the active target lanes.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Launch the ordered prompt refresh workflow for target-company targeting."
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Execute the ordered refresh workflow for the active target lanes.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Print the ordered lane refresh workflow.",
    )
    args = parser.parse_args()

    rows = load_order(ORDER_FILE)
    if args.run:
        refresh_targets(rows)
    elif args.list or not any((args.run, args.list)):
        run_order(rows)


if __name__ == "__main__":
    main()
