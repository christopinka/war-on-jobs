import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from war_on_jobs.site_allowlist import is_allowed_site, load_site_allowlist


class SiteAllowlistTests(unittest.TestCase):
    def test_load_site_allowlist_reads_config(self):
        domains = load_site_allowlist()
        self.assertIn("epic.com", domains)
        self.assertIn("oracle.com", domains)
        self.assertTrue(len(domains) >= 5)

    def test_is_allowed_site_accepts_repo_config_domains(self):
        self.assertTrue(is_allowed_site("https://careers.epic.com/"))
        self.assertTrue(is_allowed_site("https://www.oracle.com/careers/"))
        self.assertFalse(is_allowed_site("https://www.example.com/jobs"))


if __name__ == "__main__":
    unittest.main()
