import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyCLXMk4PNMrGXu3ltiB930Y2bq4h0gE6OY")

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("It's a test, say hello")
print(response.text)