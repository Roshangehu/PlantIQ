import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Select the LLM
MODEL_NAME = "openai/gpt-oss-20b"


def generate_response(question: str) -> str:

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are PlantIQ, an AI-powered industrial "
                    "maintenance assistant. "
                    "Provide clear, helpful and technically "
                    "accurate answers about industrial equipment "
                    "and maintenance. Never invent equipment "
                    "specifications or present uncertain advice "
                    "as verified safety instructions."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.3,
        max_completion_tokens=1024
    )

    answer = response.choices[0].message.content

    return answer