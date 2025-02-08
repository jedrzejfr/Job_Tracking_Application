from seleniumbase import Driver
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import undetected_chromedriver2 as uc


def parse_relative_date(date_text):
    """
    Convert relative dates like "26 days ago" into a formatted date (day/month/year).
    """
    if "today" in date_text.lower() or "just now" in date_text.lower():
        return datetime.now().strftime("%d/%m/%Y")
    elif "day" in date_text:
        try:
            days_ago = int(date_text.split()[0])  # Extract the number of days
            actual_date = datetime.now() - timedelta(days=days_ago)
            return actual_date.strftime("%d/%m/%Y")
        except (ValueError, IndexError):
            pass  # Handle invalid date formats
    return "Date not provided"


def setup_driver():
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
    #options.add_argument("--log-level=3")  # Suppress logging
    #options.add_argument("--silent")  # Suppress errors

    driver = uc.Chrome(options=options)  # Set Chrome version manually
    return driver


def get_page_source(url):
    driver = setup_driver()
    driver.get(url)
    time.sleep(5)  # Allow time for dynamic content to load
    page_source = driver.page_source
    driver.quit()
    return page_source


def scrape_indeed_jobs():
    url = "https://uk.indeed.com/jobs?q=software+engineer&l=London"
    page_source = get_page_source(url)
    soup = BeautifulSoup(page_source, 'html.parser')

    desired_characs = ['titles', 'companies', 'locations', 'salaries', 'links', 'date_listed', 'job_ids']
    job_data, num_listings = extract_job_information_indeed(soup, desired_characs)

    print(f"Extracted {num_listings} job listings:")
    for i in range(num_listings):
        print(
            f"{i + 1}. {job_data['titles'][i]} - {job_data['companies'][i]} - {job_data['locations'][i]} - {job_data['salaries'][i]} - {job_data['links'][i]} - {job_data['date_listed'][i]} - {job_data['job_ids'][i]}")

    return job_data

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


if __name__ == "__main__":
    job_results = scrape_indeed_jobs()
