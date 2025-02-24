from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
import time

### Age and gender

def extract_age_gender_data(driver, timeout=10):
    """
    Extract age and gender percentage data from the Highcharts chart
    
    Args:
        driver: Selenium webdriver instance
        timeout: Wait timeout in seconds
        
    Returns:
        dict: Dictionary containing the age categories and percentages for each group
    """
    try:
        # Wait for the chart container to be present
        chart_container = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "ageSexRatio_container"))
        )
        
        # Get the Highcharts data directly using JavaScript
        script = """
        var chart = $('#ageSexRatio_container').highcharts();
        return {
            categories: chart.xAxis[0].categories,
            series: chart.series.map(function(series) {
                return {
                    name: series.name,
                    data: series.data.map(function(point) {
                        return point.y;
                    })
                };
            })
        };
        """
        
        chart_data = driver.execute_script(script)
        
        # Format the data
        result = {
            'age_categories': chart_data['categories'],
            'data': {}
        }
        
        # Add percentage data for each series
        for series in chart_data['series']:
            result['data'][series['name']] = [round(x, 2) if x is not None else 0 for x in series['data']]
            
        return result

    except TimeoutException:
        print("Timeout waiting for chart to load")
        return None
    except Exception as e:
        print(f"Error extracting chart data: {str(e)}")
        return None

# Alternative method using element parsing if JavaScript method doesn't work
def extract_age_gender_data_backup(driver, timeout=10):
    """
    Backup method to extract data by parsing chart elements
    """
    try:
        # Wait for chart to be visible
        chart = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#ageSexRatio_container .highcharts-xaxis-labels"))
        )
        
        # Get age categories
        age_labels = driver.find_elements(By.CSS_SELECTOR, "#ageSexRatio_container .highcharts-xaxis-labels text")
        age_categories = [label.text for label in age_labels]
        
        # Get series names
        series_labels = driver.find_elements(By.CSS_SELECTOR, "#ageSexRatio_container .highcharts-legend-item text")
        series_names = [label.text for label in series_labels]
        
        # Get data columns
        columns = driver.find_elements(By.CSS_SELECTOR, "#ageSexRatio_container .highcharts-series rect")
        
        # Calculate height percentages (this is approximate and may need adjustment)
        chart_height = float(driver.find_element(By.CSS_SELECTOR, "#ageSexRatio_container .highcharts-plot-background").get_attribute("height"))
        
        result = {
            'age_categories': age_categories,
            'data': {}
        }
        
        # Initialize data structure
        for series in series_names:
            result['data'][series] = []
        
        # This part would need customization based on the exact chart structure
        # As the height-to-percentage conversion needs specific chart parameters
        
        return result
        
    except Exception as e:
        print(f"Error in backup extraction method: {str(e)}")
        return None

# def print_chart_data(data):
#     """
#     Print the extracted chart data in a readable format
#     """
#     if not data:
#         print("No data to display")
#         return
        
#     print("\nAge and Gender Distribution:")
#     print("-" * 50)
    
#     # Print header
#     headers = ["Age"] + list(data['data'].keys())
#     print("{:<10}".format("Age"), end="")
#     for header in headers[1:]:
#         print("{:<25}".format(header), end="")
#     print("\n" + "-" * (10 + 25 * len(data['data'])))
    
#     # Print data rows
#     for i, age in enumerate(data['age_categories']):
#         print("{:<10}".format(age), end="")
#         for series_name in data['data']:
#             print("{:<25.2f}".format(data['data'][series_name][i]), end="")
#         print()

def analyze_peak_age_group(chart_data):
    """
    Analyze which age group has the highest total population
    
    Args:
        chart_data: Dictionary containing the chart data
        
    Returns:
        tuple: (age_group, total_percentage, breakdown)
    """
    try:
        age_categories = chart_data['age_categories']


        data = chart_data['data']
        data = {key: value for key, value in data.items() if "Council" not in key}

        
        # Initialize dictionary to store combined percentages for each age group
        age_totals = {}
        
        # Calculate total for each age group
        for i, age in enumerate(age_categories):
            total = 0
            breakdown = {}
            
            # Sum up percentages from all groups for this age
            for group_name, percentages in data.items():
                value = percentages[i]
                total += value
                breakdown[group_name] = value
                
            age_totals[age] = {
                'total': round(total, 2),
                'breakdown': breakdown
            }
        
        # Find the age group with highest percentage
        peak_age = max(age_totals.items(), key=lambda x: x[1]['total'])
        
        return {
            'Peak Age Group': peak_age[0],
            'Peak Age Group Percentage': peak_age[1]['total'],
            #'breakdown': peak_age[1]['breakdown']
        }

    except Exception as e:
        print(f"Error analyzing peak age group: {str(e)}")
        return None

# returns the peak age group
def run_age_gender(driver):
    try:
        # Extract data
        chart_data = extract_age_gender_data(driver)
        
        if not chart_data:
            print("Trying backup method...")
            chart_data = extract_age_gender_data_backup(driver)
        
        if chart_data:
            return analyze_peak_age_group(chart_data)

                
    except Exception as e:
        print(f"An error occurred: {str(e)}")

