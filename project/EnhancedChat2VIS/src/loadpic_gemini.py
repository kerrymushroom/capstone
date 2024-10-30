import streamlit as st
import json
from withLangChain import useGemini


def use_gemini(url, api_key, query):
    answer = useGemini(url, query)

    cleaned_answer = answer.replace('```json', '', 1).strip("`")
    return json.loads(cleaned_answer)
