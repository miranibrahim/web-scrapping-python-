import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Function to fetch data from a page using Selenium
def fetch_data_from_page(page_number):
    url = f'https://medeasy.health/category/otc-medicine?page={page_number}'
    
    # Set up Selenium WebDriver with Chrome
    options = Options()
    options.headless = True  # Run in headless mode (no browser UI)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    # Wait for the page to load
    time.sleep(1)  # Adjust sleep time if necessary to ensure the page is fully loaded
    
    html_content = driver.page_source
    driver.quit()
    
    return html_content

# Function to extract JSON data from the page's HTML
def extract_json_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tag = soup.find('script', {'id': 'product-view-OTC Medicine'})
    if script_tag:
        json_data = script_tag.string.strip()
        # Extract the JSON-like part of the script (between the curly braces)
        start_index = json_data.find("{")
        end_index = json_data.rfind("}") + 1
        json_str = json_data[start_index:end_index]
        
        # Clean up the string: remove any unnecessary parts before the JSON data
        json_str = json_str.replace("event: \"view_item_list\",", "")
        
        # Replace single quotes with double quotes for valid JSON format
        json_str = json_str.replace("'", '"')

        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            print(f"Error decoding JSON for page content: {json_str}")
            return None
    else:
        print("No JSON data found")
        return None

# Function to save data as JSON and Excel
def save_data_to_files(data, json_filename, excel_filename):
    # Save JSON data
    with open(json_filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    # Convert the data to a pandas DataFrame and save as Excel
    items = data['ecommerce']['items']
    df = pd.DataFrame(items)
    df.to_excel(excel_filename, index=False)

# Main script loop
def main():
    all_items = []
    for page in range(81, 82):
        print(f"Fetching data from page {page}...")
        html_content = fetch_data_from_page(page)
        if html_content:
            data = extract_json_data(html_content)
            if data:
                all_items.extend(data['ecommerce']['items'])

    # Save all fetched data
    save_data_to_files({'ecommerce': {'items': all_items}}, 'medicines_data.json', 'medicines_data.xlsx')
    print("Data saved to medicines_data.json and medicines_data.xlsx")

if __name__ == "__main__":
    main()
