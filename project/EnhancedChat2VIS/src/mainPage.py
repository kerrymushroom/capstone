import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from loadpic_NL4DV import *
import requests
from loadpic_YoloPandas import use_yolopandas
from loadpic_gemini import use_gemini
from loadpic_chatgpt import use_chatgpt

# The models that can be used, name: code
availableLLM = {
    "ChatGPT 4o mini": "gpt-4o-mini",
    "ChatGPT 4o": "gpt-4o",
    # "ChatGPT o1": "gptO1",
    "NL4DV 2.0": "nl4dv_2",
    "NL4DV 3.0": "nl4dv_3",
    "Gemini": "gemini",
    "yoloPandas": "YOLOPandas"
}

# Example data URLs
exampleData = {
    "cars": "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/cars.csv",
    "colleges": "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/colleges.csv",
    "customers_and_products_contacts": "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main"
                                       "/customers_and_products_contacts.csv",
    "department_store": "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/department_store.csv",
    "energy_production": "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/energy_production.csv",
    "housing": "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/housing.csv",
    "movies": "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/movies.csv"
}

# OpenAI API key input
chatGptApiKey = ''
if 'chatGptApiKey' not in st.session_state:
    st.session_state.chatGptApiKey = ''
else:
    chatGptApiKey = st.session_state.chatGptApiKey

geminiApiKey = ''
if 'geminiApiKey' not in st.session_state:
    st.session_state.geminiApiKey = ''
else:
    geminiApiKey = st.session_state.geminiApiKey

# User choice of LLM usage
llmChoice = {}


# API Key dialog
@st.dialog("API key")
def key(api_openai, api_gemini):
    st.write("Enter OpenAI API Key")
    chatGptApikeyInput = st.text_input("OpenAI API Key", api_openai)
    st.write("")
    st.write("Enter Gemini API Key")
    geminiApikeyInput = st.text_input("Gemini API Key", api_gemini)
    if st.button('Submit'):  #
        st.session_state.chatGptApiKey = chatGptApikeyInput
        st.session_state.geminiApiKey = geminiApikeyInput
        st.rerun()


# DEPRECATED: Using public URL instead of using local files.
# Preload example datasets ()

# dataLoc = '../data'
# fileNames = os.listdir(dataLoc)
# if 'exampleDataset' not in st.session_state:
#     exampleDataset = {}
#     for fileName in fileNames:
#         local_file_upload(f'{dataLoc}/{fileName}', "example")
#         exampleDataset[fileName.split('.')[0]] = pd.read_csv(f'{dataLoc}/{fileName}')
#     st.session_state.exampleDataset = exampleDataset
# else:
#     exampleDataset = st.session_state.exampleDataset


# Chosen file name
chosenFileName = ''
chosenFileURL = ''

# Sidebar contents
with (st.sidebar):
    st.title("Enhanced Chat2VIS")
    col1, col2 = st.columns([2, 1])  # Adjust the ratio for better alignment

    with col1:
        st.markdown("### Choose your models")

    # API key button
    with col2:
        if st.button('Key ✅' if (st.session_state.chatGptApiKey != '' and st.session_state.geminiApiKey != '')
                     else 'API Key'):
            key(st.session_state.chatGptApiKey, st.session_state.geminiApiKey)
            chatGptApiKey = st.session_state.chatGptApiKey
            geminiApiKey = st.session_state.geminiApiKey

    # Model selection checkboxes
    for llmName, llmCode in availableLLM.items():
        if (('ChatGPT' in llmName and chatGptApiKey == "") or
                ('yolo' in llmName and chatGptApiKey == "") or ('NL4DV 3.0' in llmName and chatGptApiKey == "")):
            llmChoice[llmCode] = st.checkbox(llmName, disabled=True, help="Please enter ChatGPT API key first.")
        elif 'Gemini' in llmName and geminiApiKey == "":
            llmChoice[llmCode] = st.checkbox(llmName, disabled=True, help="Please enter Gemini API key first.")
        else:
            llmChoice[llmCode] = st.checkbox(llmName)

    # Dataset source selection
    st.markdown("### Choose your dataset")

    # Choose example or custom dataset
    selected = option_menu(None, ['Custom', 'Example'],
                           icons=['file-earmark-arrow-up-fill', 'clipboard-data-fill'],
                           orientation="horizontal")

    # Show example dataset
    if selected == 'Example':
        st.session_state['isExampleDataset'] = True
        exampleDataChosen = st.radio(
            "Choose an example dataset", [key.capitalize() for key in exampleData.keys()]
        )
        chosenFileName = exampleDataChosen.lower()
        chosenFileURL = exampleData[chosenFileName]
        print(chosenFileName, chosenFileURL)

    # Show upload dataset
    else:
        st.session_state['isExampleDataset'] = False
        # 初始化session_state
        if 'customFileURL' not in st.session_state:
            st.session_state['customFileURL'] = ''
            st.session_state['csv_checked'] = False  # To mark whether CONFIRM button is checked.

        # URL input, if checked, disabled input.
        if not st.session_state['csv_checked']:
            inputURL = st.text_input("Input a custom CSV file URL", value=st.session_state['customFileURL'])

            # confirm button, click to check url
            if st.button("Confirm"):
                if inputURL.endswith(".csv"):
                    st.session_state['customFileURL'] = inputURL
                    st.session_state['csv_checked'] = True
                    st.rerun()
                else:
                    st.error("ERROR: Please provide a legal .csv URL")
        else:
            st.text_input("Input a custom CSV file URL", value=st.session_state['customFileURL'], disabled=True)
            st.success(".csv file checked")
            chosenFileName = st.session_state['customFileURL'].split('/')[-1].replace('.csv', '')
            chosenFileURL = st.session_state['customFileURL']
            print(chosenFileName, chosenFileURL)

            # Edit button
            if st.button("Edit"):
                st.session_state['csv_checked'] = False
                st.rerun()

