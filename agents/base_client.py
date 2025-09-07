#Import all dependencies and librraies required
import os
from dotenv import load_dotenv
import google.generativeai as genai

#Load environmnet variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found.")

#Configuring gemini
genai.configure(api_key=api_key)

#Just to see the gemini model instance
def get_model(model_name="gemini-2.0-flash"):
    return genai.GenerativeModel(model_name)