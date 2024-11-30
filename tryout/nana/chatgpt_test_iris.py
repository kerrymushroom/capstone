from openai import OpenAI
import openai
import random
client = OpenAI(
    api_key="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",
)
def run_gpt(question_to_ask, model_type, key):
    llm_response = None
    if model_type == "gpt-4" or model_type == "gpt-3.5-turbo" :
        # Run OpenAI ChatCompletion API
        task = "Generate Python Code Script."
        if model_type == "gpt-4":
            # Ensure GPT-4 does not include additional comments
            task = task + " The script should only include code, no comments."
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
#get all available model of chat gpt
def get_available_models():
    try:
        models_response = client.models.list()
        model_ids = [model.id for model in models_response.data]
        return model_ids
    except Exception as e:
        print("An error occurred while fetching models:", e)
        return []
models=get_available_models()
selected_model = random.choice(models)#get a random model include voice and picture and code model.
print(selected_model)
#use model to generate some code from gpt
result = run_gpt("give me some code ,sum 2 number","gpt-4",client.api_key)
print(result)
