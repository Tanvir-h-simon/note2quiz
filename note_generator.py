from google.genai import types
from gemini_client import client, MODEL

def generate_note(files):

    prompt = "Summarize the content of the uploaded image in no more than 100 words. " \
    "Organize the summary into relevant sections using appropriate Markdown formatting, " \
    "such as headings, bullet points, and bold text, to highlight key information and improve readability."

    # Converting the uploaded files into parts Gemini can read
    parts = [types.Part.from_bytes(data=file.getvalue(), mime_type=file.type) for file in files]

    response = client.models.generate_content(
        model=MODEL,
        contents=[*parts, prompt]
    )

    return response.text