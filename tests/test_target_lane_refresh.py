import csv
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from war_on_jobs.target_lane_refresh import merge_rows, load_order, ORDER_FILE
from war_on_jobs.workflow import run_full_workflow


class TargetLaneRefreshTests(unittest.TestCase):
    def test_load_order_has_expected_lane_sequence(self):
        rows = load_order(ORDER_FILE)
        self.assertEqual([row["lane"] for row in rows], [
            "core_healthcare",
            "global_remote_saas",
            "healthcare_adjacent",
            "consulting_recruiting_tier1",
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

    @patch("war_on_jobs.workflow.refresh_targets")
    @patch("war_on_jobs.workflow.backup_current_state")
    @patch("war_on_jobs.workflow.find_live_source")
    @patch("war_on_jobs.workflow.read_csv_rows")
    @patch("war_on_jobs.workflow.filter_live_rows")
    @patch("war_on_jobs.workflow.write_csv_rows")
    def test_run_full_workflow_refreshes_lanes_and_filters_live_jobs(
        self,
        mock_write_csv_rows,
        mock_filter_live_rows,
        mock_read_csv_rows,
        mock_find_live_source,
        mock_backup_current_state,
        mock_refresh_targets,
    ):
        mock_read_csv_rows.return_value = [{"title": "Python Engineer", "company": "Epic", "location": "Remote US"}]
        mock_filter_live_rows.return_value = (
            [{"title": "Python Engineer", "company": "Epic", "location": "Remote US", "fit_score": 2, "reject": False, "reason": ""}],
            [],
        )

        result = run_full_workflow()

        self.assertEqual(result["kept"], 1)
        self.assertEqual(result["rejected"], 0)
        mock_refresh_targets.assert_called_once()
        mock_backup_current_state.assert_called_once()
        mock_write_csv_rows.assert_called()


if __name__ == "__main__":
    unittest.main()
