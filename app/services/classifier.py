import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def classify_statement(message: str) -> str:
    prompt = f"""Classify the following statement into exactly one of these categories:
- question (asking for information)
- demand (commanding or requesting action)
- angry (frustrated, upset, or hostile tone)
- insulting (derogatory or offensive)
- neutral (none of the above)

Respond with only the category name, nothing else.

Statement: "{message}"

Category:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10,
    )

    category = response.choices[0].message.content.strip().lower()

    valid_categories = ["question", "demand", "angry", "insulting", "neutral"]
    if category not in valid_categories:
        category = "neutral"

    return category
