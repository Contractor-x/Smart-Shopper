import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def analyze_products(products: list[dict]):
    prompt = "Compare the following products and pick the best one for VALUE (not just lowest price):\n\n"
    for i, p in enumerate(products):
        prompt += f"{i+1}. {p.get('title', 'No Title')} — Price: {p.get('price', 'N/A')}, Rating: {p.get('rating', 'N/A')}\n"
    prompt += "\nReturn a one-paragraph recommendation and name the top pick."

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You're a product analyst AI helping people shop smart."},
            {"role": "user", "content": prompt}
        ]
    )
    return {"recommendation": completion.choices[0].message.content.strip()}


