
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load settings from the .env file
load_dotenv()

api_key = os.getenv("OLLAMA_API_KEY")
model = os.getenv("OLLAMA_MODEL", "gemma4:31b")

if not api_key:
    raise ValueError(
        "OLLAMA_API_KEY not found. Check your .env file."
    )

# Connect to Ollama Cloud
client = OpenAI(
    base_url="https://ollama.com/v1",
    api_key=api_key
)

try:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": "Introduce yourself in one sentence."
            }
        ]
    )

    print("\nOllama connection successful!")
    print(response.choices[0].message.content)

except Exception as error:
    print("\nConnection failed.")
    print("Error:", error)
