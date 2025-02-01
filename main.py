# Jedrzej Fratczak
# jedrzej.fratczak@gmail.com
# Job Tracking Application

import json
from scraper import (
    setup_indeed_selenium,
    load_indeed_jobs_div,
    extract_job_information_indeed,
    # setup_other_selenium,
    # load_other_jobs_div,
    # extract_job_information_other
)
from bs4 import BeautifulSoup


def scrape_indeed():
    """
    Scrape job listings from Indeed.
    """
    # Set up Selenium for Indeed
    driver = setup_indeed_selenium()

    try:
        # Initialize a dictionary to store all job listings
        all_jobs = {
            'titles': [],
            'companies': [],
            'links': [],
            'date_listed': []
        }

        # Scrape 3 pages
        for page in range(3):  # Scrape pages 1, 2, and 3
            start = page * 15  # Indeed uses increments of 10 for pagination
            print(f"Scraping Indeed page {page + 1}...")

            # Load job listings for the current page
            job_soup = load_indeed_jobs_div(driver, "software engineer", "London", start=start)
            if job_soup:
                # Parse the page source with BeautifulSoup
                soup = BeautifulSoup(job_soup, "html.parser")

                # Extract job information
                jobs_list, num_listings = extract_job_information_indeed(soup, ['titles', 'companies', 'links', 'date_listed'])

                # Append the results to the all_jobs dictionary
                for key in all_jobs:
                    all_jobs[key].extend(jobs_list.get(key, []))

                print(f"Found {num_listings} listings on Indeed page {page + 1}")

        # Print all job listings
        print("\nAll Indeed Job Listings:")
        print(json.dumps(all_jobs, indent=4))
        print(f"Total Indeed listings: {len(all_jobs['titles'])}")

    finally:
        # Close the browser
        driver.quit()


# def scrape_other_website():


def main():
    """
    Main function to run all scrapers.
    """
    # Scrape Indeed
    scrape_indeed()

    # Scrape another website (uncomment when ready)
    # scrape_other_website()


if __name__ == "__main__":
    main()