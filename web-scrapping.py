import requests
import json

# Initialize an empty list to store all the products
all_products = []

# Define the category and the number of pages for each category
categories = {
    # "otc-medicine": 290,
    # "womens-choice": 4,
    # "sexual-wellness": 6,
    # "diabetic-care": 3,
    # "baby-care": 5,
    # "dental-care": 2,
    # "supplement": 2,
    # "diapers": 5,
    # "personal-care": 6,
    # "devices": 2,
    "prescription-medicine": 1075
}
# https://medeasy.health/_next/data/WzarUBZ0M7ekq86WXo6ov/en/category/otc-medicine.json?page=2&slug=otc-medicine
# https://medeasy.health/_next/data/WzarUBZ0M7ekq86WXo6ov/en/category/womens-choice.json?page=2&slug=womens-choice
# https://medeasy.health/_next/data/WzarUBZ0M7ekq86WXo6ov/en/category/sexual-wellness.json?page=2&slug=sexual-wellness
# https://medeasy.health/_next/data/WzarUBZ0M7ekq86WXo6ov/en/category/{category_name}.json?page={page+1}&slug={category_name}

# Loop through each category
for category_name, total_pages in categories.items():
    for page in range(total_pages):
        # Build the URL for the current page
        url = f"https://medeasy.health/_next/data/WzarUBZ0M7ekq86WXo6ov/en/category/{category_name}.json?page={page+1}&slug={category_name}"
        
        # Send a GET request to fetch the data
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Extract the 'products' array from the response
            products = data['pageProps']['products']
            
            # Append the products to the all_products list
            all_products.extend(products)
            
            print(f"Page {page+1} products for {category_name} fetched successfully.")
        else:
            print(f"Failed to fetch data for page {page+1} of {category_name}. Status code: {response.status_code}")

    # Save the combined products for the category to a new JSON file
    with open(f'{category_name}-all.json', 'w') as outfile:
        json.dump(all_products, outfile, indent=4)

    print(f"All products for {category_name} have been saved to '{category_name}-all.json'.")
