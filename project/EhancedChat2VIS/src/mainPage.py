import streamlit as st
import os
import pandas as pd
from streamlit_option_menu import option_menu

# The model can be used, name: code
availableLLM = {
    "ChatGPT 4o mini": "gpt4oMini",
    "ChatGPT 4o": "gpt4o",
    "ChatGPT o1": "gptO1",
    "NL4DV": "nl4dv",
    "ncNET": "ncNet",
    "yoloPandas": "YOLOPandas"}

# OpenAI API key.
apiKey = ''
if 'apiKey' not in st.session_state:
    st.session_state.apiKey = ''
else:
    apiKey = st.session_state.apiKey

# User choice of LLM usage.
llmChoice = {}

# Preload example datasets.
dataLoc = '../data'
fileNames = os.listdir(dataLoc)
if 'exampleDataset' not in st.session_state:
    exampleDataset = {}
    for fileName in fileNames:
        exampleDataset[fileName.split('.')[0]] = pd.read_csv(f'{dataLoc}/{fileName}')
    st.session_state.exampleDataset = exampleDataset
else:
    exampleDataset = st.session_state.exampleDataset

# Choose example data, isExampleDataset = True.
if 'isExampleDataset' not in st.session_state:
    st.session_state['isExampleDataset'] = True  # Default value


# API Key dialog
@st.dialog("API key")
def key(api):
    st.write("Enter OpenAI API Key")
    apikeyInput = st.text_input("API Key", api)
    if st.button('Submit'):  #
        st.session_state.apiKey = apikeyInput
        st.rerun()


# Sidebar contents.
with st.sidebar:
    st.title("Enhanced Chat2VIS")
    col1, col2 = st.columns([2, 1])  # Adjust the ratio for better alignment

    with col1:
        st.markdown("### Choose your models")

    # API Key button
    with col2:
        if st.button('Key ✅' if st.session_state.apiKey != '' else 'API Key'):
            key(st.session_state.apiKey)
            apiKey = st.session_state.apiKey

    # LLM checkbox
    for llmName, llmCode in availableLLM.items():
        llmChoice[llmCode] = st.checkbox(llmName)

    # Dataset source
    st.markdown("### Choose your dataset")

    datasetSelected = option_menu(None, ['Example', 'Upload'],
                                  icons=['clipboard-data-fill', 'file-earmark-arrow-up-fill'], orientation="horizontal")

    #
    if datasetSelected == "Example":
        st.session_state['isExampleDataset'] = True
        exampleDataChosen = st.radio(
            "Choose an example dataset", [key.capitalize() for key in exampleDataset.keys()]
        )
    else:
        st.session_state['isExampleDataset'] = False
        # Upload a .csv file
        try:
            # TO DO: read csv
            uploadDataset = st.file_uploader("Please upload a CSV file", type="csv")
            if uploadDataset is not None:
                fileName = uploadDataset.name.capitalize()
        except Exception as e:
            st.error("File failed to load. Please select a valid CSV file.")
            print("File failed to load.\n" + str(e))
