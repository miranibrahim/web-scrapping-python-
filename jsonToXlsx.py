import pandas as pd
import json

# Load JSON data from a file
with open('womens-choice-all.json', 'r') as json_file:
    json_data = json.load(json_file)

# Prepare a list to store the processed data
processed_data = []

# Iterate through the data
for item in json_data:
    # Base fields
    base_data = {
        "id": item["id"],
        "medicine_name": item["medicine_name"],
        "category_name": item["category_name"],
        "slug": item["slug"],
        "generic_name": item["generic_name"],
        "strength": item["strength"],
        "manufacturer_name": item["manufacturer_name"],
        "discount_value": f"{item['discount_value']}%",  # Concatenate discount value with '%'
        "is_discountable": item["is_discountable"],
        "is_available": item["is_available"],
        "medicine_image": item["medicine_image"],
        "rx_required": item["rx_required"]
    }
    
    # Combine all unit prices into a single string with conditions
    unit_prices_str = "\n".join(
        f"{price['unit']}-{price['price']} BDT" if price['unit'][0].isdigit() 
        else f"{price['unit_size']} {price['unit']} - {price['price']} BDT"
        for price in item["unit_prices"]
    )
    
    # Add the unit price string to the base data
    base_data["unit_price"] = unit_prices_str
    
    # Append the processed row
    processed_data.append(base_data)

# Convert the processed data to a pandas DataFrame
df = pd.DataFrame(processed_data)

# Save the DataFrame to an Excel file
df.to_excel('womens-choice-all.xlsx', index=False, engine='openpyxl')

print("JSON data has been successfully converted to data_with_unit_prices.xlsx")
