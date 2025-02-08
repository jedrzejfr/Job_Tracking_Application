# Import functions/classes from indeed_scraper
from .indeed_scraper import (
    setup_selenium as setup_indeed_selenium,
    load_indeed_jobs_div,
    extract_job_information_indeed
)

# Import functions/classes from other_scraper (future scraper)
# from .other_scraper import (
#     setup_selenium as setup_other_selenium,
#     load_other_jobs_div,
#     extract_job_information_other
# )

# Expose reusable utility functions
from .utils import parse_relative_date

# Define what gets imported when using `from scraper import *`
__all__ = [
    'setup_indeed_selenium',
    'load_indeed_jobs_div',
    'extract_job_information_indeed',
    # 'setup_other_selenium',
    # 'load_other_jobs_div',
    # 'extract_job_information_other',
    'parse_relative_date'
]