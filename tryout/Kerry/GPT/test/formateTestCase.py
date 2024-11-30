import json

file_path = './formatted_testCase.json'
ori_path = '../data.json'

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

with open(ori_path, 'r') as file1:
    oriData = json.load(file1)

count = 0

formatted_data = {}
for key, value in data.items():
    belong = ''
    count += 1
    if count < 23:
        belong = 'Kerry'
    elif count <= 43:
        belong = "Dewei"
    elif count <= 63:
        belong = "Lina"
    elif count <= 83:
        belong = "Zihuan"
    elif count <= 103:
        belong = "Jing"

    formatted_data[key] = {
        "0": {
            "belong": belong,
            "question": value["0"]["question"],
            "hardness": value["0"]["hardness"],
            "isDataCorrect": value["0"]["isDataCorrect"],
            "isStyleCorrect": value["0"]["isStyleCorrect"],
            "evaluation": value["0"]["evaluation"],
            "code": value["0"]["code"],
            "addRule": value["0"]["addRule"],
            "addExample": value["0"]["addExample"],
        }
    }


with open('formatted_testCase.json', 'w') as file:
    json.dump(formatted_data, file, indent=4)
