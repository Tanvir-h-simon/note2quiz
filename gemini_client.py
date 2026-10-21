from google import genai
from dotenv import load_dotenv
import os

# Loading the environment variable
load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

# Initializing a client, shared by the note and quiz generators
client = genai.Client(api_key=gemini_key)

MODEL = 'gemini-3.8-flash'