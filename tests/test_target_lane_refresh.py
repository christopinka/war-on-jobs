import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from war_on_jobs.target_lane_refresh import merge_rows, load_order, ORDER_FILE


class TargetLaneRefreshTests(unittest.TestCase):
    def test_load_order_has_expected_lane_sequence(self):
        rows = load_order(ORDER_FILE)
        self.assertEqual([row["lane"] for row in rows], [
            "core_healthcare",
            "global_remote_saas",
            "healthcare_adjacent",
        ])

    def test_merge_rows_appends_new_and_updates_existing(self):
        existing = [
            {"company": "Epic", "priority": "high", "category": "healthcare"},
            {"company": "GitLab", "priority": "medium", "category": "saas"},
        ]
        new_rows = [
            {"company": "GitLab", "priority": "high", "category": "devops saas"},
            {"company": "Datadog", "priority": "high", "category": "observability"},
        ]

        merged = merge_rows(existing, new_rows)

        self.assertEqual(len(merged), 3)
        self.assertEqual(merged[0]["company"], "Epic")
        self.assertEqual(merged[1]["company"], "GitLab")
        self.assertEqual(merged[1]["priority"], "high")
        self.assertEqual(merged[2]["company"], "Datadog")


if __name__ == "__main__":
    unittest.main()
