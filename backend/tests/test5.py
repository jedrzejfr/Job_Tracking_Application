# coding: utf-8

import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
import base64


logging.basicConfig(level=10)
logger = logging.getLogger('test')


def main():
    driver = None
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')  # Use the new headless mode
        chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration
        chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
        chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

        # Initialize the Chrome driver
        driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Navigate to chrome://version and take a screenshot
        driver.get('chrome://version')
        driver.save_screenshot('/home/runner/work/_temp/versioninfo.png')

        # Navigate to chrome://settings/help and take a screenshot
        driver.get('chrome://settings/help')
        driver.save_screenshot('/home/runner/work/_temp/helpinfo.png')

        # Navigate to Google and take a screenshot
        driver.get('https://www.google.com')
        driver.save_screenshot('/home/runner/work/_temp/google.com.png')

        # Navigate to bot challenge page and generate PDF
        driver.get('https://bot.incolumitas.com/#botChallenge')
        pdfdata = driver.execute_cdp_cmd('Page.printToPDF', {})
        if pdfdata and 'data' in pdfdata:
            buffer = base64.b64decode(pdfdata['data'])
            with open('/home/runner/work/_temp/report.pdf', 'w+b') as f:
                f.write(buffer)

        # Navigate to nowsecure.nl and handle Cloudflare challenge
        driver.get('https://www.nowsecure.nl')
        logger.info('Current URL: %s', driver.current_url)

        try:
            WebDriverWait(driver, 15).until(EC.title_contains('moment'))
        except TimeoutException:
            logger.info('Timeout while waiting for title to contain "moment"')

        logger.info('Current page source:\n%s', driver.page_source)
        logger.info('Current URL: %s', driver.current_url)

        try:
            WebDriverWait(driver, 15).until(EC.title_contains('nowSecure'))
            logger.info('PASSED CLOUDFLARE!')
        except TimeoutException:
            logger.info('Timeout while waiting for title to contain "nowSecure"')
            print(driver.current_url)

        logger.info('Current page source:\n%s\n', driver.page_source)

        # Save a screenshot of the nowsecure.nl page
        driver.save_screenshot('/home/runner/work/_temp/nowsecure.png')

    except Exception as e:
        logger.error('An error occurred: %s', e)
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    main()