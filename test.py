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
    Создаем приложение без режима 'testing',
    потому что в проекте НЕТ конфигурации TestingConfig.
    """
    app = create_app()  # вызываем без аргументов

    app.config["TESTING"] = True
    # Переназначаем БД для тестов
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
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
    branch = Branch(name="Центральный", location="Москва")
    db.session.add(branch)
    db.session.flush()

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

    # Если в модели Book есть relationship faculties — используем его
    book.faculties.append(fac1)
    book.faculties.append(fac2)

    db.session.commit()

    response = client.get(f"/api/books/{book.id}/faculties/{branch.id}")

    assert response.status_code == 200
    data = response.get_json()

    assert data["count"] == 2
    names = {f["name"] for f in data["faculties"]}
    assert "Факультет информационной безопасности" in names
    assert "Факультет прикладной математики" in names


def test_api_get_faculties_for_nonexistent_book(client):
    response = client.get("/api/books/999999/faculties/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["faculties"] == []
    assert data["count"] == 0


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))




