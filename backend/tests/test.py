from seleniumbase import SB

def setup_seleniumbase():
    with SB(
        browser="chrome",  # Use "chrome" for Chrome
        headless=True,  # Set to True for headless mode
        uc=True,  # Use undetected driver
        agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",  # Set user-agent
    ) as sb:
        sb.open("https://uk.indeed.com/jobs?q=software+engineer&l=London")
        sb.save_screenshot("indeed_jobs12.png")

if __name__ == "__main__":
    setup_seleniumbase()