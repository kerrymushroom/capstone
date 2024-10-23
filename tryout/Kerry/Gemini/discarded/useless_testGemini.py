import enum

import google.generativeai as genai
import pandas as pd
import tempfile
from typing import TypedDict, Optional, Union, List

question = "Average MPG by origin."
model = genai.GenerativeModel("gemini-1.5-flash")
url = "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/cars.csv"

genai.configure(api_key="AIzaSyCLXMk4PNMrGXu3ltiB930Y2bq4h0gE6OY")


class CType(enum.Enum):
    bar = "bar"
    circle = "circle"
    line = "line"
    area = "area"
    point = "point"
    rect = "rect"
    rule = "rule"
    square = "square"
    text = "text"
    tick = "tick"
    trail = "trail"
    boxplot = "boxplot"
    errorbar = "errorbar"
    erroband = "errorband"


class DataSchema(TypedDict):
    field: str
    type: str
    # ... 其他属性，如 aggregate, bin, scale 等


class Encoding(TypedDict):
    x: Optional[DataSchema]
    y: Optional[DataSchema]
    color: Optional[DataSchema]
    # ... 其他编码通道


class Recipe(TypedDict):
    # "$schema": "https://vega.github.io/schema/vega-lite/v5.json"
    description: str
    data: Union[List, dict, str]  # 支持 list, dict, URL
    mark: str  # 默认使用柱状图
    encoding: Encoding


def read_csv(original_csv):
    # Write the original CSV data to a temporary file
    csv = pd.read_csv(original_csv)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
        csv.to_csv(temp_file, index=False)
        temp_file.seek(0)  # Read from the beginning
        print(f"File name：{temp_file.name}")
        return temp_file


def chart_type(ori_question, csv_data):
    fi_question = ori_question + 'I want to show a chart, What type of chart should I use?'
    return model.generate_content([fi_question, csv_data], generation_config=genai.GenerationConfig(
        response_mime_type="text/x.enum", response_schema=CType))


uploadFile = genai.upload_file(read_csv(url).name)
chart_type_chosen = chart_type(question, uploadFile)

# response = model.generate_content(["Average MPG by origin.", uploadFile],
#                                   generation_config=genai.GenerationConfig(
#                                       response_mime_type='application/json', response_schema=C_type
#                                   ))
print(response.text)
