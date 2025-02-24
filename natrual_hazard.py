from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains

import time


def click_hazard_trigger(driver, timeout=10):
    """
    Click the hazard trigger element using multiple approaches if needed
    
    Args:
        driver: Selenium webdriver instance
        timeout: Maximum time to wait for element
    """
    try:
        # Method 1: Standard click with explicit wait
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "hazard-trigger"))
        )
        element.click()
        return True
        
    except ElementClickInterceptedException:
        try:
            # Method 2: JavaScript click
            element = driver.find_element(By.ID, "hazard-trigger")
            driver.execute_script("arguments[0].click();", element)
            return True
            
        except Exception as e:
            try:
                # Method 3: ActionChains click
                actions = ActionChains(driver)
                element = driver.find_element(By.ID, "hazard-trigger")
                actions.move_to_element(element).click().perform()
                return True
                
            except Exception as e:
                try:
                    # Method 4: Try clicking with a small delay and scroll into view
                    element = driver.find_element(By.ID, "hazard-trigger")
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    time.sleep(0.5)  # Small delay after scroll
                    element.click()
                    return True
                    
                except Exception as e:
                    print(f"All click attempts failed: {str(e)}")
                    return False

def wait_for_trigger_state(driver, timeout=10):
    """
    Wait for the trigger element to be in the correct state before clicking
    
    Args:
        driver: Selenium webdriver instance
        timeout: Maximum time to wait
    """
    try:
        # Wait for element to be present
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "hazard-trigger"))
        )
        
        # Check if element is visible
        if not element.is_displayed():
            print("Trigger element is not visible")
            return False
            
        # Check if element is enabled
        if not element.is_enabled():
            print("Trigger element is not enabled")
            return False
            
        return True
        
    except Exception as e:
        print(f"Error checking trigger state: {str(e)}")
        return False

def click_show_risk_summary(driver):
    try:
        # Check trigger state first
        if wait_for_trigger_state(driver):
            # Try to click the trigger
            if click_hazard_trigger(driver):
                print("Successfully clicked hazard trigger")
                
                # Optional: Wait for any animations or changes after click
                time.sleep(1)
                
                # Optional: Verify the click worked (e.g., check if content is visible)
                try:
                    # Add your verification logic here
                    # For example, check if a certain element becomes visible
                    risk_summary = WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.ID, "risk-summary"))
                    )
                    print("Risk summary is now visible")
                except TimeoutException:
                    print("Risk summary did not become visible after click")
            else:
                print("Failed to click hazard trigger")
        else:
            print("Trigger is not in clickable state")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def extract_content(driver, selector):
    """Extract content from specified element"""
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        return element.text
    except TimeoutException:
        print(f"Element with selector {selector} not found")
        return None

def run_natural_hazard(driver):
    natural_hazard = {'Bushfire': '#natural-hazard > div:nth-child(3) > div.col-xs-4.col-sm-4 > span',
                      'Flood': '#natural-hazard > div:nth-child(4) > div.col-xs-4.col-sm-4 > span',
                      'Landslide':'#natural-hazard > div:nth-child(5) > div.col-xs-4.col-sm-4 > span',
                      'Coastal Risk Score': '#natural-hazard > div:nth-child(8) > div.col-xs-4.col-sm-4 > span',
                      'Coastal Erosion Risk':'#natural-hazard > div:nth-child(9) > div.col-xs-4.col-sm-4 > span',
                      'Storm Surge Risk':'#natural-hazard > div:nth-child(10) > div.col-xs-4.col-sm-4 > span',
                      }
    
    #click this botton
    click_show_risk_summary(driver)

    result_dict = {}
    #hazard-trigger
    for name in natural_hazard:
        scraped_item  = extract_content(driver, natural_hazard[name])
        print(f"The item is {name}, the value is {scraped_item}")
        result_dict[name] = scraped_item

    return result_dict
