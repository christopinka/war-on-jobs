import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from war_on_jobs.job_daily_scan import location_allowed, score_job, should_reject


class DailyScanTests(unittest.TestCase):
    def test_global_remote_and_europe_allowed(self):
        self.assertTrue(location_allowed("Remote"))
        self.assertTrue(location_allowed("Global"))
        self.assertTrue(location_allowed("Berlin, Germany"))
        self.assertTrue(location_allowed("London, UK"))

    def test_us_only_rejects_non_us(self):
        self.assertFalse(location_allowed("Madrid, Spain", allowed_locations=["us"]))
        self.assertTrue(location_allowed("New York, NY", allowed_locations=["us"]))

    def test_rejects_vendor_and_keeps_direct_employer_roles(self):
        self.assertTrue(should_reject("Senior Software Engineer", "A recruiter firm", "Remote"))
        self.assertFalse(should_reject("Senior Platform Engineer", "Pivotal Health", "Remote"))

    def test_scoring_prefers_technical_healthcare_matches(self):
        self.assertGreater(score_job("Senior Platform Engineer", "Pivotal Health", "Remote"), 0)
        self.assertLess(score_job("Vendor Recruiter", "Staffing Co", "Remote"), 0)


if __name__ == "__main__":
    unittest.main()
