"""Проверки требований к пяти функциям. Каждый тест использует свою папку."""

import shutil

import pytest

from file_operations import (
    append_to_file,
    copy_file,
    read_file,
    search_in_file,
    write_file,
)


@pytest.mark.parametrize("text", ["Привет, Python!\nВторая строка", ""])
def test_read_file_returns_all_text(tmp_path, text):
    path = tmp_path / "текст.txt"
    path.write_text(text, encoding="utf-8")
    assert read_file(str(path)) == text


def test_read_file_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_file(str(tmp_path / "missing.txt"))


def test_read_file_invalid_utf8(tmp_path):
    path = tmp_path / "binary.bin"
    path.write_bytes(b"\xff\xfe\x80")
    with pytest.raises(UnicodeDecodeError):
        read_file(str(path))


@pytest.mark.parametrize("text", ["Новый текст\nВторая строка", ""])
def test_write_file_creates_file(tmp_path, text):
    path = tmp_path / "new.txt"
    assert write_file(str(path), text) is None
    assert path.read_text(encoding="utf-8") == text


@pytest.mark.parametrize("text", ["Короткий текст", ""])
def test_write_file_replaces_existing_content(tmp_path, text):
    path = tmp_path / "existing.txt"
    path.write_text("Старое содержимое, которое необходимо удалить целиком", encoding="utf-8")
    write_file(str(path), text)
    assert path.read_text(encoding="utf-8") == text


def test_write_file_missing_parent(tmp_path):
    with pytest.raises(FileNotFoundError):
        write_file(str(tmp_path / "missing" / "file.txt"), "Текст")


@pytest.mark.parametrize("original, added, expected", [
    ("Первая\n", "Вторая\n", "Первая\nВторая\n"),
    ("Начало", " и конец", "Начало и конец"),
    ("Останется", "", "Останется"),
])
def test_append_preserves_existing_text(tmp_path, original, added, expected):
    path = tmp_path / "notes.txt"
    path.write_text(original, encoding="utf-8")
    assert append_to_file(str(path), added) is None
    assert path.read_text(encoding="utf-8") == expected


def test_append_creates_missing_file(tmp_path):
    path = tmp_path / "new.txt"
    append_to_file(str(path), "Создано добавлением")
    assert path.read_text(encoding="utf-8") == "Создано добавлением"


@pytest.mark.parametrize("content", [b"\x00\xff\x80\r\n", b""])
def test_copy_preserves_bytes_and_source(tmp_path, content):
    source, destination = tmp_path / "source.bin", tmp_path / "copy.bin"
    source.write_bytes(content)
    assert copy_file(str(source), str(destination)) is None
    assert destination.read_bytes() == content
    assert source.read_bytes() == content


def test_copy_replaces_destination(tmp_path):
    source, destination = tmp_path / "source.txt", tmp_path / "copy.txt"
    source.write_bytes(b"new")
    destination.write_bytes(b"old content is longer")
    copy_file(str(source), str(destination))
    assert destination.read_bytes() == b"new"


def test_copy_missing_source(tmp_path):
    destination = tmp_path / "copy.txt"
    with pytest.raises(FileNotFoundError):
        copy_file(str(tmp_path / "missing.txt"), str(destination))
    assert not destination.exists()


def test_copy_to_same_file(tmp_path):
    path = tmp_path / "same.txt"
    path.write_bytes(b"keep this")
    with pytest.raises(shutil.SameFileError):
        copy_file(str(path), str(path))
    assert path.read_bytes() == b"keep this"


def test_search_line_numbers_start_at_one(tmp_path):
    # Подготовка: создаём файл независимо от проверяемого модуля.
    path = tmp_path / "text.txt"
    path.write_text("Python\nJava\nPython снова\n", encoding="utf-8")
    # Действие: вызываем функцию поиска.
    result = search_in_file(str(path), "Python")
    # Проверка: номера строк должны совпадать с обычной нумерацией с 1.
    assert result == [(1, "Python"), (3, "Python снова")]


def test_search_is_case_sensitive(tmp_path):
    path = tmp_path / "text.txt"
    path.write_text("Python\npython\nPYTHON\n", encoding="utf-8")
    assert search_in_file(str(path), "python") == [(2, "python")]


@pytest.mark.parametrize("text", ["Нет нужного слова\n", ""])
def test_search_no_matches(tmp_path, text):
    path = tmp_path / "text.txt"
    path.write_text(text, encoding="utf-8")
    assert search_in_file(str(path), "Python") == []


def test_search_rejects_empty_query(tmp_path):
    path = tmp_path / "text.txt"
    path.write_text("Текст", encoding="utf-8")
    with pytest.raises(ValueError, match="не должен быть пустым"):
        search_in_file(str(path), "")


def test_search_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        search_in_file(str(tmp_path / "missing.txt"), "Python")


def test_search_preserves_spaces_and_returns_line_once(tmp_path):
    path = tmp_path / "text.txt"
    path.write_text("  Python и Python  \n", encoding="utf-8")
    assert search_in_file(str(path), "Python") == [(1, "  Python и Python  ")]


def test_search_last_line_without_newline(tmp_path):
    path = tmp_path / "text.txt"
    path.write_text("Начало\nПоследняя строка", encoding="utf-8")
    assert search_in_file(str(path), "строка") == [(2, "Последняя строка")]
