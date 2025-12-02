"""
Интеграционный тест для эндпоинта:
GET /api/books/<book_id>/faculties/<branch_id>
— возвращает список факультетов, использующих книгу в филиале.
"""

import pytest
from app import create_app, db
from app.models import Book, Branch, Faculty


def _create_app():
    """
    Создаем приложение.

    ВАЖНО: не трогаем SQLALCHEMY_DATABASE_URI, чтобы использовать обычную app.db,
    иначе in-memory SQLite изолирует данные между соединениями.
    """
    app = create_app()  # фабрика без параметров
    app.config["TESTING"] = True
    return app


@pytest.fixture(scope="function")
def app():
    app = _create_app()
    with app.app_context():
        # Полностью пересоздаём таблицы перед каждым тестом
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
    Ожидаем:
      - HTTP 200
      - count == 2
      - в списке два нужных факультета
    """
    # --- Подготовка данных ---
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
        copies_available=0,   # важно для хука валидации
        times_issued=0,       # безопасное значение
        branch_id=branch.id,  # книга относится к этому филиалу
    )
    db.session.add(book)

    fac1 = Faculty(name="Факультет информационной безопасности", description="...")
    fac2 = Faculty(name="Факультет прикладной математики", description="...")
    db.session.add_all([fac1, fac2])

    # Связываем книгу с факультетами через relationship
    book.faculties.append(fac1)
    book.faculties.append(fac2)

    db.session.commit()

    # --- Запрос к API ---
    response = client.get(f"/api/books/{book.id}/faculties/{branch.id}")

    # --- Проверки ---
    assert response.status_code == 200
    data = response.get_json()

    assert "faculties" in data
    assert "count" in data
    assert isinstance(data["faculties"], list)
    assert data["count"] == 2

    names = {f["name"] for f in data["faculties"]}
    assert "Факультет информационной безопасности" in names
    assert "Факультет прикладной математики" in names


def test_api_get_faculties_for_nonexistent_boo






