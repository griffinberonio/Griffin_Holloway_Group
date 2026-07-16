import pandas as pd
import matplotlib.pyplot as plt 
import geopandas as gpd
import numpy as np
from bs4 import BeautifulSoup
import requests
import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Establishing the Vessel Finder base URL and calling the ship data CSV:

# Vessel Finder URL
baseurl = 'https://www.vesselfinder.com/vessels'

# Ship CSV: 
shipcsv = '/Users/griffinberonio/Documents/Holloway_Group/Data/Copy of south_coast_ship_lookup.csv'


def find_shipdata(ship, baseurl):

    info = {}

    delay = random.uniform(1.5, 30.3)

    # Spin up a Chrome browser

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get(baseurl)

    # Find elements — same ideas as BeautifulSoup but different syntax

    search_box = driver.find_element(By.ID, "advsearch-name")

    time.sleep(delay)
    ActionChains(driver).move_to_element(search_box).click().send_keys(ship).perform()
    time.sleep(delay)

    # search_box.send_keys('9354662')
    search_button = driver.find_element(By.CSS_SELECTOR, "button[data-action='Search']")
    search_button.click()

    print(driver.title)
    print(driver.page_source[:2000])

    # Wait for results page to load
    WebDriverWait(driver, delay).until(
        EC.url_changes(driver.current_url)
    )

    print(driver.title)
    print(driver.page_source[:2000])

    # Click the ship link
    ship_link = driver.find_element(By.CSS_SELECTOR, "a.ship-link")
    ship_link.click()

    # Wait for the details page to load
    WebDriverWait(driver, delay).until(
        EC.url_contains("/vessels/details/")
    )

    # Scrape the details page
    soup = BeautifulSoup(driver.page_source, "html.parser")

    driver.quit()
    
    # Finding Gross Tonnage and Year of Build from the soup:

    for section in soup.find_all("section", class_="ship-section"):
        heading = section.find("h2", class_="bar")
        if heading and heading.text.strip() == "Vessel Particulars":
            
            # Parse all label/value pairs into a dict
            data = {}
            for row in section.find_all("tr"):
                cells = row.find_all("td")
                if len(cells) == 2:
                    label = cells[0].text.strip()
                    value = cells[1].text.strip()
                    data[label] = value
            
            # Pull what you need
            gross_tonnage = data.get("Gross Tonnage")
            year_of_build = data.get("Year of Build")
            
            print(f"Gross Tonnage: {gross_tonnage}")
            print(f"Year of Build: {year_of_build}")
            
            # Append information to info dictionary:
            info['ship'] = ship
            info['GT'] = gross_tonnage
            info['Build_Year'] = year_of_build

            break

    infodf = pd.DataFrame(info)
    return infodf

    


if __name__ == "__main__":
    testship = '9354662'

    testshipinfo = find_shipdata(testship, baseurl=baseurl)
    print(testshipinfo)