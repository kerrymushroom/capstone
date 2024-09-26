import os
from openai import OpenAI

client = OpenAI(
    # Gets API Key from environment variable OPENAI_API_KEY
    api_key=os.environ.get("OPENAI_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "How are you?",
        }
    ],
    # model="gpt-3.5-turbo",
    # model="gpt-4o",
    # model="gpt-4o-mini",
    model="o1-preview",
)

# print response
message_content = chat_completion.choices[0].message.content
print(message_content)