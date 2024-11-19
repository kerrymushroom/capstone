from gptTest import run_visEval
from utils import get_dataframe, mask
import json
from datetime import datetime

rules = ["only use .dt accessor with datetimelike values"]
key = "" # add your gpt key here

def date_type(date_string):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if date_string in weekdays:
        return "WEEKDAY"

    if date_string.isdigit() and 1 <= len(date_string) <= 4:
        return "YEAR"

    for fmt in ("%B", "%b"):  
        try:
            datetime.strptime(date_string, fmt)
            return "MONTH"
        except ValueError:
            continue

    return "Unknown"

def checkDates(eva_id):
	# specify the path of your data.file
    with open('data.json', 'r') as file:
        data = json.load(file)

    # run_visEval would return answer string
    answer = run_visEval(eva_id,rules, 0, key)
    local_vars = {}
    exec(answer, {}, local_vars)
    df = local_vars[get_dataframe(answer)]    

    binning = data[eva_id]["vis_query"]["data_part"]["binning"].split(' ')[-1]
    return binning==date_type(str(df.index[0]))

# getDatesResult will return True or False, True means dates formats on x-axis are correct
def getDatesResult(eva_id):
	return mask(checkDates,eva_id)