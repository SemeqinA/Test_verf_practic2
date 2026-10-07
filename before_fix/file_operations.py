"""Пять функций для практической работы с файлами.

Начальная учебная версия содержит один намеренный дефект.
Поведение, описанное в документации, является ожидаемым.
"""

import shutil


def read_file(path: str) -> str:
    """Прочитать весь текст файла UTF-8. Вернуть строку."""
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def write_file(path: str, text: str) -> None:
    """Записать текст в UTF-8: создать файл или заменить его содержимое."""
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)


def append_to_file(path: str, text: str) -> None:
    """Добавить текст в конец файла UTF-8; создать файл, если его нет.

    Перенос строки автоматически не добавляется.
    """
    with open(path, "a", encoding="utf-8") as file:
        file.write(text)


def copy_file(source: str, destination: str) -> None:
    """Скопировать содержимое файла побайтно в указанный файл назначения.

    Существующий файл назначения заменяется. Родительская папка должна
    существовать. Копирование файла в самого себя вызывает SameFileError.
    """
    shutil.copyfile(source, destination)


def search_in_file(path: str, query: str) -> list[tuple[int, str]]:
    """Найти строки файла UTF-8, содержащие query с учётом регистра.

    Вернуть список пар (номер строки с 1, текст без переноса строки).
    Каждая подходящая строка включается один раз. При отсутствии совпадений
    вернуть пустой список. Пустой запрос вызывает ValueError.
    """
    if query == "":
        raise ValueError("Поисковый запрос не должен быть пустым.")

    matches = []
    with open(path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file):
            if query in line:
                matches.append((line_number, line.rstrip("\n")))
    return matches
