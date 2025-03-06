def construct_totaljobs_url(job_title, location, page):
    """
    Construct the TotalJobs URL for a given job title, location, and page number.
    """
    # Replace spaces with hyphens in job title and location
    job_title_formatted = job_title.replace(" ", "-").lower()
    location_formatted = location.replace(" ", "-").lower()

    # Construct the URL
    url = f"https://www.totaljobs.com/jobs/{job_title_formatted}/in-{location_formatted}?page={page}"
    return url


# Example usage
job_title = "software engineer"
location = "london"
page = 1  # Page starts from 1
url = construct_totaljobs_url(job_title, location, page)
print(url)  # Output: https://www.totaljobs.com/jobs/software-engineer/in-london?page=1