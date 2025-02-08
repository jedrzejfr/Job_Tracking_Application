from seleniumbase import SB

def setup_seleniumbase():
    try:
        with SB(
            browser="chrome",  # Use "chrome" for Chrome
            headless=True,  # Set to True for headless mode
            uc=True,  # Use undetected driver
        ) as sb:
            sb.open("https://uk.indeed.com/jobs?q=software+engineer&l=London")
            sb.save_screenshot("indeed_jobs.png")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    setup_seleniumbase()