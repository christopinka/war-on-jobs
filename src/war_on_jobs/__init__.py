"""War on Jobs local screening package."""

from .job_scan import (
    BAD_KEYWORDS,
    DEFAULT_ALLOWED_LOCATIONS,
    GOOD_KEYWORDS,
    location_allowed,
    parse_job_rows,
    score_job,
    should_reject,
)

__all__ = [
    "BAD_KEYWORDS",
    "DEFAULT_ALLOWED_LOCATIONS",
    "GOOD_KEYWORDS",
    "location_allowed",
    "parse_job_rows",
    "score_job",
    "should_reject",
]
