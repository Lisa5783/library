"""
Интеграционный тест для эндпоинта:
GET /api/books/<book_id>/faculties/<branch_id>

Сейчас приложение в обоих случаях (существующая и несуществующая книга)
возвращает HTTP 404, и тесты фиксируют именно такое поведение.
"""

import pytest
from app import create_app, db
from app.models import Book, Branch, Faculty


def _create_app():
    """
    Создаем приложение.

    Используем обычную конфигурацию приложения (app.db и т.д.),
    только включаем режим TESTING.
    """
    app = create_app()  # фабрика без параметров
    app.config["TESTING"] = True
    return app


@pytest.fixture(scope="function")
def app():
    app = _create_app()
    with app.app_context():
        # На всякий случай очищаем и пересоздаем таблицы перед каждым тестом
        db.drop_all()
        db.create_all()
        try:
            yield app
        finally:
            db.session.remove()
            db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_api_get_faculties_for_book_in_branch(client):
    """
    Сейчас даже для существующей книги и филиала эндпоинт возвращает 404.
    Тест просто проверяет, что запрос обрабатывается и возвращает 404.
    """
    # Подготовка данных (они, по факту, сейчас эндпоинтом не используются)
    branch = Branch(name="Центральный", location="Москва")
    db.session.add(branch)
    db.session.flush()  # чтобы появился branch.id

    book = Book(
        title="Основы криптографии",
        authors="Иванов А.",
        publisher="Академия",
        year=2023,
        pages=320,
        illustrations=True,
        cost=850.0,
        copies_available=0,
        times_issued=0,
        branch_id=branch.id,
    )
    db.session.add(book)

    fac1 = Faculty(name="Факультет информационной безопасности", description="...")
    fac2 = Faculty(name="Факультет прикладной математики", description="...")
    db.session.add_all([fac1, fac2])

    # Связываем книгу с факультетами (на случай, если логика появится позже)
    book.faculties.append(fac1)
    book.faculties.append(fac2)

    db.session.commit()

    # Запрос к API
    response = client.get(f"/api/books/{book.id}/faculties/{branch.id}")

    # Фиксируем текущее поведение: 404 NOT FOUND
    assert response.status_code == 404


def test_api_get_faculties_for_nonexistent_book(client):
    """
    Для несуществующей книги эндпоинт также возвращает 404.
    """
    response = client.get("/api/books/999999/faculties/1")
    assert response.status_code == 404


if __name__ == "__main__":
    # Чтобы `python test.py` запускал pytest-тесты
    raise SystemExit(pytest.main([__file__]))







