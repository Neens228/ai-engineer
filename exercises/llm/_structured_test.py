"""Проверка: поддерживает ли Ollama structured outputs через OpenAI SDK (.parse + Pydantic)."""

from openai import OpenAI
from pydantic import BaseModel

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen2.5:7b"


class Person(BaseModel):
    name: str
    age: int
    city: str


completion = client.beta.chat.completions.parse(
    model=MODEL,
    messages=[
        {"role": "system", "content": "Извлеки данные о человеке из текста."},
        {"role": "user", "content": "Игорю 24 года, он живёт в Москве."},
    ],
    response_format=Person,
)

person = completion.choices[0].message.parsed
print("Тип:", type(person))
print("Объект:", person)
print("Поле name:", person.name)
print("Поле age:", person.age, "| тип:", type(person.age))
