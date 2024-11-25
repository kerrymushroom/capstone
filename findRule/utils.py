import io
from contextlib import redirect_stdout
import matplotlib
import re
import pandas as pd
import os

include = [r'\n(\w+)\.plot\(',r'\n(\w+)\.\w+\(.*?\)\.plot\(',r'=(\w+)\.plot\(',r'= (\w+)\.plot\(',r'\n(?:ax|plt)\.\w+\((\w+)[.[]{1}']
text = ""

# get the target dataframe string using re
def get_dataframe(text,include=include):
    res = ""
    for line in include:
        if  re.search(line, text):
            res = re.search(line, text).group(1)
            break
    local_vars = {}
    exec(text, {}, local_vars)
    return local_vars[res]

# return the last df 
def get_last_var(answer):
    local_vars = {}
    exec(answer, {}, local_vars)
    res = [x for x in list(local_vars.keys()) if x not in ['pd', 'plt', 'df','fig', 'ax']]
    return local_vars[res[-1]]

# this function is to suppress printing or plotting
def mask(func, *args, **kwargs):
    original_backend = matplotlib.get_backend()
    matplotlib.use('Agg')
    with io.StringIO() as buf, redirect_stdout(buf):
        return func(*args, **kwargs)
    matplotlib.use(original_backend)
    #matplotlib.use('module://matplotlib_inline.backend_inline')

def save_df_json(df):
    # convert non-numeric index class such as (pd.DatetimeIndex, pd.PeriodIndex,TimedeltaIndex,IntervalIndex) to string
    if not (isinstance(df.index, pd.Index) and df.index.dtype in ['int64', 'float64']):
        df.index = [str(idx) for idx in df.index]
    # if the index is integer number, then the index is not x_data, the first column is x_data, the rest columns are y_data
    if isinstance(df, pd.Series):
         # for Series object, only one dimention
        x_data = [df.index.tolist()]
        y_data = [df.values.tolist()]
    elif df.index[1]==1:
        x_data = [df[df.columns[0]].tolist()]
        y_data = [df[col].tolist() for col in df.columns[1:]] 
    else:
        # else, the index is x_data, all the columns is y_data
        x_data = [df.index.tolist()]
        y_data = [df[col].tolist() for col in df.columns[:]] 
    result_json = {
    'x_data': x_data,
    'y_data': y_data
    }
    return result_json

def create_folder(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        print("The path exists.")
    else:
        os.makedirs(file_path)
        print("The path will be created.")