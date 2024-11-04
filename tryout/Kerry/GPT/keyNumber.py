# Path to the JSON file
import json

file_path = 'test/formatted_testCase.json'

# Read the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

num = 0

for key, value in data.items():
    num = num + 1

print(num)