
import openai
import pandas as pd
import os
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

def use_chatgpt(url, api_key, query, type):
    os.environ['OPENAI_API_KEY'] = api_key
    openai.api_key = api_key

    csv = pd.read_csv(url)
    primer1, primer2 = getTemplateCode(csv, url)

    question_to_ask = format_question(primer1, primer2, query)

    print(question_to_ask)
    # use model to generate some code from gpt
    result = run_gpt(question_to_ask, type)
    print(result)
    #
    cleaned_code = result.lstrip('```python')
    cleaned_code = cleaned_code.rstrip('```')
    exec(cleaned_code)
    return cleaned_code
def format_question(primer_desc,primer_code , question):
    # Fill in the model_specific_instructions variable
    instructions = ""
    primer_desc = primer_desc.format(instructions)
    # Put the question at the end of the description primer within quotes, then add on the code primer.
    return  '"""\n' + primer_desc + question + '\n"""\n' + primer_code

def getTemplateCode(df_dataset, csv_url):
    # Extract the file name (like 'movies') from the URL
    df_name = csv_url.split('/')[-1].replace('.csv', '')  # This will be 'movies' for 'movies.csv'

    # Describe the data and columns
    primer_desc = f"Use a dataframe called df from '{csv_url}' with columns '" \
                  + "','".join(str(x) for x in df_dataset.columns) + "'. "

    for i in df_dataset.columns:
        if len(df_dataset[i].drop_duplicates()) < 20 and df_dataset.dtypes[i] == "O":
            primer_desc += f"\nThe column '{i}' has categorical values '" + \
                           "','".join(str(x) for x in df_dataset[i].drop_duplicates()) + "'. "
        elif df_dataset.dtypes[i] == "int64" or df_dataset.dtypes[i] == "float64":
            primer_desc += f"\nThe column '{i}' is type " + str(df_dataset.dtypes[i]) + " and contains numeric values. "

    primer_desc += "\nLabel the x and y axes appropriately."
    primer_desc += "\nAdd a title. Set the fig suptitle as empty."
    primer_desc += "{}"  # Space for additional instructions if needed
    primer_desc += "\nUsing Python version 3.9.12, create a script using the dataframe df to graph the following: "

    # Adjusting the code snippet to read from the URL
    pimer_code = "import pandas as pd\nimport matplotlib.pyplot as plt\n"
    pimer_code += f"df = pd.read_csv('{csv_url}')\n"
    pimer_code += "fig,ax = plt.subplots(1,1,figsize=(10,4))\n"
    pimer_code += "ax.spines['top'].set_visible(False)\nax.spines['right'].set_visible(False)\n"
    pimer_code += f"df = {df_name}.copy()\n"  # Use the dynamically extracted df_name

    return primer_desc, pimer_code

def run_gpt(question_to_ask, model_type):
    llm_response = None
    supported_models = ["gpt-4o", "gpt-4o-mini"]
    if model_type in supported_models:
        # 设置任务描述
        task = "Generate Python Code Script.The script should only include code, no comments. I need executable code. Do not append any other non-executable text."
        try:
            # 调用 OpenAI ChatCompletion API
            response = openai.ChatCompletion.create(
                model=model_type,
                messages=[
                    {"role": "system", "content": task},
                    {"role": "user", "content": question_to_ask}
                ]
            )
            llm_response = response['choices'][0]['message']['content']  # 提取返回的内容
        except Exception as e:
            print("An error occurred while calling the OpenAI API:", e)
            return ""
    else:
        print(f"Model '{model_type}' is not supported.")
        return ""

    return llm_response
# #case1
# use_chatgpt(exampleData["department_store"],
#             "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",
#             "What is the highest price of product, grouped by product type? Show a bar chart, and display by the names in desc.")
#
# use_chatgpt(exampleData["colleges"],
#             "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",
#             "Show debt and earnings for Public and Private colleges.")
#
#
# use_chatgpt(exampleData["energy_production"],
#             "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",
#             "What is the trend of oil production since 2004?")
#
#
# use_chatgpt(exampleData["customers_and_products_contacts"],
#             "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",
#             "Show the number of products with price higher than 1000 or lower than 500 for each product name in a bar chart, and could you rank y-axis in descending order?")
#
#
# use_chatgpt(exampleData["movies"],
#             "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",
#             "draw the numbr of movie by gener")


use_chatgpt(exampleData["movies"],
            "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",
            "tomatoes",
            "gpt-4o")
