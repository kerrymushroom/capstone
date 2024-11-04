import json
import re

# ==========================================================================================
# IMPORTANT: You need to use shell script to change all the data table name into lowercase.
# This code doesn't deal with it, use `lowercaseFileName.py`.
# ==========================================================================================

# Path to the JSON file
file_path = './visEval_single.json'

# Read the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

# Dictionary to store [key,table] pairs
table_ids = {}

# Find table name
for key, value in data.items():
    sql = value['vis_query']['data_part']['sql_part']
    table_name = ''
    try:
        table_name = re.search(r' from\s+(\w+)', sql, re.IGNORECASE).group(1)
    except IndexError:
        print(f"Error: {key}")
    table_ids[key] = table_name

# Modify the JSON data
for key, table_id in table_ids.items():
    if key in data:
        # Get the dictionary corresponding to the key
        entry = data[key]

        # Create a new dictionary with "table_id" inserted after "db_id"
        modified_entry = {}
        for k, v in entry.items():
            modified_entry[k] = v
            if k == "db_id":
                # Insert "table_id" immediately after "db_id"
                modified_entry["table_id"] = table_id

        # Update the entry in the main data dictionary
        data[key] = modified_entry

# Save the modified data back to the JSON file
with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)
