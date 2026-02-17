from groq import Groq
import os
import random
from dotenv import load_dotenv

load_dotenv()

secret_word = None

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_word(model: object = "llama-3.3-70b-versatile"):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"Выведи одно случайное существительное русского языка в именительном падеже. Только кириллица. Только одно слово. Без точек, без пробелов, без кавычек."
            },
            {
                "role": "user",
                "content": f"Сид: {random.randint(0,99999999999999999)}"
            }
        ],
        model = model,
        temperature=1.5
    )
    return chat_completion.choices[0].message.content

def rate_range(guessed_word: object, real_word: object, sys_prompt: object = None, model: object = "qwen/qwen3-32b") -> str | None:
    chat_completion = client.chat.completions.create(
        messages = [
        {
            "role": "system",
            #промпт от нейронки (для игры который промпт)
            "content": """
Оцени смысловую близость двух русских слов числом от 0 до 100.

Шкала:
95-100: синонимы (собака, пёс)
80-94: очень близкие (собака, волк)  
60-79: одна тема (собака, кошка)
40-59: косвенная связь (собака, поводок)
20-39: слабая связь (собака, дерево)
1-19: едва уловимая (собака, алгебра)
0: нет связи вообще

Топор, кирка → 75
Топор, дерево → 55
Топор, нож → 70

Ответь ТОЛЬКО числом."""

        },
        {
            "role": "user",
            "content":  f"{real_word}, {guessed_word}",
        }
    ],
    model = model,
    temperature=0.6,
    reasoning_format="hidden"
    )
    answer = chat_completion.choices[0].message.content
    return answer
