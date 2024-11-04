import json

file_path = './formatted_testCase.json'

# with open(file_path, 'r') as file:
#     data = file.read().splitlines()

# formatted_data = {}
# for line in data:
#     key, value = line.split(':')
#     formatted_data[str(key)] = {"hardness": value}

# with open('formatted_testCase.json', 'w') as file:
#     json.dump(formatted_data, file, indent=4)

with open(file_path, 'r') as file:
    data = json.load(file)

formatted_data = {}
for key, value in data.items():

    formatted_data[key] = {
        "hardness": value["hardness"],
        "result": None,
        "code": None,
        "zeroshot": None
    }


with open('formatted_testCase.json', 'w') as file:
    json.dump(formatted_data, file, indent=4)
