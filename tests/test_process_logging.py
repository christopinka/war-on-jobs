import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from war_on_jobs.process_logging import log_event


class ProcessLoggingTests(unittest.TestCase):
    def test_log_event_writes_to_file_and_stdout(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "site_discovery.log"
            with unittest.mock.patch("sys.stdout") as mock_stdout:
                written = log_event(
                    "site_unavailable",
                    company="Epic",
                    domain="epic.com",
                    url="https://careers.epic.com/",
                    note="site responded with 404",
                    path=log_path,
                )

            self.assertEqual(written, log_path)
            self.assertTrue(log_path.exists())
            contents = log_path.read_text(encoding="utf-8")
            self.assertIn("site_unavailable", contents)
            self.assertIn("Epic", contents)
            mock_stdout.write.assert_called()


if __name__ == "__main__":
    unittest.main()
