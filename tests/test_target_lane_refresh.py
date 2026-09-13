import csv
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from war_on_jobs.target_lane_refresh import merge_rows, load_order, ORDER_FILE
from war_on_jobs.workflow import (
    build_top_roles_output,
    populate_role_queue_from_company_sites,
    run_full_workflow,
)


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

    def test_build_top_roles_output_writes_top_rows(self):
        source_path = Path(tempfile.mkdtemp()) / "role_queue.csv"
        target_path = Path(tempfile.mkdtemp()) / "top_roles_output.csv"
        with source_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["company", "website", "job_title", "location", "role_type", "fit_score", "status", "priority", "source", "notes"])
            writer.writerow(["Epic", "https://www.epic.com", "Senior Platform Engineer", "Remote - US", "platform", "95", "new", "high", "company_careers", "Strong fit"])
            writer.writerow(["GitLab", "https://about.gitlab.com", "Senior DevOps Engineer", "Remote - Global", "devops", "92", "new", "high", "company_careers", "Great remote fit"])
            writer.writerow(["Datadog", "https://www.datadoghq.com", "Cloud Engineer", "Remote - US", "cloud", "88", "new", "medium", "company_careers", "Strong product company"])

        rows = build_top_roles_output(source_path=source_path, target_path=target_path, limit=2)

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["company"], "Epic")
        self.assertTrue(target_path.exists())
        with target_path.open("r", encoding="utf-8") as handle:
            text = handle.read()
        self.assertIn("Epic", text)
        self.assertIn("GitLab", text)

    def test_build_top_roles_output_keeps_one_from_each_lane(self):
        source_path = Path(tempfile.mkdtemp()) / "role_queue.csv"
        target_path = Path(tempfile.mkdtemp()) / "top_roles_output.csv"
        with source_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["company", "website", "job_title", "location", "role_type", "fit_score", "status", "priority", "source", "notes"])
            writer.writerow(["Epic", "https://www.epic.com", "Senior Platform Engineer", "Remote - US", "platform", "95", "new", "high", "company_careers", "Strong fit"])
            writer.writerow(["GitLab", "https://about.gitlab.com", "Senior DevOps Engineer", "Remote - Global", "devops", "92", "new", "high", "company_careers", "Great remote fit"])
            writer.writerow(["Deloitte", "https://www.deloitte.com", "Senior Cloud Engineer", "Remote - US", "cloud", "90", "new", "medium", "company_careers", "Secondary watch lane"])

        rows = build_top_roles_output(source_path=source_path, target_path=target_path, limit=3)

        self.assertEqual(len(rows), 3)
        self.assertEqual({row["company"] for row in rows}, {"Epic", "GitLab", "Deloitte"})
        self.assertTrue(target_path.exists())

    def test_build_top_roles_output_uses_lane_quotas(self):
        source_path = Path(tempfile.mkdtemp()) / "role_queue.csv"
        target_path = Path(tempfile.mkdtemp()) / "top_roles_output.csv"
        with source_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["company", "website", "job_title", "location", "role_type", "fit_score", "status", "priority", "source", "notes"])
            writer.writerow(["Epic", "https://www.epic.com", "Senior Platform Engineer", "Remote - US", "platform", "98", "new", "high", "company_careers", "Strong fit"])
            writer.writerow(["athenahealth", "https://www.athenahealth.com", "Senior Backend Engineer", "Remote - US", "backend", "97", "new", "high", "company_careers", "Strong fit"])
            writer.writerow(["GitLab", "https://about.gitlab.com", "Senior DevOps Engineer", "Remote - Global", "devops", "96", "new", "high", "company_careers", "Great remote fit"])
            writer.writerow(["Datadog", "https://www.datadoghq.com", "Cloud Engineer", "Remote - US", "cloud", "95", "new", "high", "company_careers", "Strong fit"])
            writer.writerow(["Deloitte", "https://www.deloitte.com", "Senior Cloud Engineer", "Remote - US", "cloud", "94", "new", "medium", "company_careers", "Watch lane"])

        rows = build_top_roles_output(source_path=source_path, target_path=target_path, limit=5)

        lane_counts = {}
        for row in rows:
            lane = "healthcare_core" if row["company"].lower() not in {"gitlab", "datadog", "deloitte"} else ("global_remote_saas" if row["company"].lower() in {"gitlab", "datadog"} else "consulting_recruiting")
            lane_counts[lane] = lane_counts.get(lane, 0) + 1

        self.assertGreaterEqual(lane_counts.get("healthcare_core", 0), 2)
        self.assertGreaterEqual(lane_counts.get("global_remote_saas", 0), 1)
        self.assertGreaterEqual(lane_counts.get("consulting_recruiting", 0), 1)

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

    def test_populate_role_queue_from_company_sites(self):
        company_sites = Path(tempfile.mkdtemp()) / "company_site_urls.csv"
        queue_path = Path(tempfile.mkdtemp()) / "role_queue.csv"

        with company_sites.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["company", "domain", "company_url", "careers_url", "source", "notes"])
            writer.writerow(["Epic", "epic.com", "https://www.epic.com", "https://careers.epic.com/", "public_site", "Official public careers site"])
            writer.writerow(["GitLab", "gitlab.com", "https://about.gitlab.com", "https://about.gitlab.com/jobs/", "public_site", "Official jobs site"])

        rows = populate_role_queue_from_company_sites(
            source_path=company_sites,
            target_path=queue_path,
        )

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["company"], "Epic")
        self.assertEqual(rows[0]["careers_url"], "https://careers.epic.com/")
        self.assertEqual(rows[1]["company"], "GitLab")
        self.assertTrue(queue_path.exists())

    def test_build_top_roles_output_backs_up_existing_file_before_overwrite(self):
        source_path = Path(tempfile.mkdtemp()) / "role_queue.csv"
        target_dir = Path(tempfile.mkdtemp())
        target_path = target_dir / "top_roles_output.csv"
        backup_root = target_dir / "backups"
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text("old\ncontent\n", encoding="utf-8")

        with source_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["company", "website", "job_title", "location", "role_type", "fit_score", "status", "priority", "source", "notes"])
            writer.writerow(["Epic", "https://www.epic.com", "Senior Platform Engineer", "Remote - US", "platform", "95", "new", "high", "company_careers", "Strong fit"])

        rows = build_top_roles_output(source_path=source_path, target_path=target_path, limit=1)

        self.assertEqual(len(rows), 1)
        backups = sorted(backup_root.glob("top_roles_output*.csv"))
        self.assertGreaterEqual(len(backups), 1)
        self.assertIn("old", backups[0].read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
