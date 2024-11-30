import ast
import json
import re


def detect_plot_type(code_string):
    plot_types = {
        'plot': 'line',
        'bar': 'bar',
        'barh': 'barh',
        'hist': 'hist',
        'box': 'box',
        'scatter': 'scatter',
        'pie': 'pie',
    }

    try:
        tree = ast.parse(code_string)

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr
                    if func_name in plot_types:
                        for keyword in node.keywords:
                            if keyword.arg == 'kind':
                                return keyword.value.s
                        return plot_types[func_name]
    except Exception as e:
        print(f"Error parsing code: {e}")

    return "Unknown"


def check_stacked_in_code(code_string):
    pattern = r'stacked\s*=\s*True'
    if re.search(pattern, code_string):
        return True
    else:
        return False


def eval_type_check(question_serial, question_index, answer):
    with open('./data.json', 'r') as file:
        data = json.load(file)
        standard_type = data[question_serial]['vis_obj']['chart']
        chart_type = detect_plot_type(answer)
        if standard_type == chart_type:
            if standard_type == 'bar':
                try:
                    # For stacked bar chart.
                    if data[question_serial]["query_meta"][int(question_index)]["stacked_bar"]:
                        if check_stacked_in_code(answer):
                            return 1  # Stacked bar chart
                        else:
                            return 0.5  # Failed to stack

                    # For non-stacked bar chart.
                    if not data[question_serial]["query_meta"][int(question_index)]["stacked_bar"]:
                        if not check_stacked_in_code(answer):
                            return 1    # Non-stacked bar chart
                        else:
                            return 0.5  # Stacked bar chart
                except KeyError:
                    return -1
            return 1
        else:
            return 0
