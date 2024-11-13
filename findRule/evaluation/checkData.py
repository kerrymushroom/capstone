import json
import re
import pandas as pd


def eval_data_check(question_serial, question_index, answer):
    with open('./data.json', 'r') as file:
        data = json.load(file)
        check_range = data[question_serial]["query_meta"][int(question_index)]["channel_specified"]
        check_classify = False

        if any(element == "classify" for element in check_range):
            check_classify = True
            standard_series = data[question_serial]["vis_obj"]["classify"]

        standard_x = data[question_serial]["vis_obj"]["x_data"]
        standard_y = data[question_serial]["vis_obj"]["y_data"]




    match = re.search(r"(\w+)\s*\.plot\(", answer)
    exec(answer)
    print(answer)

    if match:
        answer_df = eval(match.group(1))

        print(answer_df)
        answer_x = answer_df.index.tolist()
        if check_classify is True:
            answer_series = answer_df.columns.tolist()
        answer_y = answer_df.values

        if check_classify is True:
            if not are_lists_equal(standard_series, answer_series):
                print('standard_series:', standard_series)
                print('answer_series:', answer_series)
                return 0

        if not are_lists_equal(standard_x, answer_x):
            print('standard_x:', standard_x)
            print('answer_x:', answer_x)
            return 0

        if not are_lists_equal(standard_y, answer_y):
            print('standard_y:', standard_y)
            print('answer_y:', answer_y)
            return 0
        return 1

    else:
        return -1


def are_lists_equal(list1, list2):

    if len(list1) != len(list2):
        return False

    list1 = sorted(list1, key=str)
    list2 = sorted(list2, key=str)

    for item1, item2 in zip(list1, list2):
        if isinstance(item1, pd.Period) or isinstance(item2, pd.Period):
            continue

        if isinstance(item1, list) and isinstance(item2, list):

            if not are_lists_equal(item1, item2):
                return False
        elif isinstance(item1, str) and isinstance(item2, str):

            if item1.lower() != item2.lower():
                return False
        elif isinstance(item1, (int, float)) and isinstance(item2, (int, float)):

            if abs(item1 - item2) > 0.1:
                return False
        else:

            if item1 != item2:
                return False

    return True