from seleniumbase import SB
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def setup_seleniumbase():
    with SB(
        uc=True,  # Use undetected-chromedriver (or undetected-edgedriver)
        headless=False,  # Set to True for headless mode
        agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",  # Set user-agent
    ) as sb:
        # Open the target URL with reconnection handling
        sb.driver.uc_open_with_reconnect(
            "https://uk.indeed.com/jobs?q=software+engineer&l=London",
            reconnect_time=4,  # Time to wait for reconnection
        )
        return sb.driver

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

# Example usage
if __name__ == "__main__":
    driver = setup_seleniumbase()
    driver2 = setup_selenium()
    # Perform additional actions with the driver
    print(driver)
    print(driver2)