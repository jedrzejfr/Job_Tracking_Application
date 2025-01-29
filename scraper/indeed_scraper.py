from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # Automatically manages ChromeDriver
import time
import urllib
import json
import unicodedata
import re
import html

# Configure Selenium to use Chrome
def setup_selenium():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument("accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
    chrome_options.add_argument("accept-language=en-US,en;q=0.5")
    chrome_options.headless = False

    # Use webdriver_manager to automatically download and manage ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


# Load job listings from Indeed
def load_indeed_jobs_div(driver, job_title, location):
    # Construct the URL
    getVars = {'q': job_title, 'l': location, 'fromage': 'last', 'sort': 'date'}
    url = ('https://www.indeed.co.uk/jobs?' + urllib.parse.urlencode(getVars))

    # Open the URL
    driver.get(url)
    time.sleep(6)  # Wait for the page to load

    # Return the page source for parsing
    return driver.page_source


# Extract job information from the page
def extract_job_information_indeed(job_soup, desired_characs):
    job_elems = job_soup.find_all('div', class_='job_seen_beacon')  # Updated class name

    cols = []
    extracted_info = []

    if 'titles' in desired_characs:
        titles = []
        cols.append('titles')
        for job_elem in job_elems:
            titles.append(extract_job_title_indeed(job_elem))
        extracted_info.append(titles)

    if 'companies' in desired_characs:
        companies = []
        cols.append('companies')
        for job_elem in job_elems:
            companies.append(extract_company_indeed(job_elem))
        extracted_info.append(companies)

    if 'links' in desired_characs:
        links = []
        cols.append('links')
        for job_elem in job_elems:
            links.append(extract_link_indeed(job_elem))
        extracted_info.append(links)

    if 'date_listed' in desired_characs:
        dates = []
        cols.append('date_listed')
        for job_elem in job_elems:
            dates.append(extract_date_indeed(job_elem))
        extracted_info.append(dates)

    jobs_list = {}

    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]

    num_listings = len(extracted_info[0])

    return jobs_list, num_listings


def normalize_text(text):
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(u"\u2013", "-", text)  # Replace en dash with hyphen for readability
    text = re.sub(u"\u2014", "-", text)  # Replace em dash with hyphen for readability
    text = re.sub(u"\u2010", "-", text)  # Replace hyphen
    text = re.sub(u"\u00e2\u0080\u0093", "-", text)  # Replace problematic sequence
    text = html.unescape(text)
    return text.strip()


# Helper functions to extract specific job details
def extract_job_title_indeed(job_elem):
    title_elem = job_elem.select_one('[id^="jobTitle"]')
    if title_elem:
        title_text = title_elem.text.strip()
        title_text = normalize_text(title_text)
        return title_text
    return "N/A"




def extract_company_indeed(job_elem):
    company_elem = job_elem.find('span', class_='company')
    if company_elem:
        return company_elem.text.strip()
    return "N/A"


def extract_link_indeed(job_elem):
    link_elem = job_elem.find('a', href=True)
    if link_elem:
        return 'https://www.indeed.co.uk' + link_elem['href']
    return "N/A"


def extract_date_indeed(job_elem):
    date_elem = job_elem.find('span', class_='date')
    if date_elem:
        return date_elem.text.strip()
    return "N/A"


# Main function
if __name__ == "__main__":
    # Set up Selenium
    driver = setup_selenium()

    try:
        # Load job listings
        job_soup = load_indeed_jobs_div(driver, "software engineer", "London")
        if job_soup:
            # Parse the page source with BeautifulSoup
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(job_soup, "html.parser")

            # Extract job information
            jobs_list, num_listings = extract_job_information_indeed(soup,
                                                                     ['titles', 'companies', 'links', 'date_listed'])
            # Print job list in a readable format
            print(json.dumps(jobs_list, indent=4))
            print(f"Number of listings: {num_listings}")
    finally:
        # Close the browser
        driver.quit()
