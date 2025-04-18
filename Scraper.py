from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
import time

from natrual_hazard import run_natural_hazard

from age_gender import run_age_gender

from income import run_income

from renter_onwer import run_owner_renter

import pandas as pd
from datetime import datetime

import random

# Before doing anything: Run this command to init an instance in CMD

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium\ChromeProfile"


# Before running this script, start Chrome with remote debugging port
# chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenium\ChromeProfile"

# import logging

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# not in use
# def debug_page_state(driver, selector):
#     """Helper function to debug page state"""
#     logger.debug(f"Current URL: {driver.current_url}")
#     logger.debug(f"Page source length: {len(driver.page_source)}")
#     logger.debug(f"Looking for selector: {selector}")
#     elements = driver.find_elements(By.CSS_SELECTOR, selector)
#     logger.debug(f"Found {len(elements)} elements matching selector")
#     if len(elements) > 0:
#         logger.debug(f"Element visible: {elements[0].is_displayed()}")
#         logger.debug(f"Element enabled: {elements[0].is_enabled()}")

class Scraper():
    def __init__(self, prepped_df, uuid):
        # filter out the 
        self.clean_df = prepped_df[prepped_df['Status']=='To be Scraped']
        self.scraped_df = pd.DataFrame()
        self.uuid = uuid

        #wait until the end to fill
        self.scraped_df_path = None

    def setup_driver_with_existing_session(self):
        """Setup Chrome WebDriver using an existing Chrome session"""
        chrome_options = Options()
        # This connects to your existing Chrome instance
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def fill_search_box(self, driver, search_selector, text):
        """Fill in a search box with specified text"""
        try:
            search_box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, search_selector))
            )
            search_box.clear()
            search_box.send_keys(text)
        except TimeoutException:
            print(f"Search box with selector {search_selector} not found")


    def press_enter_on_element(self, driver, selector):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            # element.send_keys(Keys.DOWN) # add down movement
            element.send_keys(Keys.RETURN)  # or Keys.ENTER - they're equivalent
        except TimeoutException:
            print(f"Element with selector {selector} not found")

    def scroll_to_end(self, driver, scroll_pause_time=2, max_retries=2):
        """
        Scroll to the end of page and wait for dynamic content to load
        
        Args:
            driver: Selenium webdriver instance
            scroll_pause_time: Time to wait between scrolls
            max_retries: Maximum number of scroll attempts if height doesn't change
        
        Returns:
            bool: True if reached bottom, False otherwise
        """
        try:
            last_height = driver.execute_script("return document.body.scrollHeight")
            retries = 0
            
            while retries < max_retries:
                # Scroll to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # Wait for new content to load
                time.sleep(scroll_pause_time)
                
                # Calculate new scroll height and compare with last height
                new_height = driver.execute_script("return document.body.scrollHeight")
                
                # Break if no new content (height didn't change)
                if new_height == last_height:
                    retries += 1
                else:
                    # Reset retries if height changed
                    retries = 0
                
                last_height = new_height
                
                # Print progress (optional)
                print(f"Current scroll height: {new_height}")
            
            return True
            
        except Exception as e:
            print(f"Error while scrolling: {str(e)}")
            return False
        
    def scroll_smoothly(self, driver, scroll_pause=0.5, scroll_step=300):
        """
        Smooth scroll to the end of page to trigger lazy loading
        
        Args:
            driver: Selenium webdriver instance
            scroll_pause: Time to wait between each scroll step
            scroll_step: Pixels to scroll in each step
        """
        try:
            # Get scroll height
            last_height = driver.execute_script("return document.body.scrollHeight")
            
            # Current scroll position
            current_position = 0
            
            while current_position < last_height:
                # Scroll down by step
                current_position += scroll_step
                driver.execute_script(f"window.scrollTo(0, {current_position});")
                
                # Wait for content to load
                time.sleep(scroll_pause)
                
                # Update total height
                last_height = driver.execute_script("return document.body.scrollHeight")
                
        except Exception as e:
            print(f"Error while smooth scrolling: {str(e)}")

    def extract_content(self, driver, selector):
        """Extract content from specified element"""
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element.text
        except TimeoutException:
            print(f"Element with selector {selector} not found")
            return None


    def check_search_success(self, driver, success_criteria_selector="#paddress > span.streetAddress"):
        """
        Check whether the search was performed successfully by verifying
        if an element with the specified selector is present.
        
        Args:
            driver: The Selenium WebDriver instance.
            success_criteria_selector: The CSS selector of an element that confirms a successful search.

        Returns:
            bool: True if the element is found, False otherwise.
        """
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, success_criteria_selector))
            )
            print(element)
            if element == None:
                print(f"Search unsuccessful. Element not found.")
                return False                
            else:
                print("Search performed successfully.")
                return True
        except TimeoutException:
            print(f"Search unsuccessful. Element with selector {success_criteria_selector} not found.")
            return False

    def scrape_one_address(self, driver:webdriver, input_index:int, input_address:str):
        
        print(f"Scraping {input_address}")
        self.fill_search_box(driver, "#propertysearch", input_address)
        time.sleep(2)
        self.press_enter_on_element(driver, "#propertysearch")

        #check whether it has been filled successfully? 
        if not self.check_search_success(driver):
            return 
        # scroll_to_end(driver)
        scroll_pause = random.uniform(0.1, 0.6)
        self.scroll_smoothly(driver, scroll_pause=scroll_pause)

        #init the final output dict
        final_result_dict = {'Index': input_index, 'Input Address': input_address}

        for name in item_to_scrape:

            
            scraped_item  = self.extract_content(driver, item_to_scrape[name])

            if (name == "Output Address") and (scraped_item is None):
                print("skipping this one")
                return
            #update the final result dict
            final_result_dict[name]= scraped_item
            print(f"The item is {name}, the value is {scraped_item}")

        natural_hazard_result_dict = run_natural_hazard(driver)
        final_result_dict.update(natural_hazard_result_dict)
        print(natural_hazard_result_dict)

        peak_age_group_result_dict  = run_age_gender(driver)
        final_result_dict.update(peak_age_group_result_dict)
        print(peak_age_group_result_dict['Peak Age Group'])
        print(peak_age_group_result_dict['Peak Age Group Percentage'])

        income_group_result_dict = run_income(driver)
        final_result_dict.update(income_group_result_dict)
        print(income_group_result_dict['Peak Income Group'])
        print(income_group_result_dict['Peak Income Group Percentage'])  
        
        owner_vs_renter_result_dict = run_owner_renter(driver) 
        final_result_dict.update(owner_vs_renter_result_dict)
        print(owner_vs_renter_result_dict['Owner vs Renter'])

        return final_result_dict


    def scrape_dat_shit(self):

        driver = self.setup_driver_with_existing_session()
        output_list = []

        unsuccessful_list = []

        for index, address in self.clean_df['Address'].items():
            print(f"Scraping {index}/{len(self.clean_df['Address'])}")
            sleep_time = random.uniform(5, 10.4)
            try:
                one_result_dict = self.scrape_one_address(driver, input_address=address, input_index=index)
                #print(one_result_dict)
            except Exception as e:
                print(f"An error occurred while scraping {address}: {str(e)}")
                unsuccessful_list.append({'Index': index, 'Address': address})
                continue
            
            output_list.append(one_result_dict)
            time.sleep(sleep_time)
        

        # remove None from output_list and unsuccessful list

        # Clean up output list 
        output_list = [item for item in output_list if item is not None]

        self.scraped_df = pd.DataFrame(output_list)
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d-%H%M%S")

        scraped_df_path_filename = "./processed_dataset"+f"/{self.uuid}_scraped_{timestamp}.xlsx"
        self.scraped_df.to_excel(scraped_df_path_filename, index=False)

        self.scraped_df_path = scraped_df_path_filename

        # Clean up unsuccessful list
        unsuccessful_list = [item for item in unsuccessful_list if item is not None]
        unsuccessful_df = pd.DataFrame(unsuccessful_list)
        unsuccessful_df_path_filename= "./processed_dataset"+f"/{self.uuid}_unsuccessful_{timestamp}.xlsx"
        unsuccessful_df.to_excel(unsuccessful_df_path_filename, index=False)

    def check_no_property_found(self, driver, dropdown_selector="body > div:nth-child(15) > ul > li"):
        """
        Check if the dropdown shows "No Property Found"

        Args:
            driver: The Selenium WebDriver instance
            dropdown_selector: The CSS selector for the dropdown results container

        Returns:
            bool: True if no property was found, False if property results exist
        """
        try:
            # Wait for dropdown to appear
            dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, dropdown_selector))
            )

            print(dropdown.text)
            
            # Check if "No Property Found" is in the dropdown
            if "No property found" in dropdown.text:
                print("No property found in search results")
                return True
            print("No property NOT found in search results")
            return False
                
        except TimeoutException:
            print("Dropdown results never appeared")
            return True
        except Exception as e:
            print(f"Unexpected error checking search results: {str(e)}")
            return True


