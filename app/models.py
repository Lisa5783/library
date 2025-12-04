# app/models.py
"""
Модели базы данных для системы управления библиотекой
"""

from datetime import datetime
from app import db
from sqlalchemy import event

# Связь многие-ко-многим для книг и факультетов
book_faculties = db.Table(
    'book_faculties',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('faculty_id', db.Integer, db.ForeignKey('faculty.id'), primary_key=True)
)

class Book(db.Model):
    """Модель книги"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    authors = db.Column(db.Text, nullable=False)
    publisher = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    illustrations = db.Column(db.Integer, default=0)
    cost = db.Column(db.Float, nullable=False)
    copies_available = db.Column(db.Integer, default=1)
    times_issued = db.Column(db.Integer, default=0)
    genre = db.Column(db.String(50), nullable=True)


    # Внешний ключ на филиал
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)

    # Связи
    branch = db.relationship('Branch', back_populates='books')
    faculties = db.relationship('Faculty', secondary=book_faculties, back_populates='books')

    # Метаданные
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Book {self.title}>'

    def to_dict(self):
        """Преобразование в словарь для JSON API"""
        return {
            'id': self.id,
            'title': self.title,
            'authors': self.authors,
            'publisher': self.publisher,
            'year': self.year,
            'pages': self.pages,
            'illustrations': self.illustrations,
            'cost': self.cost,
            'copies_available': self.copies_available,
            'times_issued': self.times_issued,
            'branch_id': self.branch_id,
            'branch_name': self.branch.name if self.branch else None,
            'faculties': [faculty.name for faculty in self.faculties],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @classmethod
    def count_copies_in_branch(cls, book_id, branch_id):
        """Подсчитать количество экземпляров книги в филиале"""
        book = cls.query.filter_by(id=book_id, branch_id=branch_id).first()
        return book.copies_available if book else 0

    @classmethod
    def count_faculties_in_branch(cls, book_id, branch_id):
        """Подсчитать количество факультетов, использующих книгу в филиале"""
        book = cls.query.filter_by(id=book_id, branch_id=branch_id).first()
        return len(book.faculties) if book else 0

    @classmethod
    def get_faculties_for_book_in_branch(cls, book_id, branch_id):
        """Получить список факультетов, использующих книгу в филиале"""
        book = cls.query.filter_by(id=book_id, branch_id=branch_id).first()
        return [faculty.name for faculty in book.faculties] if book else []


class Branch(db.Model):
    """Модель филиала библиотеки"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True, index=True)
    location = db.Column(db.String(500), nullable=False)

    # Связи
    books = db.relationship('Book', back_populates='branch', lazy='dynamic')

    # Метаданные
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Branch {self.name}>'

    def to_dict(self):
        """Преобразование в словарь для JSON API"""
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            # 'books_count': self.books.count(),  # УДАЛЕНО! Не используйте здесь!
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Faculty(db.Model):
    """Модель факультета"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True, index=True)
    description = db.Column(db.Text)

    # Связи
    books = db.relationship('Book', secondary=book_faculties, back_populates='faculties')

    # Метаданные
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Faculty {self.name}>'

    def to_dict(self):
        """Преобразование в словарь для JSON API"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            # 'books_count': len(self.books),  # Можно оставить, но лучше убрать из хуков!
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class AuditLog(db.Model):
    """Модель журнала аудита для отслеживания изменений"""

    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(50), nullable=False)
    record_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(10), nullable=False)  # INSERT, UPDATE, DELETE
    old_values = db.Column(db.Text)  # JSON строка с предыдущими значениями
    new_values = db.Column(db.Text)  # JSON строка с новыми значениями
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<AuditLog {self.table_name}:{self.record_id} {self.action}>'
