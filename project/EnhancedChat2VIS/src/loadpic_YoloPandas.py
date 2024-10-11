from yolopandas import pd
import os
import streamlit as st


def use_yolopandas(url, api_key, query):
    os.environ['OPENAI_API_KEY'] = api_key
    product_df = pd.read_csv(url)
    result = product_df.llm.query(query, yolo=True)

    return result
