"""
Углубление async — таймауты, обработка ошибок, семафоры (rate limiting).

Формат: условие + примеры. Подсказка — только НАЗВАНИЕ инструмента, решение сам.
Гугли: "asyncio wait_for", "asyncio gather return_exceptions", "asyncio Semaphore".

Запуск:  python async_deep.py
Цель:    "Все проверки пройдены!"
"""

import asyncio
import time


# Вспомогательные «запросы» — НЕ меняй их.
async def fetch_one(name: str, delay: float = 0.3) -> str:
    await asyncio.sleep(delay)
    return f"данные {name}"


async def fetch_or_fail(name: str, delay: float = 0.1) -> str:
    """Падает с ошибкой, если name == 'BAD'."""
    await asyncio.sleep(delay)
    if name == "BAD":
        raise ValueError(f"плохой запрос: {name}")
    return f"данные {name}"


# ============================================================
# ТВОИ ФУНКЦИИ
# ============================================================

async def fetch_with_timeout(name: str, delay: float, timeout: float) -> str:
    """Вернуть результат fetch_one(name, delay).
    НО если запрос идёт дольше timeout секунд — вернуть строку "TIMEOUT".
    fetch_with_timeout("A", 0.1, 0.5) -> "данные A"
    fetch_with_timeout("B", 1.0, 0.2) -> "TIMEOUT"
    Инструмент: asyncio.wait_for (бросает исключение при превышении — поймай его).
    """
    task = asyncio.create_task(fetch_one(name, delay))
    try:
        result = await asyncio.wait_for(task, timeout=timeout)
        return result
    except TimeoutError:
        return "TIMEOUT"



async def fetch_all_safe(names: list[str]) -> list[str]:
    """Запросить все имена ПАРАЛЛЕЛЬНО через fetch_or_fail.
    Если какой-то запрос упал с ошибкой — на его месте в результате должна быть строка "ОШИБКА",
    а остальные результаты — нормальные (весь набор НЕ должен падать).
    Порядок сохраняется.
    fetch_all_safe(["A", "BAD", "C"]) -> ["данные A", "ОШИБКА", "данные C"]
    Инструмент: asyncio.gather(..., return_exceptions=True), потом разобрать результаты.
    """
    coros = [fetch_or_fail(name) for name in names]
    results = await asyncio.gather(*coros, return_exceptions=True)
    final_result = []
    for result in results:
        if isinstance(result, ValueError):
            final_result.append("ОШИБКА")
        else:
            final_result.append(result)
    return final_result

async def fetch_limited(names: list[str], max_concurrent: int) -> list[str]:
    """Запросить все имена через fetch_one, но одновременно — НЕ БОЛЕЕ max_concurrent штук
    (имитация rate limit). Вернуть список данных В ТОМ ЖЕ порядке, что и names.
    Инструмент: asyncio.Semaphore + async with внутри корутины-обёртки, затем gather.
    """
    sem = asyncio.Semaphore(max_concurrent)
    async def worker_with_sem(temp):
        async with sem:
            return await fetch_one(temp)
    
    tasks = [worker_with_sem(name) for name in names]
    result = await asyncio.gather(*tasks)
    return result
    


def _check() -> None:
    # 1) Таймаут
    assert asyncio.run(fetch_with_timeout("A", 0.1, 0.5)) == "данные A"
    assert asyncio.run(fetch_with_timeout("B", 1.0, 0.2)) == "TIMEOUT"

    # 2) Обработка ошибок — порядок сохранён, упавший заменён на "ОШИБКА"
    assert asyncio.run(fetch_all_safe(["A", "BAD", "C"])) == ["данные A", "ОШИБКА", "данные C"]
    assert asyncio.run(fetch_all_safe(["BAD", "BAD"])) == ["ОШИБКА", "ОШИБКА"]

    # 3) Семафор: 6 задач по 0.3с, max_concurrent=2 -> 3 «волны» -> ~0.9с
    start = time.perf_counter()
    result = asyncio.run(fetch_limited(["A", "B", "C", "D", "E", "F"], 2))
    elapsed = time.perf_counter() - start
    assert result == ["данные A", "данные B", "данные C", "данные D", "данные E", "данные F"]
    assert 0.8 < elapsed < 1.15, f"ожидалось ~0.9с (3 волны по 2), получено {elapsed:.2f}с"

    print(f"Семафор: 6 задач по 2 одновременно заняли {elapsed:.2f}с")
    print("Все проверки пройдены!")


if __name__ == "__main__":
    _check()
