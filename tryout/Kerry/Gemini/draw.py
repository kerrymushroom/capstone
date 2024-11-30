import streamlit as st
import json
from langChainTest import useGemini

url = "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/cars.csv"
question = "Average MPG by origin."
answer = useGemini(url, question)

cleaned_answer = answer.replace('```json', '', 1).strip("`")

st.vega_lite_chart(json.loads(cleaned_answer))
