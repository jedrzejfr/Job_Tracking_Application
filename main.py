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
from database import create_connection, create_table, insert_job
from bs4 import BeautifulSoup


def scrape_indeed(db_conn):
    """
    Scrape job listings from Indeed and save them to the database.
    """
    # Set up Selenium for Indeed
    driver = setup_indeed_selenium()

    try:
        # Initialize a dictionary to store all job listings
        all_jobs = {
            'titles': [],
            'companies': [],
            'links': [],
            'date_listed': [],
            'job_ids': []  # Add job_ids to the dictionary
        }

        # Scrape 3 pages
        for page in range(10):  # Scrape pages 1, 2, and 3
            start = page * 15  # Indeed uses increments of 10 for pagination
            print(f"Scraping Indeed page {page + 1}...")

            # Load job listings for the current page
            try:
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
            except Exception as e:
                print(f"Error scraping page {page + 1}: {e}")

        # Save job listings to the database
        for i in range(len(all_jobs['titles'])):
            job = (
                all_jobs['titles'][i],
                all_jobs['companies'][i],
                all_jobs['links'][i],
                all_jobs['date_listed'][i],
                all_jobs['job_ids'][i]  # Include job_id
            )
            insert_job(db_conn, job, source="indeed")  # Pass the source parameter

        # Print all job listings
        print("\nAll Indeed Job Listings:")
        print(json.dumps(all_jobs, indent=4))
        print(f"Total Indeed listings: {len(all_jobs['titles'])}")

    finally:
        # Close the browser
        driver.quit()





# def scrape_other_website(db_conn):
#     """
#     Scrape job listings from another website and save them to the database.
#     """
#     pass


def main():
    """
    Main function to run all scrapers and save data to the database.
    """
    # Connect to the SQLite database
    db_conn = create_connection("database/jobs.db")
    if db_conn is not None:
        # Create the jobs table (if it doesn't exist)
        create_table(db_conn)

        # Scrape Indeed and save data to the database
        scrape_indeed(db_conn)  # Pass db_conn as a parameter

        # Scrape another website (uncomment when ready)
        # scrape_other_website(db_conn)

        # Close the database connection
        db_conn.close()
    else:
        print("Error: Could not connect to the database.")


if __name__ == "__main__":
    main()