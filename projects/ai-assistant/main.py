"""
main.py — FastAPI-сервис AI-ассистента. ТВОЯ РАБОТА.

Запуск:  uvicorn main:app --reload   (потом http://localhost:8000/docs)
Тесты:   uv run python test_api.py
"""

from fastapi import FastAPI

from llm import assistant_chat, extract_data
from models import ChatRequest, ChatResponse, ExtractRequest, Contact

app = FastAPI(title="AI Assistant")


# health-check
@app.get("/")
async def root():
    return {"message": "AI Assistant работает"}


# ЗАДАНИЕ 1: POST /chat
#   - принимает тело ChatRequest (в нём поле message)
#   - вызывает assistant_chat(req.message)
#   - возвращает ChatResponse(reply=<ответ модели>)
#   - объяви: @app.post("/chat", response_model=ChatResponse)

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    return ChatResponse(reply=assistant_chat(req.message))

# ЗАДАНИЕ 2: POST /extract/contact
#   - принимает тело ExtractRequest (в нём поле text)
#   - вызывает extract_data(req.text, Contact)  -> вернёт объект Contact
#   - возвращает этот Contact (он и есть response_model)
#   - объяви: @app.post("/extract/contact", response_model=Contact)

@app.post("/extract/contact", response_model=Contact)
async def contact(req : ExtractRequest):
    return extract_data(req.text, Contact)

