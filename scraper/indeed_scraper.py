from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import urllib
from .utils import normalize_text, parse_relative_date


# Configure Selenium to use Chrome
def setup_selenium():
    edge_options = Options()
    #edge_options.add_argument("--headless")  # Uncomment to run in headless mode
    edge_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation detection
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")
    edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59")
    edge_options.headless = False  # Set to True for headless mode

    # Use webdriver_manager to automatically download and manage Edge WebDriver
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=edge_options)
    return driver


# Load job listings from Indeed
def load_indeed_jobs_div(driver, job_title, location, start=0):
    # Construct the URL
    getVars = {'q': job_title, 'l': location, 'fromage': 'last'}  # Removed 'sort': 'date'
    url = ('https://www.indeed.co.uk/jobs?' + urllib.parse.urlencode(getVars))

    # Open the URL
    driver.get(url)
    time.sleep(10)  # Wait for the page to load

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

    # Extract job IDs
    job_ids = []
    cols.append('job_ids')
    for job_elem in job_elems:
        job_ids.append(extract_job_id_indeed(job_elem))
    extracted_info.append(job_ids)

    jobs_list = {}

    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]

    num_listings = len(extracted_info[0])

    return jobs_list, num_listings


# Helper functions to extract specific job details
def extract_job_id_indeed(job_elem):
    a_elem = job_elem.find('a', {'data-jk': True})
    if a_elem:
        job_id = a_elem.get('data-jk')
        if job_id:
            return job_id.strip()
    print("Failed to extract job_id from:", job_elem)  # Debugging print
    return "N/A"


def extract_job_title_indeed(job_elem):
    title_elem = job_elem.select_one('[id^="jobTitle"]')
    if title_elem:
        title_text = title_elem.text.strip()
        title_text = normalize_text(title_text)
        return title_text
    return "N/A"


def extract_company_indeed(job_elem):
    company_elem = job_elem.find('span', class_='css-1h7lukg eu4oa1w0')
    if company_elem:
        return company_elem.text.strip()
    return "N/A"


def extract_link_indeed(job_elem):
    link_elem = job_elem.find('a', href=True)
    if link_elem:
        return 'https://www.indeed.co.uk' + link_elem['href']
    return "N/A"


def extract_date_indeed(job_elem):
    # Look for the date element using data-testid
    date_elem = job_elem.find('span', attrs={'data-testid': 'myJobsStateDate'})
    if date_elem:
        # Extract the text (e.g., "EmployerActive 11 days ago")
        date_text = date_elem.text.strip()
        # Extract just the date part (e.g., "11 days ago")
        if "Active" in date_text:
            date_text = date_text.split("Active")[-1].strip()
        return parse_relative_date(date_text)
    return "Date not provided"

