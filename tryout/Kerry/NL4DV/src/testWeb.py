import streamlit as st
import pandas as pd

dt = {"query": "show average MPG of different Origin", "query_raw": "show average MPG of different Origin",
      "dataset": "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/cars.csv", "visList": [
        {"attributes": ["MPG", "Origin"], "queryPhrase": ["average", "MPG", "Origin"], "visType": "None",
         "tasks": ["derived_value"], "inferenceType": "explicit",
         "vlSpec": {"$schema": "https://vega.github.io/schema/vega-lite/v4.json",
                    "data": {"url": "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/cars.csv"}, "mark": "bar",
                    "encoding": {"x": {"field": "Origin", "type": "nominal"},
                                 "y": {"aggregate": "mean", "field": "MPG", "type": "quantitative"}}}}],
      "attributeMap": {"MPG": {"name": "MPG", "queryPhrase": ["MPG"], "encode": True},
                       "Origin": {"name": "Origin", "queryPhrase": ["Origin"], "encode": True}}, "taskMap": {
        "derived_value": [
            {"task": "derived_value", "queryPhrase": ["average", "MPG"], "values": [], "attributes": ["MPG"],
             "operator": "AVG", "inferenceType": "explicit"}]}, "visType": "None", "visQueryPhrase": "None",
      "dialogId": "0", "queryId": "0"}

dt2 = {'query_raw': 'show average MPG of different Origin', 'query': 'show average mpg of different origin',
       'dataset': 'https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/cars.csv', 'alias': None, 'visList': [
        {'attributes': ['MPG', 'Origin'], 'queryPhrase': None, 'visType': None, 'tasks': ['derived_value'],
         'inferenceType': 'implicit', 'vlSpec': {'$schema': 'https://vega.github.io/schema/vega-lite/v4.json',
                                                 'mark': {'type': 'bar', 'tooltip': True}, 'encoding': {
                'y': {'field': 'MPG', 'type': 'quantitative', 'aggregate': 'mean', 'axis': {'format': 's'}},
                'x': {'field': 'Origin', 'type': 'nominal'}}, 'transform': [],
                                                 'data': {'url': 'https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/cars.csv', 'format': {'type': 'csv'}}}}],
       'attributeMap': {
           'MPG': {'name': 'MPG', 'queryPhrase': ['mpg'], 'inferenceType': 'explicit', 'isAmbiguous': False,
                   'ambiguity': []},
           'Origin': {'name': 'Origin', 'queryPhrase': ['origin'], 'inferenceType': 'explicit', 'isAmbiguous': False,
                      'ambiguity': []}}, 'taskMap': {'derived_value': [
        {'task': 'derived_value', 'queryPhrase': 'average', 'operator': 'AVG', 'values': [], 'attributes': ['MPG'],
         'inferenceType': 'explicit', 'followup_type': 'nothing'}]}, 'followUpQuery': False, 'contextObj': None,
       'attributeMapping': {'MPG': {'mpg': 1}, 'Origin': {'origin': 1}}, 'followUpConfidence': None,
       'ambiguity': {'attribute': {}, 'value': {}}, 'dialogId': '0', 'queryId': '0'}

#
# st.write("show average mpg of different origin")
# col1, col2 = st.columns([2, 1])
# with col1:
#     st.write("NL4DV 3.0")
#     st.vega_lite_chart(dt["visList"][0]["vlSpec"])
# with col2:
#     st.write("NL4DV 2.0")
#     st.vega_lite_chart(dt2["visList"][0]["vlSpec"])

print (dt2.get('taskMap', {}))

