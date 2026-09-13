from pathlib import Path

from war_on_jobs.live_daily_search import backup_current_state, filter_live_rows, merge_unique_rows


def test_backup_current_state_copies_target_csvs(tmp_path):
    target_dir = tmp_path / "data" / "targets"
    target_dir.mkdir(parents=True)
    (target_dir / "alpha.csv").write_text("company\nEpic\n", encoding="utf-8")
    (target_dir / "beta.csv").write_text("company\nGitLab\n", encoding="utf-8")

    backup_dir = backup_current_state(target_dir=target_dir, backup_root=tmp_path / "data" / "backups")

    assert backup_dir.exists()
    assert (backup_dir / "alpha.csv").exists()
    assert (backup_dir / "beta.csv").exists()
    assert backup_dir.name.startswith("backup_")


def test_filter_live_rows_keeps_good_jobs_and_rejects_noise():
    rows = [
        {"title": "Senior Platform Engineer", "company": "Epic", "location": "Remote US"},
        {"title": "Senior Backend Engineer", "company": "GitLab", "location": "Remote Global"},
        {"title": "Recruiter, Technical Staffing", "company": "Vendor Partners LLC", "location": "Remote US"},
        {"title": "Principal Platform Engineer", "company": "Example Corp", "location": "Berlin, Germany"},
    ]

    kept, rejected = filter_live_rows(rows)

    assert [r["company"] for r in kept] == ["Epic", "GitLab", "Example Corp"]
    assert [r["company"] for r in rejected] == ["Vendor Partners LLC"]


def test_merge_unique_rows_appends_without_duplicates():
    existing = [
        {"title": "Senior Platform Engineer", "company": "Epic", "location": "Remote US", "fit_score": 3, "reject": False, "reason": ""},
    ]
    incoming = [
        {"title": "Senior Platform Engineer", "company": "Epic", "location": "Remote US", "fit_score": 3, "reject": False, "reason": ""},
        {"title": "Senior Backend Engineer", "company": "GitLab", "location": "Remote Global", "fit_score": 2, "reject": False, "reason": ""},
    ]

    merged = merge_unique_rows(existing, incoming)

    assert len(merged) == 2
    assert [r["company"] for r in merged] == ["Epic", "GitLab"]


def test_filter_live_rows_uses_profile_intake_defaults(tmp_path):
    profile_path = tmp_path / "career_profile_intake.yaml"
    profile_path.write_text(
        """
company_and_role_filters:
  keywords_to_prioritize:
    - python
    - aws
  keywords_to_reject:
    - recruiter
    - staffing
    - vendor
  minimum_fit_score: 2
location:
  preferred_locations:
    - remote
    - us
    - europe
""".strip(),
        encoding="utf-8",
    )

    rows = [
        {"title": "Senior Platform Engineer", "company": "Epic", "location": "Remote US"},
        {"title": "Recruiter, Technical Staffing", "company": "Vendor Partners LLC", "location": "Remote US"},
    ]

    kept, rejected = filter_live_rows(rows, profile_path=profile_path)

    assert [r["company"] for r in kept] == ["Epic"]
    assert [r["company"] for r in rejected] == ["Vendor Partners LLC"]


def test_filter_live_rows_uses_profile_minimum_fit_score(tmp_path):
    profile_path = tmp_path / "career_profile_intake.yaml"
    profile_path.write_text(
        """
company_and_role_filters:
  minimum_fit_score: 3
  keywords_to_prioritize:
    - python
    - aws
  keywords_to_reject:
    - recruiter
location:
  preferred_locations:
    - remote
    - us
""".strip(),
        encoding="utf-8",
    )

    rows = [
        {"title": "Platform Engineer", "company": "Example", "location": "Remote US"},
        {"title": "Python Engineer", "company": "Example", "location": "Remote US"},
    ]

    kept, rejected = filter_live_rows(rows, profile_path=profile_path)

    assert [r["company"] for r in kept] == ["Example"]
    assert rejected[0]["reason"] == "low_fit_score"
