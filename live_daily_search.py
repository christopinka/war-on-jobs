#!/usr/bin/env python3

import sys

from src.war_on_jobs.live_daily_search import main


if __name__ == "__main__":
    sys.argv = ["live_daily_search.py", *sys.argv[1:]]
    main()
