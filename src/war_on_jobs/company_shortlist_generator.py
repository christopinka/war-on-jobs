import csv
from pathlib import Path

SRC = Path('company_targets.csv')
OUT = Path('company_shortlist_output.csv')


def load_rows():
    with SRC.open(newline='') as f:
        return list(csv.DictReader(f))


def is_relevant(row):
    company = (row.get('company') or '').lower()
    category = (row.get('category') or '').lower()
    priority = (row.get('priority') or '').lower()
    notes = (row.get('notes') or '').lower()

    if priority not in {'high', 'medium'}:
        return False

    keywords = [
        'healthcare', 'health', 'platform', 'cloud', 'devops',
        'infrastructure', 'saas', 'regulated', 'integration', 'clinical'
    ]
    if any(k in category for k in keywords) or any(k in notes for k in keywords):
        return True

    if any(
        k in company
        for k in [
            "ust",
            "veterans",
            "tebra",
            "equipment",
            "misoftech",
            "intuitive",
            "snapsheet",
            "jobot",
            "respondus",
            "thatdot",
            "haystack",
        ]
    ):
        return True

    return False


def main():
    rows = load_rows()
    kept = [r for r in rows if is_relevant(r)]

    with OUT.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['company', 'website', 'priority', 'category', 'notes'])
        writer.writeheader()
        writer.writerows(kept)

    print(f'company_count={len(kept)}')
    for r in kept:
        print(f"{r['company']} | {r['priority']} | {r['category']}")


if __name__ == '__main__':
    main()
