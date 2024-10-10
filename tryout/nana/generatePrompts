from openai import OpenAI
import openai
import random
import matplotlib.pyplot as plt
import pandas as pd

client = OpenAI(
    api_key="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",
)


def run_gpt(question_to_ask, model_type, key):
    llm_response = None
    if model_type == "gpt-4o-mini" or model_type == "gpt-3.5-turbo":
        # Run OpenAI ChatCompletion API
        task = "Generate Python Code Script."
        if model_type == "gpt-4o-mini":
            # Ensure GPT-4 does not include additional comments
            task = task + " The script should only include code, no comments. I need a executable code.Do not append any other can not execute text"
        response = client.chat.completions.create(
            model=model_type,
            messages=[
                {"role": "system", "content": task},
                {"role": "user", "content": question_to_ask}
            ]
        )
        llm_response = response.choices[0].message.content
    elif model_type == "text-davinci-003" or model_type == "gpt-3.5-turbo-instruct":
        response = openai.Completion.create(
            engine=model_type,
            prompt=question_to_ask,
            temperature=0,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        llm_response = response.choices[0].text

    else:
        print(f"Model '{model_type}' is not supported.")
        return ""
    return llm_response


# get all available model of chat gpt
def get_available_models():
    try:
        models_response = client.models.list()
        model_ids = [model.id for model in models_response.data]
        return model_ids
    except Exception as e:
        print("An error occurred while fetching models:", e)
        return []


def getTemplateCode(df_dataset, df_name):
   
    primer_desc = "Use a dataframe called df from '../../project/EnhancedChat2VIS/data/movies.csv' with columns '" \
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
    pimer_code = pimer_code + "df=" + df_name + ".copy()\n"
    return primer_desc, pimer_code

question_to_ask0 = "Generate Python code to calculate the sum of an array of integers. The function should take an input list and return the sum."
question_to_ask1 = "Write a Python function named `calculate_sum` that takes a list of integers as input and returns the sum. The input will be a list like `[1, 2, 3, 4]`, and the output should be the integer sum of the list. Make sure the function is properly structured with type hints."
question_to_ask2 = "Generate Python code that calculates the sum of a list of integers. Optimize the code for performance."
question_to_ask3 = "Write a Python function that calculates the sum of a list of integers. Focus on readability and clarity."
template = """
def calculate_sum(numbers: List[int]) -> int:
    # Your code here
    pass
"""

#we can found this one with template is the best one to get code, which we need get a graph.
question_to_ask4 = "Fill in the provided Python function template to calculate the sum of a list of integers. {template}"

question_to_ask5 = "Write a Python function to calculate the sum of a list of integers. Include unit tests using the `unittest` library to verify its correctness."
question_to_ask6 = "Improve the previously generated Python function by handling empty lists and adding type annotations."

result0 = run_gpt(question_to_ask0, "gpt-4o-mini", client.api_key)
result1 = run_gpt(question_to_ask1, "gpt-4o-mini", client.api_key)
result2 = run_gpt(question_to_ask2, "gpt-4o-mini", client.api_key)
result3 = run_gpt(question_to_ask3, "gpt-4o-mini", client.api_key)
result4 = run_gpt(question_to_ask4, "gpt-4o-mini", client.api_key)
result5 = run_gpt(question_to_ask5, "gpt-4o-mini", client.api_key)
result6 = run_gpt(question_to_ask6, "gpt-4o-mini", client.api_key)

print(result0)
print(result1)
print(result2)
print(result3)
print(result4)
print(result5)
print(result6)
