
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains


def extract_occupancy_data(driver):
    """
    Extract occupancy data from the Highcharts pie chart
    
    Args:
        driver: Selenium webdriver instance
    
    Returns:
        dict: Dictionary containing categories and their percentages
    """
    try:
        # Extract data using JavaScript
        script = """
        var chart = $('#occupancy_container').highcharts();
        return chart.series[0].data.map(function(point) {
            return {
                category: point.name,
                percentage: point.y
            };
        });
        """
        
        chart_data = driver.execute_script(script)
        
        # Format the data into a dictionary
        occupancy_data = {}
        for item in chart_data:
            occupancy_data[item['category']] = round(item['percentage'], 2)
            
        return occupancy_data
        
    except Exception as e:
        print(f"Error extracting occupancy data: {str(e)}")
        return None

def print_occupancy_data(data):
    """
    Print the occupancy data in a readable format
    """
    try:
        if not data:
            print("No occupancy data available")
            return
            
        print("\nOccupancy Categories:")
        print("-" * 40)
        
        # Sort by percentage in descending order
        sorted_categories = sorted(data.items(), key=lambda x: x[1], reverse=True)
        
        for category, percentage in sorted_categories:
            print(f"{category}: {percentage}%")
            
    except Exception as e:
        print(f"Error printing occupancy data: {str(e)}")

def owner_vs_renter(data):
    try:
        if not data:
            print("No occupancy data available")
            return
        
        owner = data['Purchaser'] + data['Owns Outright']
        renter = data['Renting']
        
        renter = renter
        #type 
        return {'Owner vs Renter': str(owner)+"/"+str(renter)}

    except Exception as e:
        print(f"Error printing occupancy data: {str(e)}")



def run_owner_renter(driver):
    try:
        
        # Extract occupancy data
        occupancy_data = extract_occupancy_data(driver)
        
        if occupancy_data:
            # Print the data
            return owner_vs_renter(occupancy_data)
            

                
    except Exception as e:
        print(f"Error in main: {str(e)}")