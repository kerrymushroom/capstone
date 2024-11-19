import io
from contextlib import redirect_stdout
import matplotlib
import re

include = [r'\n(\w+)\.plot\(','\n(\w+)\.\w+\(.*?\)\.plot\(',r'\n(?:ax|plt)\.\w+\((\w+)[.[]{1}']
text = ""

# get the target dataframe string
def get_dataframe(text,include=include):
    res = ""
    for line in include:
        if  re.search(line, text):
            res = re.search(line, text).group(1)
            break
    return res

# this function is to suppress printing or plotting
def mask(func, *args, **kwargs):
    original_backend = matplotlib.get_backend()
    matplotlib.use('Agg')
    with io.StringIO() as buf, redirect_stdout(buf):
        return func(*args, **kwargs)
    matplotlib.use(original_backend)