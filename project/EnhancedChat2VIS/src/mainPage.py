import streamlit as st
import os
import pandas as pd
from streamlit_option_menu import option_menu

# The models that can be used, name: code
availableLLM = {
    "ChatGPT 4o mini": "gpt4oMini",
    "ChatGPT 4o": "gpt4o",
    "ChatGPT o1": "gptO1",
    "NL4DV": "nl4dv",
    "ncNET": "ncNet",
    "yoloPandas": "YOLOPandas"
}

# OpenAI API key input
apiKey = ''
if 'apiKey' not in st.session_state:
    st.session_state.apiKey = ''
else:
    apiKey = st.session_state.apiKey

# User choice of LLM usage
llmChoice = {}

# Preload example datasets
dataLoc = '../data'
fileNames = os.listdir(dataLoc)
if 'exampleDataset' not in st.session_state:
    exampleDataset = {}
    for fileName in fileNames:
        exampleDataset[fileName.split('.')[0]] = pd.read_csv(f'{dataLoc}/{fileName}')
    st.session_state.exampleDataset = exampleDataset
else:
    exampleDataset = st.session_state.exampleDataset

# Sidebar contents
with st.sidebar:
    st.title("Enhanced Chat2VIS")
    st.markdown("### Choose your models")
    # Model selection checkboxes
    for llmName, llmCode in availableLLM.items():
        llmChoice[llmCode] = st.checkbox(llmName)

    # Dataset source selection
    st.markdown("### Choose your dataset")
    datasetSelected = option_menu(None, ['Example', 'Upload'],
                                  icons=['clipboard-data-fill', 'file-earmark-arrow-up-fill'], orientation="horizontal")

    # Example dataset selection
    if datasetSelected == "Example":
        st.session_state['isExampleDataset'] = True
        exampleDataChosen = st.radio(
            "Choose an example dataset", [key.capitalize() for key in exampleDataset.keys()]
        )
    else:
        st.session_state['isExampleDataset'] = False
        # Upload a CSV file
        uploadDataset = st.file_uploader("Please upload a CSV file", type="csv")
        if uploadDataset is not None:
            fileName = uploadDataset.name  # 获取上传文件的名称
            # Store uploaded dataset in session state
            st.session_state.uploaded_df = pd.read_csv(uploadDataset)

# Text area for input commands
st.markdown("## What would you like to visualize?")
user_input = st.text_area("👀 What would you like to visualize?")

# Button to run LLM
if st.button('Go...'):
    # Placeholder for LLM processing (to be implemented)
    st.write(f"Running model on: {user_input}")

# Display dataset as a table
if 'isExampleDataset' in st.session_state and st.session_state['isExampleDataset']:
    if exampleDataChosen:
        st.markdown(f"### {exampleDataChosen} Dataset")
        st.dataframe(exampleDataset[exampleDataChosen.lower()])
elif 'uploaded_df' in st.session_state:
    st.markdown(f"### Uploaded Dataset: {fileName}")
    st.dataframe(st.session_state.uploaded_df)
