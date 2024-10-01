import streamlit as st
import os
import pandas as pd
from streamlit_option_menu import option_menu
from uploadServer import *
from loadpic_NL4DV import *

# The models that can be used, name: code
availableLLM = {
    "ChatGPT 4o mini": "gpt4oMini",
    "ChatGPT 4o": "gpt4o",
    # "ChatGPT o1": "gptO1",
    "NL4DV 2.0": "nl4dv_2",
    "NL4DV 3.0": "nl4dv_3",
    # "ncNET": "ncNet",
    "yoloPandas": "YOLOPandas"
}

# Example data URLs
# TODO: Change ways to choose example data
exampleData = {
    "cars": "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/cars.csv",
    "colleges": "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/colleges.csv",
    "customers_and_products_contacts": "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/customers_and_products_contacts.csv",
    "department_store": "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/department_store",
    "energy_production": "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/energy_production.csv",
    "housing": "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/housing.csv",
    "movies": "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/movies.csv"
}

# OpenAI API key input
apiKey = ''
if 'apiKey' not in st.session_state:
    st.session_state.apiKey = ''
else:
    apiKey = st.session_state.apiKey

# User choice of LLM usage
llmChoice = {}

# Start local server
if 'server_started' not in st.session_state:
    st.session_state.server_started = False

if not st.session_state.server_started:
    start_server()
    st.session_state.server_started = True


# API Key dialog
@st.dialog("API key")
def key(api):
    st.write("Enter OpenAI API Key")
    apikeyInput = st.text_input("API Key", api)
    if st.button('Submit'):  #
        st.session_state.apiKey = apikeyInput
        st.rerun()


# Preload example datasets
dataLoc = '../data'
fileNames = os.listdir(dataLoc)
if 'exampleDataset' not in st.session_state:
    exampleDataset = {}
    for fileName in fileNames:
        local_file_upload(f'{dataLoc}/{fileName}', "example")
        exampleDataset[fileName.split('.')[0]] = pd.read_csv(f'{dataLoc}/{fileName}')
    st.session_state.exampleDataset = exampleDataset
else:
    exampleDataset = st.session_state.exampleDataset

# Chosen file name
chosenFile = ''

# Sidebar contents
with st.sidebar:
    st.title("Enhanced Chat2VIS")
    col1, col2 = st.columns([2, 1])  # Adjust the ratio for better alignment

    with col1:
        st.markdown("### Choose your models")

    # API key button
    with col2:
        if st.button('Key ✅' if st.session_state.apiKey != '' else 'API Key'):
            key(st.session_state.apiKey)
            apiKey = st.session_state.apiKey

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
        chosenFile = exampleDataChosen.lower() + ".csv"
        print(chosenFile)
    else:
        st.session_state['isExampleDataset'] = False
        chosenFile = ''
        # Upload a CSV file
        uploadDataset = st.file_uploader("Please upload a CSV file", type="csv")
        if uploadDataset is not None:
            uploadFileName = uploadDataset.name  # Get upload file name

            # Upload data to local server
            local_file_upload(uploadDataset, 'upload')

            # Store uploaded dataset in session state
            st.session_state.uploaded_df = pd.read_csv(uploadDataset)
            chosenFile = uploadFileName

# Text area for input commands
st.markdown("## What would you like to visualize?")
user_input = st.text_area("👀 What would you like to visualize?")

# Button to run LLM
if st.button('Go...', key='submit'):
    if chosenFile == '':
        st.write("Please upload a CSV file")
    else:
        # Placeholder for LLM processing (to be implemented)
        st.write(f"Running model on: {user_input}")
        if llmChoice["nl4dv_3"]:
            print("running nl4dv_3")
            st.vega_lite_chart(use_nl4dv_3(f"http://localhost:8000/{chosenFile}", apiKey, user_input))

# Display dataset as a table
if 'isExampleDataset' in st.session_state and st.session_state['isExampleDataset']:
    if exampleDataChosen:
        st.markdown(f"### {exampleDataChosen} Dataset")
        st.dataframe(exampleDataset[exampleDataChosen.lower()])
elif 'uploaded_df' in st.session_state:
    st.markdown(f"### Uploaded Dataset: {uploadFileName}")
    st.dataframe(st.session_state.uploaded_df)
