from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import urllib
from urllib import parse
from .utils import parse_relative_date, random_delay


# Configure Selenium to use Chrome
def load_totaljobs_jobs_div(sb, job_title, location, start):
    """
    Load job listings from totaljobs with retry logic.
    """
    # Construct the URL
    getVars = {'q': job_title, 'l': location, 'fromage': 'last', 'start': start}
    url = ('https://www.totaljobs.co.uk/jobs?' + urllib.parse.urlencode(getVars))

    retry_count = 0
    while True:
        print(f"Attempting to load page: {url} (Attempt {retry_count + 1})")
        sb.open(url)
        random_delay()  # Add a random delay

        # Wait for the job listings to load (2 seconds max)
        try:
            WebDriverWait(sb.driver, 1).until(
                ec.presence_of_element_located((By.CLASS_NAME, "job_seen_beacon"))
            )
            print("Page loaded successfully!")
            break  # Exit the retry loop if the page loads successfully
        except:
            print("Page did not load within 2 seconds. Retrying...")
            retry_count += 1

    # Return the page source for parsing
    return sb.get_page_source()


# Extract job information from the page
def extract_job_information_totaljobs(job_soup, desired_characs):
    job_elems = job_soup.find_all('div', class_='job_seen_beacon')

    cols = []
    extracted_info = []

    if 'titles' in desired_characs:
        titles = []
        cols.append('titles')
        for job_elem in job_elems:
            titles.append(extract_job_title_totaljobs(job_elem))
        extracted_info.append(titles)

    if 'companies' in desired_characs:
        companies = []
        cols.append('companies')
        for job_elem in job_elems:
            companies.append(extract_company_totaljobs(job_elem))
        extracted_info.append(companies)

    if 'locations' in desired_characs:
        locations = []
        cols.append('locations')
        for job_elem in job_elems:
            locations.append(extract_location_totaljobs(job_elem))
        extracted_info.append(locations)

    if 'salaries' in desired_characs:
        salaries = []
        cols.append('salaries')
        for job_elem in job_elems:
            salaries.append(extract_salary_totaljobs(job_elem))
        extracted_info.append(salaries)

    if 'links' in desired_characs:
        links = []
        cols.append('links')
        for job_elem in job_elems:
            links.append(extract_link_totaljobs(job_elem))
        extracted_info.append(links)

    if 'date_listed' in desired_characs:
        dates = []
        cols.append('date_listed')
        for job_elem in job_elems:
            dates.append(extract_date_totaljobs(job_elem))
        extracted_info.append(dates)

    if 'job_ids' in desired_characs:
        job_ids = []
        cols.append('job_ids')
        for job_elem in job_elems:
            job_ids.append(extract_job_id_totaljobs(job_elem))
        extracted_info.append(job_ids)

    jobs_list = {}
    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]

    num_listings = len(extracted_info[0])

    return jobs_list, num_listings


def extract_salary_totaljobs(job_elem):
    salary_elem = job_elem.find('div', class_='metadata salary-snippet-container css-1f4kgma eu4oa1w0')
    if salary_elem:
        return salary_elem.text.strip()
    return "No salary range listed"


def extract_location_totaljobs(job_elem):
    location_elem = job_elem.find('div', {'data-testid': 'text-location'})
    if location_elem:
        return location_elem.text.strip()
    return


def extract_job_id_totaljobs(job_elem):
    a_elem = job_elem.find('a', {'data-jk': True})
    if a_elem:
        job_id = a_elem.get('data-jk')
        if job_id:
            return job_id.strip()
    print("Failed to extract job_id from:", job_elem)  # Debugging print
    return "N/A"


def extract_job_title_totaljobs(job_elem):
    title_elem = job_elem.select_one('[id^="jobTitle"]')
    if title_elem:
        return title_elem.text.strip()
    return "N/A"


def extract_company_totaljobs(job_elem):
    company_elem = job_elem.find('span', class_='css-1h7lukg eu4oa1w0')
    if company_elem:
        return company_elem.text.strip()
    return "N/A"


def extract_link_totaljobs(job_elem):
    link_elem = job_elem.find('a', href=True)
    if link_elem:
        return 'https://www.totaljobs.co.uk' + link_elem['href']
    return "N/A"


def extract_date_totaljobs(job_elem):
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



