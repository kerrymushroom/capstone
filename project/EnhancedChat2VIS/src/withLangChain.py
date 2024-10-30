import os
import requests
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import tempfile

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["GOOGLE_API_KEY"] = "AIzaSyCLXMk4PNMrGXu3ltiB930Y2bq4h0gE6OY"


def useGemini(csv_url, question):
    question = "Extract information from this question, give back natural language answer, don't need to draw chart." + question
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    # Read the CSV file
    CSVResponse = requests.get(csv_url)
    if CSVResponse.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_file.write(CSVResponse.content)
            temp_file_path = temp_file.name

    agent = create_csv_agent(GoogleGenerativeAI(temprature=0, model="gemini-1.5-flash"), temp_file_path, verbose=True, allow_dangerous_code=True, handle_parsing_errors=True)
    final = agent.run(question)
    systemMessage = "Now you need to chrats. Use human's message to generate the vega-lite visualization json code, no other reply: "
    messages = [
        ("system", systemMessage),
        ("human", question + "I already got the data I need: " + final),
    ]

    llm.invoke(messages)
    return llm.invoke(messages).content
