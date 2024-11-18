import re

include = [r'\n(\w+).plot\(',r'\n(?:ax|plt).\w+.(\w+)[.[]{1}']
text = ""

# get the target dataframe string
def get_dataframe(text,include=include):
    res = ""
    for line in include:
        if  re.search(line, text):
            res = re.search(line, text).group(1)
            break
    return res