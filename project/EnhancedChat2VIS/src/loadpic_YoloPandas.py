from yolopandas import pd
import matplotlib.pyplot as plt
import os
import streamlit as st


def use_yolopandas(url, api_key, query):
    os.environ['OPENAI_API_KEY'] = api_key

    df = pd.read_csv(url)

    # Checks whether the specified word is contained
    keywords = ['plot', 'chart', 'diagram', 'picture', 'graph', 'photo']

    # Check if the query contain these keywords, add a hint
    if not any(keyword in query.lower() for keyword in keywords):
        query += " For the result, show a plot. Return a matplotlib Axes object."
    else:
        query += " Return a matplotlib Axes object."

    try:
        # Executing YOLOPandas queries
        result = df.llm.query(query, yolo=True)
        # Check if result is an instance of matplotlib Axes
        if isinstance(result, plt.Axes):
            print("The result is a matplotlib Axes object.")
            plt.show()  # Show the plot if it is an Axes object
        else:
            print("The result is not a matplotlib Axes object.")
            return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

    return result

    product_df = pd.read_csv(url)
    result = product_df.llm.query(query, yolo=True)

    return result
