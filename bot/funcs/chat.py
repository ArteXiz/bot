from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask(prompt: object, name: object = None, tone: object = None, sys_prompt: object = None, model: object = "openai/gpt-oss-120b") -> str | None:
    chat_completion = client.chat.completions.create(
        messages = [
        {
            "role": "system",
            "content": f"Dont use MarkDown! (like ** and etc) Always respond in Russian unless requested otherwise, but if name and etc in english you can use this only for it. Use more short answers. You are assistant named {name}. Communication tone - {tone}. Additional prompt: {sys_prompt}",
        },
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model = model,
    )
    answer = chat_completion.choices[0].message.content
    return answer
