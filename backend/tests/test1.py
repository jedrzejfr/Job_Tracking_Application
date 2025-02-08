from seleniumbase import SB

def setup_seleniumbase():
    with SB(
        browser="edge",  # Use "chrome" for Chrome
        headless=False,  # Set to True for headless mode
        uc=True,  # Use undetected driver
        agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",  # Set user-agent
    ) as sb:
        # Open the target URL
        sb.open("https://uk.indeed.com/jobs?q=software+engineer&l=London")

        # Perform actions with the driver inside the context manager
        sb.save_screenshot("indeed_jobs.png")

        # You can also access the driver directly if needed
        print(sb.driver.title)  # Print the page title

        # No need to return the driver