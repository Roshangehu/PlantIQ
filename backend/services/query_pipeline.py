import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = "openai/gpt-oss-20b"


def pipeline(question: str, history: list = None) -> str:

    if history is None:
        history = []

    messages = [
        {
            "role": "system",
            "content": (
                "You are PlantIQ, an AI-powered industrial "
                "maintenance assistant. "
                "Answer questions clearly and accurately. "
                "Explain technical concepts in simple language. "
                "Never invent equipment specifications or "
                "present uncertain advice as verified "
                "safety instructions."
            )
        }
    ]

    # Add previous conversation
    messages.extend(history)

    # Add the latest question
    messages.append({
        "role": "user",
        "content": question
    })

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.3,
        max_completion_tokens=1024
    )

    answer = response.choices[0].message.content

    return answer