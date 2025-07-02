from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from fastapi.middleware.cors import CORSMiddleware

# Получаем ключ из переменной окружения
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Разрешаем CORS (чтобы фронтенд мог обращаться)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Структура запроса
class TextRequest(BaseModel):
    text: str

# Эндпоинт анализа текста
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
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    content = response.choices[0].message.content
    return eval(content)
