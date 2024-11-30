import json
import re
from datetime import datetime

import numpy as np
import pandas as pd
from numpy import ndarray
from numpy.random import standard_t


def eval_data_check(question_serial, question_index, answer):
    with open('./data.json', 'r') as file:
        data = json.load(file)
        check_range = data[question_serial]["query_meta"][int(question_index)]["channel_specified"]
        check_classify = False
        binning = data[question_serial]["vis_query"]["data_part"]["binning"].split(' ')[-1]

        standard_list = []
        standard_x = data[question_serial]["vis_obj"]["x_data"]
        standard_list.extend(standard_x)

        if any(element == "classify" for element in check_range):
            if data[question_serial]["vis_obj"]["classify"] is not None:
                check_classify = True
                standard_series = data[question_serial]["vis_obj"]["classify"]
                standard_list.extend(standard_series)

        standard_y = data[question_serial]["vis_obj"]["y_data"]
        standard_list.extend(standard_y)




    match = re.search(r"(\w+)\s*\.plot\(", answer)
    exec(answer)
    print(answer)

    if match:
        answer_df = eval(match.group(1))

        print(answer_df)

        answer_list=[]
        if isinstance(answer_df, pd.DataFrame):
            answer_x = answer_df.index.tolist()
            answer_list.extend(answer_x)
            if check_classify is True:
                answer_series = answer_df.columns.tolist()
                answer_list.extend(answer_series)
            answer_y = answer_df.values
            answer_list.extend(answer_y)


            # if check_classify is True:
            #     if not are_lists_equal(standard_series, answer_series):
            #         print('standard_series:', standard_series)
            #         print('answer_series:', answer_series)
            #         return 0

            # if not are_lists_equal(standard_x, answer_x):
            #     print('standard_x:', standard_x)
            #     print('answer_x:', answer_x)
            #     return 0

            if not are_lists_equal(standard_list, answer_list, binning):
                # print('standard_list:', standard_list)
                # print('answer_list:', answer_list)
                return 0
            return 1

        elif isinstance(answer_df, pd.Series):
            answer_list = answer_df.index.tolist() + answer_df.tolist()

            if not are_lists_equal(standard_list, answer_list, binning):
                # print('standard_list:', standard_list)
                # print('answer_list:', answer_list)
                return 0
            return 1
        else:
            try:
                match = re.search(r"\.plot\((.*?)\)", answer)
                if match:
                    content = match.group(1)
                    variables = re.findall(r"[\w\.]+\[.*?\]", content)
                    print("Extracted variables:", variables)
                    variables = flatten_list([variables])

                    # Multiple data series
                    # if len(variables) > 2:
                    answer_list = []
                    for var in variables:
                        answer_list.extend(eval(var))
                    standard_x.extend(standard_y)
                    if not are_lists_equal(standard_x, answer_list, binning):
                        # print('standard_list:', standard_x)
                        # print('answer_list:', answer_list)
                        return 0
                    else:
                        return 1
                else:
                    return -1
            except Exception as e:
                print(e)
                return -1
    else:
        match = re.findall(r"ax\.[a-zA-Z]+\(([^\'\"].*?)\)", answer)
        if match:
            answer_list = []
            for content in match:
                variables = re.findall(r'(?:^|,)\s*(\b(?![\d])\w+\b)(?![^,]*=)', content)
                for var in variables:
                    answer_list.extend(eval(var))
            if not are_lists_equal(standard_list, answer_list, binning):
                print('standard_list:', standard_list)
                print('answer_list:', answer_list)
                return 0
            return 1
    return -1