item_to_scrape = {
'Output Address' : "#paddress > span.streetAddress",
#"Output Suburb" :"#paddress2 > span:nth-child(1)",
#"Output State" : "#paddress2 > span:nth-child(2)",
"Output Postcode" :"#paddress2 > span:nth-child(3)",
'Estimated Price' :"#propEstimatedPrice",
'Estimated Price Range': "#property-insights > div.panel > div.row > div.col-sm-6.col-sm-pull-6 > div:nth-child(1) > div.main-value-information > span:nth-child(6)",
'Cash Flow Score' : "#ss-collapse-1 > div > div:nth-child(2) > div > div > span.property-strategy-score-value",
'Capital Grow Score':"#ss-collapse-2 > div > div:nth-child(2) > div > div > span.property-strategy-score-value",
'Lower Risk Score' : "#ss-collapse-3 > div > div:nth-child(2) > div > div > span.property-strategy-score-value",
'Land Size' : "#property-insights > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(1) > table > tbody > tr:nth-child(4) > td:nth-child(2)",
'Floor Area': "#property-insights > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(1) > table > tbody > tr:nth-child(5) > td:nth-child(2)",
'Year Built': "#property-insights > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(2) > table > tbody > tr:nth-child(2) > td:nth-child(2)",
'Distance from CBD': "#property-insights > div:nth-child(3) > div:nth-child(8) > div > div.row > div:nth-child(1) > center > div:nth-child(1) > div > div > div > div",
"Mortgage Repayment": "#property-insights > div.panel > div.row > div.col-sm-6.col-sm-pull-6 > div:nth-child(1) > table > tbody > tr:nth-child(1) > td.data > span", 
"Estimated Rent":"#property-insights > div.panel > div.row > div.col-sm-6.col-sm-pull-6 > div:nth-child(1) > table > tbody > tr:nth-child(3) > td.data > div > span",
}




# if __name__ == "__main__":

#     scraper = Scraper(prepped_df=pd.DataFrame(), uuid = "TEST-UUID")
#     driver = scraper.setup_driver_with_existing_session()
#     # scraper.scrape_one_address(driver= driver, input_index = 1, input_address="1, 2, 4/30 Pollack Street, Colac")

#     #scraper.fill_search_box(driver, "#propertysearch", "1, 2, 4/30 Pollack Street, Colac")
#     #time.sleep(3)
#     #scraper.check_no_property_found(driver)
#     #scraper.check_search_success(driver, success_criteria_selector="#paddress > span.streetAddress")
#     print(scraper.scrape_one_address(driver= driver, input_index=3, input_address="52 Diplomat Crescent Cranbourne South VIC 3977"))






