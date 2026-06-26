"""
Задание 9 — Асинхронность: async/await, asyncio.gather (Месяц 2).

Идея: fetch_one имитирует запрос к серверу (ждёт через asyncio.sleep).
Сравним ПОСЛЕДОВАТЕЛЬНЫЙ и ПАРАЛЛЕЛЬНЫЙ запуск — и увидим разницу во времени.

fetch_one и fetch_sequential готовы как образец. Реализуй fetch_parallel.

Запуск:  python async_intro.py
Цель:    "Все проверки пройдены!" (и параллельная версия заметно быстрее)
"""

import asyncio
import time


async def fetch_one(name: str, delay: float = 0.3) -> str:
    """Имитация сетевого запроса: подождать delay секунд и вернуть результат.
    await asyncio.sleep(...) — это "ожидание", которое НЕ блокирует другие задачи."""
    await asyncio.sleep(delay)
    return f"данные {name}"


async def fetch_sequential(names: list[str]) -> list[str]:
    """ОБРАЗЕЦ: запросить данные ПО ОЧЕРЕДИ (последовательно).
    Каждый await ждёт завершения предыдущего — медленно."""
    results = []
    for name in names:
        result = await fetch_one(name)      # ждём ОДИН, потом следующий
        results.append(result)
    return results


async def fetch_parallel(names: list[str]) -> list[str]:
    """ЗАДАНИЕ: запросить данные ОДНОВРЕМЕННО (параллельно) через asyncio.gather.
    Результат должен быть таким же списком, как у fetch_sequential, но быстрее.
    HINT:
        coroutines = [fetch_one(name) for name in names]   # список корутин (пока НЕ запущены)
        return await asyncio.gather(*coroutines)           # * распаковывает список в аргументы
    """
    coroutines = [fetch_one(name) for name in names]
    return await asyncio.gather(*coroutines)

def _check() -> None:
    names = ["A", "B", "C", "D"]

    # последовательно
    start = time.perf_counter()
    seq = asyncio.run(fetch_sequential(names))
    seq_time = time.perf_counter() - start

    # параллельно
    start = time.perf_counter()
    par = asyncio.run(fetch_parallel(names))
    par_time = time.perf_counter() - start

    # результаты одинаковы
    assert seq == ["данные A", "данные B", "данные C", "данные D"]
    assert par == ["данные A", "данные B", "данные C", "данные D"]

    # параллельная версия заметно быстрее (4 задачи по 0.3с:
    # последовательно ~1.2с, параллельно ~0.3с)
    assert par_time < seq_time / 2, (
        f"параллельно должно быть быстрее: seq={seq_time:.2f}с, par={par_time:.2f}с"
    )

    print(f"Последовательно: {seq_time:.2f}с | Параллельно: {par_time:.2f}с")
    print("Все проверки пройдены!")


if __name__ == "__main__":
    _check()
