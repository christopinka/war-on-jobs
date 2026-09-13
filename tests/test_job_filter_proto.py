import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from war_on_jobs.job_filter_proto import location_allowed


class LocationFilterTests(unittest.TestCase):
    def test_global_and_remote_are_allowed_by_default(self):
        self.assertTrue(location_allowed({"location": "Remote"}))
        self.assertTrue(location_allowed({"location": "Berlin, Germany"}))
        self.assertTrue(location_allowed({"location": "London, UK"}))

    def test_us_only_filter_rejects_non_us(self):
        self.assertFalse(location_allowed({"location": "Madrid, Spain"}, allowed_locations=["us"]))
        self.assertTrue(location_allowed({"location": "New York, NY"}, allowed_locations=["us"]))

    def test_europe_filter_allows_eu_targets(self):
        self.assertTrue(location_allowed({"location": "Lisbon, Portugal"}, allowed_locations=["europe"]))
        self.assertTrue(location_allowed({"location": "Frankfurt, Germany"}, allowed_locations=["europe"]))
        self.assertFalse(location_allowed({"location": "Tokyo, Japan"}, allowed_locations=["europe"]))


if __name__ == "__main__":
    unittest.main()
