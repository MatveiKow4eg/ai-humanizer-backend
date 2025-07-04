from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from fastapi.middleware.cors import CORSMiddleware

# OpenRouter + DeepSeek через новую библиотеку openai>=1.0.0
client = openai.OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

@app.post("/analyze")
async def analyze_text(data: TextRequest):
    prompt = f"""
Анализируй следующий текст на русском языке:
{data.text}
1. Оцени человечность от 0 до 100.
2. Объясни, какие части кажутся написанными ИИ (и почему).
3. Подчеркни подозрительные фрагменты в тексте.
4. Перепиши текст, сделав его максимально человечным, дружелюбным и эмоциональным.
Ответ верни в JSON:
{{
  "score": int,
  "reasons": ["..."],
  "highlights": ["..."],
  "rewrite": "..."
}}
"""
    response = client.chat.completions.create(
        model="deepseek-chat",  # или "deepseek-coder"
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return eval(response.choices[0].message.content)
