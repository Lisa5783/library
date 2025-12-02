# tests/test_api_faculties.py
"""
Интеграционный тест для функции:
GET /api/books/<book_id>/faculties/<branch_id>
— возвращает список факультетов, использующих книгу в филиале.
"""

import pytest
from app import create_app, db
from app.models import Book, Branch, Faculty, book_faculties


@pytest.fixture(scope="function")
def app():
    """Тестовое Flask‑приложение с in‑memory БД."""
    app = create_app("testing")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Тестовый клиент Flask."""
    return app.test_client()


def test_api_get_faculties_for_book_in_branch(client):
    """Проверка списка факультетов для существующей книги и филиала."""
    # Подготовка данных
    branch = Branch(name="Центральный", location="Москва")
    db.session.add(branch)
    db.session.commit()

    book = Book(
        title="Основы криптографии",
        authors="Иванов А.",
        publisher="Академия",
        year=2023,
        pages=320,
        illustrations=True,
        cost=850.0,
        branch_id=branch.id,
    )

    fac1 = Faculty(
        name="Факультет информационной безопасности",
        description="...",
    )
    fac2 = Faculty(
        name="Факультет прикладной математики",
        description="...",
    )

    db.session.add_all([book, fac1, fac2])
    db.session.commit()

    # Связываем книгу с факультетами
    db.session.execute(
        book_faculties.insert(),
        [
            {"book_id": book.id, "faculty_id": fac1.id},
            {"book_id": book.id, "faculty_id": fac2.id},
        ],
    )
    db.session.commit()

    # Выполняем запрос к API
    response = client.get(f"/api/books/{book.id}/faculties/{branch.id}")

    # Проверки
    assert response.status_code == 200
    data = response.get_json()
    assert "faculties" in data
    assert "count" in data
    assert data["count"] == 2

    faculty_names = {f["name"] for f in data["faculties"]}
    assert "Факультет информационной безопасности" in faculty_names
    assert "Факультет прикладной математики" in faculty_names


def test_api_get_faculties_for_nonexistent_book(client):
    """Граничный случай: несуществующая книга – пустой список и count = 0."""
    response = client.get("/api/books/999999/faculties/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["faculties"] == []
    assert data["count"] == 0

