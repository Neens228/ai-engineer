# AI Assistant Service

REST API-сервис поверх LLM: ассистент с вызовом инструментов и извлечение структурированных данных.
Второй AI-проект на пути к AI Engineer. Демонстрирует интеграцию FastAPI + LLM.

## Возможности
- `POST /chat` — ассистент с **tool calling** (модель сама решает вызвать инструменты: калькулятор, время)
- `POST /extract/contact` — **structured output**: из свободного текста → строгий JSON (`name`, `email`, `phone`)
- Автодокументация Swagger на `/docs`
- Автотесты эндпоинтов (`TestClient`)

## Стек
- **Python 3.13**, **FastAPI**, **Pydantic**
- **OpenAI SDK** (OpenAI-совместимый интерфейс)
- **LLM:** Qwen 2.5 7B локально через **Ollama** (код без изменений работает с OpenAI — меняется только `base_url`)

## Архитектура (разделение ответственности)
| Файл | Слой | Ответственность |
|------|------|-----------------|
| `tools.py` | Инструменты | функции ассистента + их описания для модели |
| `llm.py` | AI-ядро | `assistant_chat()` (tool-calling цикл), `extract_data()` (structured output). Не знает про HTTP |
| `models.py` | Схемы | Pydantic-модели запросов/ответов |
| `main.py` | API | FastAPI-эндпоинты, вызывают `llm.py` |
| `test_api.py` | Тесты | проверка эндпоинтов через `TestClient` |

AI-логика полностью отделена от HTTP-слоя — можно тестировать и менять независимо.

## Запуск
```bash
# нужен запущенный Ollama с моделью qwen2.5:7b
uvicorn main:app --reload
# документация: http://localhost:8000/docs
```

### Примеры
```bash
# ассистент (сам вызовет калькулятор)
curl -X POST localhost:8000/chat -H "Content-Type: application/json" \
     -d '{"message": "Сколько будет 15 умножить на 4?"}'
# -> {"reply": "15 умножить на 4 будет равно 60."}

# извлечение контакта
curl -X POST localhost:8000/extract/contact -H "Content-Type: application/json" \
     -d '{"text": "Свяжитесь с Иваном Петровым: ivan@example.com, +7 999 123-45-67"}'
# -> {"name": "Иван Петров", "email": "ivan@example.com", "phone": "+7 999 123-45-67"}
```

## Тесты
```bash
python test_api.py
```

## Что демонстрирует проект
- Интеграция LLM в веб-сервис (production-паттерн: AI как API)
- Tool calling (агентный цикл) и structured outputs (надёжный JSON)
- Чистая слоистая архитектура
- Тестирование недетерминированных LLM-эндпоинтов
