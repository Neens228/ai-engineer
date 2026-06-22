"""
main.py — точка входа: CLI-цикл для менеджера задач.

Это верхний слой: общается с пользователем и вызывает функции из storage.py.
Сам он НЕ лезет в базу напрямую — только через storage. Это и есть разделение слоёв.

Запуск (из папки projects/task-cli):
    python main.py

Команды:
    add <текст>   — добавить задачу
    list          — показать все задачи
    done <номер>  — отметить выполненной
    exit          — выйти
"""

from storage import init_db, add_task, get_all_tasks, mark_done


def print_tasks() -> None:
    """Вывести все задачи. Формат строки: "[x] 1. Купить молоко" или "[ ] 2. ...".
    Шаги:
      - tasks = get_all_tasks()
      - если список пуст — напечатать "Список задач пуст." и выйти из функции (return)
      - иначе для каждой задачи напечатать строку:
          галочка = "[x]" если task.done иначе "[ ]"
          строка  = f"{галочка} {task.id}. {task.title}"
    """
    tasks = get_all_tasks()
    if not tasks:
        print("Список задач пуст.")
        return
    else:
        for task in tasks:
            mark = "[x]" if task.done else "[ ]"
            string = f"{mark} {task.id}. {task.title}"
            print(string)

def main() -> None:
    init_db()                       # создаём таблицу при старте, если её нет
    print("Менеджер задач. Команды: add <текст>, list, done <номер>, exit")

    while True:                     # бесконечный цикл, пока не введут exit
        command = input("> ").strip()

        if command == "exit":
            print("Пока!")
            break

        elif command == "list":
            print_tasks()

        elif command.startswith("add "):
            # текст задачи — это всё, что после "add "
            # TODO: если title не пустой — добавить через add_task(title)
            #       и напечатать f"Задача #{task.id} добавлена."
            #       иначе напечатать "Текст задачи пустой."

            title = command[len("add "):].strip()
            if len(title) > 0:
                task = add_task(title)
                print(f"Задача #{task.id} добавлена.")
            else:
                print("Текст задачи пустой.")


        elif command.startswith("done "):
            # номер задачи — после "done "
            number_text = command[len("done "):].strip()
            # TODO:
            #   1) превратить number_text в число через int(...), поймав ValueError
            #      (если не число — напечатать "Нужен номер задачи." и continue)
            #   2) вызвать mark_done(номер)
            #   3) напечатать f"Задача #{номер} выполнена."
            try:
                mark_done(int(number_text))
                print(f"Задача #{number_text} выполнена.")
            except ValueError:
                print("Нужен номер задачи.")
                continue

        else:
            print("Неизвестная команда. Доступно: add, list, done, exit")


if __name__ == "__main__":
    main()
