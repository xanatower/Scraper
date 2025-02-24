
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains



def extract_household_income_data(driver):
    """
    Extract household income data from Highcharts
    
    Args:
        driver: Selenium webdriver instance
    
    Returns:
        dict: Dictionary containing income categories and percentages
    """
    try:
        script = """
        var chart = $('#income_container').highcharts();
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
        
        result = {
            'income_categories': chart_data['categories'],
            'data': {}
        }
        
        for series in chart_data['series']:
            result['data'][series['name'].strip()] = [round(x, 2) if x is not None else 0 for x in series['data']]
            
        return result
        
    except Exception as e:
        print(f"Error extracting income data: {str(e)}")
        return None

def analyze_peak_income_group(chart_data):
    """
    Analyze which income group has the highest percentage
    
    Args:
        chart_data: Dictionary containing the chart data
    
    Returns:
        dict: Analysis results
    """
    try:
        income_categories = chart_data['income_categories']
        data = chart_data['data']
        #remove the council data
        data = {key: value for key, value in data.items() if "Council" not in key}
        
        income_totals = {}
        
        for i, income in enumerate(income_categories):
            try:
                total = 0
                breakdown = {}
                
                for group_name, percentages in data.items():
                    value = percentages[i]
                    total += value
                    breakdown[group_name] = value
                    
                income_totals[income] = {
                    'total': round(total, 2),
                    'breakdown': breakdown
                }
            except Exception as e:
                print(f"Error processing income group {income}: {str(e)}")
                continue
        
        peak_income = max(income_totals.items(), key=lambda x: x[1]['total'])
        
        return {
            'Peak Income Group': peak_income[0],
            'Peak Income Group Percentage': peak_income[1]['total'],
            #'breakdown': peak_income[1]['breakdown']
        }
    except Exception as e:
        print(f"Error analyzing peak income group: {str(e)}")
        return None

def print_income_analysis(analysis_result):
    """
    Print the income analysis in a readable format
    """
    try:
        if not analysis_result:
            print("No analysis data available")
            return
            
        print("\nPeak Income Group Analysis:")
        print("-" * 50)
        print(f"Income Range: {analysis_result['peak_income_group']}")
        print(f"Total Percentage: {analysis_result['total_percentage']}%")
        print("\nBreakdown:")
        for group, percentage in analysis_result['breakdown'].items():
            print(f"  {group}: {percentage}%")
    except Exception as e:
        print(f"Error printing analysis: {str(e)}")

def analyze_all_income_groups(chart_data):
    """
    Analyze all income groups sorted by total percentage
    """
    try:
        income_categories = chart_data['income_categories']
        data = chart_data['data']
        
        income_totals = {}
        for i, income in enumerate(income_categories):
            try:
                total = 0
                breakdown = {}
                
                for group_name, percentages in data.items():
                    value = percentages[i]
                    total += value
                    breakdown[group_name] = value
                    
                income_totals[income] = {
                    'total': round(total, 2),
                    'breakdown': breakdown
                }
            except Exception as e:
                print(f"Error processing income group {income}: {str(e)}")
                continue
        
        sorted_incomes = sorted(
            income_totals.items(), 
            key=lambda x: x[1]['total'], 
            reverse=True
        )
        
        return [
            {
                'income_group': income,
                'total_percentage': data['total'],
                'breakdown': data['breakdown']
            }
            for income, data in sorted_incomes
        ]
    except Exception as e:
        print(f"Error analyzing all income groups: {str(e)}")
        return None

def print_all_income_groups(analysis_results):
    """
    Print all income groups sorted by percentage
    """
    try:
        print("\nIncome Groups Analysis (Sorted by Percentage):")
        print("-" * 50)
        
        for i, result in enumerate(analysis_results, 1):
            try:
                print(f"\n{i}. Income Range: {result['income_group']}")
                print(f"   Total Percentage: {result['total_percentage']}%")
                print("   Breakdown:")
                for group, percentage in result['breakdown'].items():
                    print(f"     {group}: {percentage}%")
            except Exception as e:
                print(f"Error printing result {i}: {str(e)}")
                continue
    except Exception as e:
        print(f"Error printing income groups: {str(e)}")

def run_income(driver):

    # Extract data
    income_data = extract_household_income_data(driver)
    
    if income_data:
        try:
            # Find peak income group
            peak_analysis = analyze_peak_income_group(income_data)

            
            #print_income_analysis(peak_analysis)
            return peak_analysis
            
            # # Analyze all income groups
            # all_groups = analyze_all_income_groups(income_data)
            # print_all_income_groups(all_groups)

        except Exception as e:
            print(f"Error in analysis: {str(e)}")


