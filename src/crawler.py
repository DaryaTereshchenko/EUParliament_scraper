from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from selenium.webdriver.chrome.options import Options
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from utils import save_as_json, extract_links

def crawler(url, query, dir, filename):
    """
    Crawl the webpage to extract links
    :param url: URL of the webpage
    :param query: query to search
    :param dir: directory to save the links
    :param filename: name of the file
    """

    driver = webdriver.Chrome()
    links_to_scrape = []
    try:
        # Open the webpage
        driver.get(url)

        # Dropdown menu options
        time_period = ['2014 - 2019', '2009 - 2014', '2004 - 2009', '1999 - 2004', '2019 - 2024']
        
        for period in time_period:
            print("="*50)
            print(f"Extracting links from {period}")
            # Find and click on the dropdown button to open the dropdown menu
            dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#criteriaSidesLeg-button')))
            dropdown.click()
            time.sleep(3)
            
            # Locate the option in the dropdown menu and click on it
            option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//ul[@id="criteriaSidesLeg-menu"]/li/a[contains(text(), "{period}")]')))
            option.location_once_scrolled_into_view
            option.click()
            time.sleep(3)

            # Find the search input field and insert the query
            search_input = driver.find_element(By.CSS_SELECTOR, '#criteriaSidesMiText.field_full_width')
            search_input.clear()  # Clear any previous input
            search_input.send_keys(query)
            time.sleep(3)
            print("Query inserted")

            search_button = driver.find_element(By.ID, 'sidesButtonSubmit')
            search_button.click()
            print("Search button clicked")
            time.sleep(5)

            # Get the HTML content of the page after search
            html_content = driver.page_source

            # Extract links from the HTML content
            extracted_links = extract_links(html_content)
            links_to_scrape.extend(extracted_links)

            # Check if there is a next page
            try:
                first_page = driver.find_element(By.XPATH, '//*[@id="content_left"]/div[2]/div[15]/a')
            except NoSuchElementException:
                first_page = None
            
            if first_page:
                print("Next page found.")
                html_content = driver.page_source

                # Click on the next page
                first_page.location_once_scrolled_into_view
                first_page.click()
                time.sleep(3)

                # Extract links from the next page
                links_to_scrape.extend(extract_links(html_content))

            # Check if there is a next button on following pages after the first one
            try:
                next_button = driver.find_element(By.XPATH, '//*[@id="content_left"]/div[2]/div[15]/a[2]')
            except NoSuchElementException:
                next_button = None

            while next_button:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content_left"]/div[2]/div[15]/a[2]')))
                next_button.location_once_scrolled_into_view
                next_button.click()
                time.sleep(3)

                html_content = driver.page_source
                links_to_scrape.extend(extract_links(html_content))
                print("Links extracted.")

                print("Proceed to the next page.")
                time.sleep(3)

                try:
                    next_button = driver.find_element(By.XPATH, '//*[@id="content_left"]/div[2]/div[15]/a[2]')
                except NoSuchElementException:
                    break

            print("Links extracted from the last page.")

    finally:
        driver.quit()
        save_as_json(links_to_scrape, dir, f"{filename}.json")


if __name__ == '__main__':
    # Prompt the user to enter the URL of the webpage
    url = input("Enter the URL of the webpage: ")
    # Prompt the user to enter the query
    query = input("Enter the query: ")
    # Prompt the user to enter the directory to save the links
    dir = input("Enter the directory to save the links: ")
    # Prompt the user to enter the filename
    filename = input("Enter the filename without any extention: ")

    # Call the crawler function
    crawler(url, query, dir, filename)