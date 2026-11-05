
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# Load .env from the main CareerPilot_AI folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def generate_career_guidance(
    student_profile,
    predicted_career,
    existing_recommendations=None,
):
    """Generate personalized career guidance using Ollama Cloud."""

    api_key = os.getenv("OLLAMA_API_KEY")
    model = os.getenv("OLLAMA_MODEL")

    if not api_key:
        raise ValueError(
            "OLLAMA_API_KEY is missing. Check the .env file "
            "in your CareerPilot_AI folder."
        )

    if not model:
        raise ValueError(
            "OLLAMA_MODEL is missing. Add your working model "
            "name to the .env file."
        )

    client = OpenAI(
        base_url="https://ollama.com/v1",
        api_key=api_key,
    )

    prompt = f"""
You are CareerPilot AI, a helpful career guidance assistant
for college students.

The student's career prediction comes from an existing
machine-learning model. Explain that prediction; do not
change or pretend to retrain the model.

STUDENT PROFILE:
{student_profile}

ML-PREDICTED CAREER:
{predicted_career}

EXISTING RECOMMENDATIONS:
{existing_recommendations or "No existing recommendations provided."}

Prepare practical, beginner-friendly guidance using these headings:

1. Understanding Your ML Prediction
2. Why This Career May Suit You
3. Skills You Already Have
4. Skills to Develop
5. Personalized 8-Week Learning Roadmap
6. Suggested Projects
7. Useful Learning Resources
8. Next Steps

Keep advice realistic for a college student. Do not invent
the student's skills, qualifications, or achievements.
If information is missing, clearly say so.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You provide practical, honest, supportive "
                    "career guidance to students."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )

    answer = response.choices[0].message.content

    if not answer:
        raise RuntimeError("Ollama returned an empty response.")

    return answer
