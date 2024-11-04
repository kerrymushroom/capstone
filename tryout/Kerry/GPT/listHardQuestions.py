import json

file_path = "./visEval_dataset/visEval_single.json"

with open(file_path, 'r') as file:
    data = json.load(file)

for key, value in data.items():
    if 'Hard' in value['hardness']:
        print(key + ':' + value['hardness'] + '  ')
