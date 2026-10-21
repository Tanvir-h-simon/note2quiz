from pydantic import BaseModel
from gemini_client import client, MODEL

class Question(BaseModel):
    question: str
    options: list[str]
    answer: str
    explanation: str

def generate_quiz(notes, difficulty):

    prompt = f"Create a {difficulty} level quiz of 5 multiple choice questions based on the following note. " \
    "Each question must have exactly 4 options, and the answer must be copied exactly from one of the options. " \
    "Add a one sentence explanation for each answer.\n\n" \
    f"Note:\n{notes}"

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": list[Question],
        }
    )

    return response.parsed