def are_lists_equal(list1, list2, binning):

    if isinstance(list1, pd.DataFrame):
        list1 = list1.astype(str).values.tolist()

    if isinstance(list2, pd.DataFrame):
        list2 = list2.astype(str).values.tolist()

    list1 = flatten_list(list1)
    list2 = flatten_list(list2)

    if binning:
        for i, item in enumerate(list1):
            list1[i] = convert_to_timestamp(item, binning)

        for i, item in enumerate(list2):
            list2[i] = convert_to_timestamp(item, binning)


    if len(list1) != len(list2):
        return False

    list1 = sorted(list1, key=str)
    list2 = sorted(list2, key=str)

    print(list1)
    print(list2)

    for item1, item2 in zip(list1, list2):
        if isinstance(item1, str) and isinstance(item2, str):
            if item1.lower() != item2.lower():
                return False
        elif isinstance(item1, (int, float)) or isinstance(item2, (int, float)):
            if abs(float(item1) - float(item2)) > 0.1:
                return False
        else:
            if str(item1) != str(item2):
                return False
    return True

def flatten_list(nested_list):
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        elif isinstance(item, ndarray):
            flat_list.extend(flatten_list(item.tolist()))
        else:
            if (item==0) or (item is ("" or "nan" or '0' or '0.0' or None)) or (item != item):
                continue
            flat_list.append(item)
    return flat_list


def convert_to_timestamp(value, binning):
    if isinstance(value, (datetime, pd.Timestamp)):
        if binning == "MONTH":
            return value.month
        elif binning == "WEEKDAY":
            return value.weekday()
        elif binning == "YEAR":
            return value.year
        else:
            return value.timestamp()
    elif isinstance(value, pd.Period):
        if binning == "MONTH":
            return value.month
        elif binning == "WEEKDAY":
            return value.to_timestamp().weekday()
        elif binning == "YEAR":
            return value.year
        else:
            return value.to_timestamp().timestamp()
    elif isinstance(value, str):

        try:
            value = pd.to_datetime(value)

            if binning == "MONTH":
                return value.month
            elif binning == "WEEKDAY":
                return value.weekday()
            elif binning == "YEAR":
                return value.year
            else:
                return value.timestamp()
        except Exception:
            return convertDateStr(value)
    elif isinstance(value, (int, float)):
        return float(value)
    else:
        return value

def convertDateStr(value):
    if re.search(r'\b(January|Jan)\b', value, re.IGNORECASE):
        return 1
    if re.search(r'\b(February|Feb)\b', value, re.IGNORECASE):
        return 2
    if re.search(r'\b(March|Mar)\b', value, re.IGNORECASE):
        return 3
    if re.search(r'\b(April|Apr)\b', value, re.IGNORECASE):
        return 4
    if re.search(r'\b(May)\b', value, re.IGNORECASE):
        return 5
    if re.search(r'\b(June|Jun)\b', value, re.IGNORECASE):
        return 6
    if re.search(r'\b(July|Jul)\b', value, re.IGNORECASE):
        return 7
    if re.search(r'\b(August|Aug)\b', value, re.IGNORECASE):
        return 8
    if re.search(r'\b(September|Sep)\b', value, re.IGNORECASE):
        return 9
    if re.search(r'\b(October|Oct)\b', value, re.IGNORECASE):
        return 10
    if re.search(r'\b(November|Nov)\b', value, re.IGNORECASE):
        return 11
    if re.search(r'\b(December|Dec)\b', value, re.IGNORECASE):
        return 12
    if re.search(r'\b(Mon.*)\b', value, re.IGNORECASE):
        return 'Mon'
    if re.search(r'\b(Tue.*)\b', value, re.IGNORECASE):
        return 'Tue'
    if re.search(r'\b(Wed.*)\b', value, re.IGNORECASE):
        return 'Wed'
    if re.search(r'\b(Thu.*)\b', value, re.IGNORECASE):
        return 'Thu'
    if re.search(r'\b(Fri.*)\b', value, re.IGNORECASE):
        return 'Fri'
    if re.search(r'\b(Sat.*)\b', value, re.IGNORECASE):
        return 'Sat'
    if re.search(r'\b(Sun.*)\b', value, re.IGNORECASE):
        return 'Sun'
    return value
