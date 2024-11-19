import json
import os

import pandas as pd
import openai
import warnings

available_models = {"ChatGPT-4": "gpt-4o"}
selected_models = "ChatGPT-4"
model_type = selected_models
datasets = {}
openai_key = ""

def run_request(question_to_ask, model_type, key):
    if model_type == "gpt-4o" or model_type == "gpt-4o-mini":
        # Run OpenAI ChatCompletion API
        task = "Generate Python Code Script."
        if model_type == "gpt-4o" or model_type == "gpt-4o-mini":
            # Ensure GPT-4 does not include additional comments
            task = task + " The script should only include code, never start with \"```python\", no comments."
        # openai.api_key = key
        client = openai.OpenAI(api_key=key)
        response = client.chat.completions.create(model=model_type,
                                                  messages=[{"role": "system", "content": task},
                                                            {"role": "user", "content": question_to_ask}])
        llm_response = response.choices[0].message.content
    return llm_response

def get_code(text):
    text = text.replace("```python","```")
    marker = "```"
    findBlock = False
    start_index = text.find(marker)
    if start_index != -1:
        findBlock = True
        end_index = text.find(marker, start_index + len(marker))
    return text if not findBlock else text[start_index + len(marker):end_index].strip()


def format_question(primer_desc, primer_code, question, model_type):
    # Put the question at the end of the description primer within quotes, then add on the code primer.
    return '\n' + primer_desc + question + '\n\n' + primer_code


def get_primer(df_dataset, database_name, df_name):
    # Primer function to take a dataframe and its name
    # and the name of the columns
    # and any columns with less than 20 unique values it adds the values to the primer
    # and horizontal grid lines and labeling

    primer_desc = "Use a dataframe called df from \"" + "./visEval_dataset/databases/" + database_name + "/" + df_name + ".csv\" with columns '" \
                  + "','".join(str(x) for x in df_dataset.columns) + "'. "
    for i in df_dataset.columns:
        if len(df_dataset[i].drop_duplicates()) < 20 and df_dataset.dtypes[i] == "O":
            primer_desc = primer_desc + "\nThe column '" + i + "' has categorical values '" + \
                          "','".join(str(x) for x in df_dataset[i].drop_duplicates()) + "'. "
        elif df_dataset.dtypes[i] == "int64" or df_dataset.dtypes[i] == "float64":
            primer_desc = primer_desc + "\nThe column '" + i + "' is type " + str(
                df_dataset.dtypes[i]) + " and contains numeric values. "
    primer_desc = primer_desc + "\nLabel the x and y axes appropriately."
    primer_desc = primer_desc + "\nAdd a title. Set the fig suptitle as empty."
    primer_desc = primer_desc + "{}"  # Space for additional instructions if needed
    primer_desc = primer_desc + "\nUsing Python version 3.9.12, create a script using the dataframe df to graph the following: "
    pimer_code = "import pandas as pd\nimport matplotlib.pyplot as plt\n"
    pimer_code = pimer_code + "fig,ax = plt.subplots(1,1,figsize=(10,4))\n"
    pimer_code = pimer_code + "ax.spines['top'].set_visible(False)\nax.spines['right'].set_visible(False) \n"
    pimer_code = pimer_code + "df = pd.read_csv('./visEval_dataset/databases/' + database_name + '/' + df_name + '.csv')\n"
    return primer_desc, pimer_code


def print_output(database_name, df_name, question, key, rules=None, example=None):

    file_path = "./visEval_dataset/databases/" + database_name + "/" + df_name + ".csv"

    if not os.path.exists(file_path):
        print("file not exist")
        df_name = df_name.capitalize()
        file_path = f"./visEval_dataset/databases/{database_name}/{df_name}.csv"

    chosen_dataset = df_name
    datasets[chosen_dataset] = pd.read_csv(file_path)
    print ("Database = " + database_name + ";   chosen_table = " + chosen_dataset)

    # Execute chatbot query
    if len(key) > 0:
        # Get the primer for this dataset
        primer1, primer2 = get_primer(datasets[chosen_dataset], database_name, df_name)
        if rules is not None:
            # add zero-shot rules for primer_desc
            primer1 = "".join(rules) + primer1
        if example is not None:
            # add one-shot example to the original primer_desc, which describes the column names and data types of a given table
            primer1 = primer1 + example
        # Create model, run the request and print the results
        try:
            # Format the question
            # print("Model: " + model_type)
            question_to_ask = format_question(primer1, primer2, question, model_type)
            # print the query question
            # print(question_to_ask)
            # Run the question
            answer = run_request(question_to_ask, available_models[model_type], key=key)
            answer = get_code(answer)
            # the answer is the completed Python script so add to the beginning of the script to it.
            # answer = primer2 + answer
            print('\n')
            print(answer)
            # repr could get the orginal string with '\n'
            print(repr(answer))
            exec(answer)
            return answer
        except Exception as e:
            print('Error:', e)
            return None
    else:
        raise ValueError("Error: please initialize key first.")


def run_visEval(question_serial, question_index, key):
    with open('./data.json', 'r') as file:
        data = json.load(file)
        database_name = data[question_serial]['db_id']
        df_name = data[question_serial]['table_id']
        question = data[question_serial]['nl_queries'][question_index]
        print('\n')
        print(question_serial + ' - ' + str(question_index) + ': ')
        print(question + '\n')
        return print_output(database_name, df_name, question, key)
