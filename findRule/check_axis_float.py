import matplotlib.pyplot as plt
import json
import os
import pandas as pd


def check_axis_is_float(jsonFile, target_key):
    if not os.path.exists(jsonFile):
        return False
    with open(jsonFile, 'r') as f:
        data = json.load(f)
    if target_key not in data:
        return False
    target_data = data[target_key]
    entry = target_data.get("0", {})
    code = entry['code']

    # local_env is the picture
    local_env = {"plt": plt, "pd": pd}
    try:
        exec(code, local_env)
        ax = local_env.get('ax')
        if not ax:
            return False
    except Exception as e:
        print(f"Error while executing code: {e}")
        return False

    x_labels = [label.get_text() for label in ax.get_xticklabels()]  # 获取 X 轴显示的刻度标签
    y_labels = [label.get_text() for label in ax.get_yticklabels()]  # 获取 Y 轴显示的刻度标签

    print(f"X axis labels: {x_labels}")
    print(f"Y axis labels: {y_labels}")

    # test is number for y_axis
    y_axis_result = all(is_number_label(y_label) for y_label in y_labels)
    # test is number for x_axis
    x_axis_result = all(is_number_label(x_label) for x_label in x_labels)

    if not (y_axis_result and x_axis_result):
        print("Failed validation: Non-integer axis labels was found.")
        return False
    plt.close()
    print("Passed validation.")
    return True

# if is not a number
def is_number_label(label):
    try:
        return float(label).is_integer()
    except ValueError:
        return True

jsonFile = "./formatted_testCase.json"
target_key = "942@x_name@DESC"  # target key
result = check_axis_is_float(jsonFile, target_key)
print("Validation Result:", result)
