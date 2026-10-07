"""Консольное меню учебной программы. Запуск: python main.py."""

from pathlib import Path

from file_operations import (
    append_to_file,
    copy_file,
    read_file,
    search_in_file,
    write_file,
)


def ask_path(prompt: str) -> str:
    """Получить непустой путь; разрешить вставку пути в двойных кавычках."""
    path = input(prompt).strip().strip('"')
    if not path.strip():
        raise ValueError("Путь к файлу не должен быть пустым.")
    return path


def confirm_overwrite(path: str) -> bool:
    """Запросить подтверждение замены существующего файла."""
    if not Path(path).exists():
        return True
    answer = input("Файл уже существует. Заменить его содержимое? (да/нет): ")
    return answer.strip().lower() == "да"


def main() -> None:
    print("Программа для работы с файлами")
    print(f"Рабочая папка: {Path.cwd()}")
    print("Чтение, запись и поиск: текстовые файлы UTF-8.")

    while True:
        print("\n1. Прочитать файл")
        print("2. Записать текст (создать или перезаписать файл)")
        print("3. Добавить текст в конец файла")
        print("4. Скопировать файл")
        print("5. Найти текст в файле")
        print("0. Выход")

        try:
            choice = input("Выбери действие: ").strip()
            if choice == "0":
                print("Программа завершена.")
                return
            if choice not in {"1", "2", "3", "4", "5"}:
                print("Введи номер от 0 до 5.")
                continue

            path = ask_path("Путь к файлу: ")

            if choice == "1":
                text = read_file(path)
                print("\nСодержимое файла:")
                print(text if text else "[Файл пуст]")
            elif choice == "2":
                if not confirm_overwrite(path):
                    print("Запись отменена.")
                    continue
                text = input("Введи строку текста: ")
                write_file(path, text + "\n")
                print("Текст записан.")
            elif choice == "3":
                text = input("Введи текст для добавления: ")
                append_to_file(path, text + "\n")
                print("Текст добавлен.")
            elif choice == "4":
                destination = ask_path("Путь к новому файлу (включая имя): ")
                if not confirm_overwrite(destination):
                    print("Копирование отменено.")
                    continue
                copy_file(path, destination)
                print("Файл скопирован.")
            elif choice == "5":
                query = input("Какой текст найти? ")
                matches = search_in_file(path, query)
                if matches:
                    for line_number, text in matches:
                        print(f"Строка {line_number}: {text}")
                    print(f"Найдено строк: {len(matches)}")
                else:
                    print("Совпадений нет.")
        except UnicodeError:
            print("Ошибка: для этой операции нужен текстовый файл в UTF-8.")
        except (OSError, ValueError) as error:
            print(f"Ошибка: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nПрограмма завершена.")
            return


if __name__ == "__main__":
    main()
