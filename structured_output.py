import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

def get_movie_info(movie_title: str) -> dict:
    prompt = f"""
    Дай мені структуровану інформацію про фільм "{movie_title}" у форматі:
    {{
        "назва": "...",
        "режисер": "...",
        "рік випуску": ...,
        "жанр": "...",
        "головний актор": "...",
        "тривалість в хвилинах": ...
    }}
    Тільки JSON, без пояснень.
    """

    response = openai.ChatCompletion.create(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    raw_text = response.choices[0].message.content.strip()

    try:
        movie_data = json.loads(raw_text)
    except json.JSONDecodeError:
        import re
        match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if match:
            movie_data = json.loads(match.group(0))
        else:
            raise ValueError("Не вдалося розпізнати JSON")

    return movie_data

def save_to_json(data: dict, filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Дані збережено в файл {filename}")

if __name__ == "__main__":
    movie_title = "Початок"
    info = get_movie_info(movie_title)
    save_to_json(info, "inception_info.json")