# Text area for input commands
st.markdown("## What would you like to visualize?")
user_input = st.text_area("Input prompts")

# Button to run LLM


if st.button('Go...', key='submit'):
    if chosenFileName == '':
        st.error("ERROR: Please upload or choose a CSV file")
    elif llmChoice == {}:
        st.error("ERROR: Please choose a model")
    else:
        st.markdown(f"##### Running model on: {user_input}")

        # Divide the screen into columns based on the number of models selected
        columns = st.columns(min(len(llmChoice), 3))
        columns2 = st.columns(min(len(llmChoice), 3))
        col_index = 0
        if llmChoice["gpt-4o-mini"]:
            fig = use_chatgpt(chosenFileURL, chatGptApiKey, user_input, "gpt-4o-mini")
            if col_index < 3:
                with columns[col_index]:
                    st.markdown("#### ChatGPT 4o mini")
                    # 检查图形是否生成
                    if fig:
                        st.pyplot(fig)
                    else:
                        st.warning("No figure")
            else:
                with columns2[col_index - 3]:
                    st.markdown("#### ChatGPT 4o mini")
                    if fig:
                        st.pyplot(fig)
                    else:
                        st.warning("No figure")
            col_index += 1
        if llmChoice["gpt-4o"]:
            fig = use_chatgpt(chosenFileURL, chatGptApiKey, user_input, "gpt-4o")
            if col_index < 3:
                with columns[col_index]:
                    st.markdown("#### ChatGPT 4o")
                    # 检查图形是否生成
                    if fig:
                        st.pyplot(fig)
                    else:
                        st.warning("No figure")
            else:
                with columns2[col_index - 3]:
                    st.markdown("#### ChatGPT 4o")
                    if fig:
                        st.pyplot(fig)
                    else:
                        st.warning("No figure")
            col_index += 1
        if llmChoice["nl4dv_3"]:
            if col_index < 3:
                with columns[col_index]:
                    st.markdown("#### NL4DV 3.0")
                    try:
                        st.vega_lite_chart(use_nl4dv_3(chosenFileURL, chatGptApiKey, user_input))
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                with columns2[col_index-3]:
                    st.markdown("#### NL4DV 3.0")
                    try:
                        st.vega_lite_chart(use_nl4dv_3(chosenFileURL, chatGptApiKey, user_input))
                    except Exception as e:
                        st.error(f"Error: {e}")
            col_index += 1

        if llmChoice["nl4dv_2"]:
            if col_index < 3:
                with columns[col_index]:
                    st.markdown("#### NL4DV 2.0")
                    try:
                        st.vega_lite_chart(use_nl4dv_2(chosenFileURL, user_input))
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                with columns2[col_index-3]:
                    st.markdown("#### NL4DV 2.0")
                    try:
                        st.vega_lite_chart(use_nl4dv_2(chosenFileURL, user_input))
                    except Exception as e:
                        st.error(f"Error: {e}")
            col_index += 1

        if llmChoice["YOLOPandas"]:
            if col_index < 3:
                with columns[col_index]:
                    st.markdown("#### YOLOPandas")
                    st.pyplot(use_yolopandas(chosenFileURL, chatGptApiKey, user_input))
            else:
                with columns2[col_index-3]:
                    st.markdown("#### YOLOPandas")
                    st.pyplot(use_yolopandas(chosenFileURL, chatGptApiKey, user_input))
            col_index += 1

        if llmChoice["gemini"]:
            if col_index < 3:
                with columns[col_index]:
                    st.markdown("#### Gemini")
                    st.vega_lite_chart(use_gemini(chosenFileURL, chatGptApiKey, user_input))
            else:
                with columns2[col_index - 3]:
                    st.markdown("#### Gemini")
                    st.vega_lite_chart(use_gemini(chosenFileURL, chatGptApiKey, user_input))
            col_index += 1

# Display dataset as a table
if 'isExampleDataset' in st.session_state and st.session_state['isExampleDataset']:
    if chosenFileName:
        st.markdown(f"### {chosenFileName} Dataset")
        try:
            csv = pd.read_csv(chosenFileURL)
            st.dataframe(csv)
        except Exception as e:
            st.error(f"Can't read CSV file: {e}")
elif 'csv_checked' in st.session_state and st.session_state['csv_checked']:
    st.markdown(f"### Custom Dataset: {chosenFileName}")
    try:
        csv = pd.read_csv(chosenFileURL)
        st.dataframe(csv)
    except Exception as e:
        st.error(f"Can't read CSV file: {e}")
