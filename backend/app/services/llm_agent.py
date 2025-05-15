import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def analyze_products(products: list[dict]):
    prompt = "Compare the following products and recommend the best one based on price and rating:\n"
    for p in products:
        prompt += f"- {p.get('title', '')}, Price: {p.get('price', 'N/A')}, Rating: {p.get('rating', 'N/A')}\n"

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a smart shopping assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return {"recommendation": completion.choices[0].message.content}

