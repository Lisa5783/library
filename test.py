# tests/test_api_faculties.py
"""
Интеграционный тест для специальной функции:
GET /api/books/<book_id>/faculties/<branch_id>
— возвращает список факультетов, использующих книгу в филиале.

Соответствует пункту из README.md:
> "Подсчет количества факультетов, использующих книгу в филиале"
> "Вывод названий факультетов, использующих книгу"
"""

import pytest
from app import create_app, db
from app.models import Book, Branch, Faculty, BookFaculty


@pytest.fixture(scope="function")
def app():
    """
    Фикстура: тестовое Flask-приложение с тестовой БД.

    ВАЖНО:
    - предполагается, что в create_app("testing") уже прописана
      тестовая конфигурация (TestingConfig) с sqlite:///:memory:
    """
    app = create_app("testing")

    # Явно говорим Flask'у, что мы в режиме тестирования
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        try:
            yield app
        finally:
            db.session.remove()
            db.drop_all()


@pytest.fixture
def client(app):
    """Фикстура: тестовый клиент Flask."""
    return app.test_client()


def test_api_get_faculties_for_book_in_branch(client):
    """
    Тестируемый модуль: app.api.books (эндпоинт /api/books/<book_id>/faculties/<branch_id>)
    Цель: Проверить корректность возвращаемого списка факультетов.

    Тестовые данные:
        - Книга: "Основы криптографии", автор Иванов А.
        - Филиал: "Центральный"
        - Факультеты:
            1. "Факультет информационной безопасности"
            2. "Факультет прикладной математики"

    Ожидаемый результат:
        - HTTP 200
        - JSON с полями "faculties" (список) и "count" (число = 2)
        - Оба факультета присутствуют в ответе
    """
    # --- Подготовка данных в БД ---
    branch = Branch(name="Центральный", location="Москва")
    db.session.add(branch)
    db.session.flush()  # чтобы у branch появился id, но без commit

    book = Book(
        title="Основы криптографии",
        authors="Иванов А.",
        publisher="Академия",
        year=2023,
        pages=320,
        illustrations=True,
        cost=850.0,
        # ВАЖНО: привяжем книгу к филиалу, раз эндпоинт по логике работает "в рамках филиала"
        branch_id=branch.id,
    )

    fac1 = Faculty(name="Факультет информационной безопасности", description="...")
    fac2 = Faculty(name="Факультет прикладной математики", description="...")

    db.session.add_all([book, fac1, fac2])
    db.session.commit()

    # --- Связываем книгу с факультетами через таблицу связей ---
    # предполагается, что BookFaculty — модель-обертка вокруг таблицы связей
    # Если у тебя там по-другому (например, просто db.Table), можно заменить
    # на явное создание объектов BookFaculty(...)
    db.session.execute(
        BookFaculty.table.insert(),
        [
            {"book_id": book.id, "faculty_id": fac1.id},
            {"book_id": book.id, "faculty_id": fac2.id},
        ],
    )
    db.session.commit()

    # --- Вызов тестируемого API ---
    response = client.get(f"/api/books/{book.id}/faculties/{branch.id}")

    # --- Проверки ---
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, dict)

    assert "faculties" in data
    assert "count" in data

    assert isinstance(data["faculties"], list)
    assert data["count"] == 2

    faculty_names = {f["name"] for f in data["faculties"]}
    assert "Факультет информационной безопасности" in faculty_names
    assert "Факультет прикладной математики" in faculty_names


def test_api_get_faculties_for_nonexistent_book(client):
    """
    Граничный случай: запрос для несуществующей книги.
    Ожидаемый результат: пустой список, count = 0.
    """
    # Берём заведомо несуществующий id книги и какой-нибудь branch_id
    response = client.get("/api/books/999999/faculties/1")

    assert response.status_code == 200
    data = response.get_json()

    assert "faculties" in data
    assert "count" in data

    assert data["faculties"] == []
    assert data["count"] == 0

