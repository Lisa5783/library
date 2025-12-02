"""
Интеграционный тест для эндпоинта:
GET /api/books/<book_id>/faculties/<branch_id>
— возвращает список факультетов, использующих книгу в филиале.
"""

import pytest
from app import create_app, db
from app.models import Book, Branch, Faculty, book_faculty


def _create_app():
    """
    Создаём приложение.

    Пытаемся сначала вызвать create_app("testing"),
    если фабрика без аргументов — ловим TypeError и вызываем без параметров.
    """
    try:
        app = create_app("testing")
    except TypeError:
        app = create_app()

    app.config["TESTING"] = True
    app.config.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///:memory:")
    return app


@pytest.fixture(scope="function")
def app():
    app = _create_app()
    with app.app_context():
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
        - JSON с полями "faculties" (список) и "count" (число = 2)
    """
    # --- Подготовка данных ---
    branch = Branch(name="Центральный", location="Москва")
    db.session.add(branch)
    db.session.flush()  # нужно, чтобы появился branch.id

    book = Book(
        title="Основы криптографии",
        authors="Иванов А.",
        publisher="Академия",
        year=2023,
        pages=320,
        illustrations=True,
        cost=850.0,
    )
    db.session.add(book)

    fac1 = Faculty(name="Факультет информационной безопасности", description="...")
    fac2 = Faculty(name="Факультет прикладной математики", description="...")
    db.session.add_all([fac1, fac2])
    db.session.commit()

    # --- Связь книга ↔ факультеты ---
    db.session.execute(
        book_faculty.insert(),
        [
            {"book_id": book.id, "faculty_id": fac1.id},
            {"book_id": book.id, "faculty_id": fac2.id},
        ],
    )
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


def test_api_get_faculties_for_nonexistent_book(client):
    """
    Граничный случай: запрос для несуществующей книги.
    Ожидаем: пустой список, count = 0.
    """
    response = client.get("/api/books/999999/faculties/1")

    assert response.status_code == 200
    data = response.get_json()
    assert data["faculties"] == []
    assert data["count"] == 0


if __name__ == "__main__":
    # Чтобы `python test.py` запускал pytest-тесты
    raise SystemExit(pytest.main([__file__]))


