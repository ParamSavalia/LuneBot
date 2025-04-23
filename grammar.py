from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def correct_grammar(text, lang="french"):
    prompt = f"""
Please correct the grammar and spelling mistakes in this {lang} sentence. Do not explain, just return the corrected version.

Text: {text}
Corrected:
"""
    response = client.chat.completions.create(
        model="gpt-4-turbo",  # or "gpt-4"
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
