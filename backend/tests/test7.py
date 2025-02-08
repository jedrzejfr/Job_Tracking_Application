from seleniumbase import BaseCase
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

def load_indeed_jobs_div(driver, job_title, location, start):
    # Construct the URL
    getVars = {'q': job_title, 'l': location, 'fromage': 'last', 'start': start}
    url = 'https://www.indeed.co.uk/jobs?' + urllib.parse.urlencode(getVars)

    # Open the URL
    driver.open(url)

    # Wait for the job listings to load
    try:
        driver.wait_for_element('.job_seen_beacon', timeout=10)
    except:
        print("Job listings did not load within the expected time.")

    # Return the page source for parsing
    return driver.get_page_source()

class IndeedJobSearchTest(BaseCase):
    def test_load_jobs(self):
        job_title = "Software Engineer"
        location = "London"
        start = 0

        # Use self as the driver
        page_source = load_indeed_jobs_div(self, job_title, location, start)

        # Optional: Print or validate the page source
        print(page_source[:500])  # Print first 500 characters for verification
