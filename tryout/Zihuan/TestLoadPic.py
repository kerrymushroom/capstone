from yolopandas import pd
import matplotlib.pyplot as plt
import os
import streamlit as st

def use_yolopandas(url, query):
    # Set OpenAI API key
    # os.environ['OPENAI_API_KEY'] = api_key

    # Read CSV file
    df = pd.read_csv(url)

    # Specified keywords
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
            fig = result.figure
            return fig
        else:
            print("The result is not a matplotlib Axes object.")
            return None


    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    

# Case study 1
url = "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/department_store.csv"
query = "What is the highest price of product, grouped by product type? Show a bar chart, and display by the names in desc."
fig = use_yolopandas(url, query)

if fig is not None:
    st.title('My Streamlit App with Existing Axes Data')
    st.pyplot(fig)  # Display the figure in Streamlit
else:
    st.write("No valid plot was returned.")
# plt.show()
# Case study 2
# url = "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/colleges.csv"
# query = "Show debt and earnings for Public and Private colleges."
# print(type(use_yolopandas(url, query)))

# Case study 3
# url = "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/energy_production.csv"
# query = "What is the trend of oil production since 2004?"
# print(type(use_yolopandas(url, query)))

# Case study 4
# url = "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/customers_and_products_contacts.csv"
# query = "Show the number of products with price higher than 1000 or lower than 500 for each product name in a bar chart, and could you rank y-axis in descending order?"
# print(type(use_yolopandas(url, query)))

# Case study 5
# url = "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/movies.csv"
# query = "draw the numbr of movie by gener"
# print(type(use_yolopandas(url, query)))

# Case study 6
# url = "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/movies.csv"
# query = "tomatoes"
# print(type(use_yolopandas(url, query)))