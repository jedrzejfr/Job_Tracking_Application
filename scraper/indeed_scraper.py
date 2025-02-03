from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import urllib
from urllib import parse
from .utils import parse_relative_date


# Configure Selenium to use Chrome
def setup_selenium():
    edge_options = Options()
    edge_options.headless = False  # Set to True for headless mode
    edge_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation detection
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")
    edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                              "like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59")

    # Use webdriver_manager to automatically download and manage Edge WebDriver
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=edge_options)
    return driver


# Load job listings from Indeed
def load_indeed_jobs_div(driver, job_title, location, start):
    # Construct the URL
    getVars = {'q': job_title, 'l': location, 'fromage': 'last', 'start': start}
    url = ('https://www.indeed.co.uk/jobs?' + urllib.parse.urlencode(getVars))

    # Open the URL
    driver.get(url)
    # Wait for the job listings to load
    try:
        WebDriverWait(driver, 600).until(
            # Adjusted to detect 'job_seen_beacon' class
            ec.presence_of_element_located((By.CLASS_NAME, "job_seen_beacon"))
        )
    except:
        print("Job listings did not load within the expected time.")

    # Return the page source for parsing
    return driver.page_source


# Extract job information from the page
def extract_job_information_indeed(job_soup, desired_characs):
    job_elems = job_soup.find_all('div', class_='job_seen_beacon')

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

    if 'locations' in desired_characs:
        locations = []
        cols.append('locations')
        for job_elem in job_elems:
            locations.append(extract_location_indeed(job_elem))
        extracted_info.append(locations)

    if 'salaries' in desired_characs:
        salaries = []
        cols.append('salaries')
        for job_elem in job_elems:
            salaries.append(extract_salary_indeed(job_elem))
        extracted_info.append(salaries)

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

    if 'job_ids' in desired_characs:
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


def extract_salary_indeed(job_elem):
    salary_elem = job_elem.find('div', class_='metadata salary-snippet-container css-1f4kgma eu4oa1w0')
    if salary_elem:
        return salary_elem.text.strip()
    return "No salary range listed"


def extract_location_indeed(job_elem):
    location_elem = job_elem.find('div', {'data-testid': 'text-location'})
    if location_elem:
        return location_elem.text.strip()
    return


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
        return title_elem.text.strip()
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



