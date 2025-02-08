from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium_stealth import stealth
import urllib.parse
from datetime import datetime, timedelta
import json
from bs4 import BeautifulSoup
import time
import random


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


def random_delay():
    time.sleep(random.uniform(1, 3))  # Random delay between 1 and 3 seconds


def load_indeed_jobs_div(driver, job_title, location, start):
    """
    Load job listings from Indeed with retry logic.
    """
    # Construct the URL
    getVars = {'q': job_title, 'l': location, 'fromage': 'last', 'start': start}
    url = ('https://www.indeed.co.uk/jobs?' + urllib.parse.urlencode(getVars))

    retry_count = 0
    while True:
        print(f"Attempting to load page: {url} (Attempt {retry_count + 1})")
        driver.get(url)
        random_delay()  # Add a random delay

        # Wait for the job listings to load (2 seconds max)
        try:
            WebDriverWait(driver, 3).until(
                ec.presence_of_element_located((By.CLASS_NAME, "job_seen_beacon"))
            )
            print("Page loaded successfully!")
            break  # Exit the retry loop if the page loads successfully
        except:
            print("Page did not load within 2 seconds. Retrying...")
            retry_count += 1

    # Return the page source for parsing
    return driver.page_source


def get_page_sources(job_title, location):
    page_sources = []

    # Configure Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=options)

    # Use Selenium Stealth to avoid detection
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    try:
        for start in [0, 15, 30]:  # Scrape first 3 pages (start values: 0, 10, 20)
            print(f"\nScraping page {start // 15 + 1}...")
            page_source = load_indeed_jobs_div(driver, job_title, location, start)
            page_sources.append(page_source)
    finally:
        driver.quit()  # Close the browser

    return page_sources


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


def main():
    try:
        job_title = "Software Engineer"
        location = "London"
        print("Starting scraping process...")
        page_sources = get_page_sources(job_title, location)

        all_jobs_list = {}
        for page_source in page_sources:
            soup = BeautifulSoup(page_source, "html.parser")
            jobs_list, num_listings = extract_job_information_indeed(
                soup, ['titles', 'companies', 'locations', 'salaries', 'links', 'date_listed', 'job_ids']
            )
            # Combine results from all pages
            for key, value in jobs_list.items():
                if key in all_jobs_list:
                    all_jobs_list[key].extend(value)
                else:
                    all_jobs_list[key] = value

        print("\nAll Indeed Job Listings (First 3 Pages):")
        print(json.dumps(all_jobs_list, indent=4, ensure_ascii=False))
        print(f"Total Indeed listings: {len(all_jobs_list['titles'])}")
    finally:
        print("Finished scraping.")


if __name__ == "__main__":
    main()