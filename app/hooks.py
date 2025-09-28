# app/hooks.py
"""
SQLAlchemy хуки и события для системы управления библиотекой
"""

from sqlalchemy import event
from sqlalchemy.inspection import inspect
from app import db
from app.models import Book, Branch, Faculty, AuditLog
import json
from datetime import datetime

def register_hooks():
    """
    Регистрация всех хуков SQLAlchemy
    """
    register_audit_hooks()
    register_validation_hooks()
    register_automation_hooks()
    print("SQLAlchemy хуки зарегистрированы")

def register_audit_hooks():
    """
    Регистрация хуков для аудита изменений
    """
    @event.listens_for(Book, 'after_insert')
    def book_after_insert(mapper, connection, target):
        create_audit_log(connection, 'book', target.id, 'INSERT', None, target.to_dict())

    @event.listens_for(Book, 'after_update')
    def book_after_update(mapper, connection, target):
        old_values = {}
        for attr in inspect(target).attrs:
            hist = attr.load_history()
            if hist.has_changes():
                old_values[attr.key] = hist.deleted[0] if hist.deleted else None
        create_audit_log(connection, 'book', target.id, 'UPDATE', old_values, target.to_dict())

    @event.listens_for(Book, 'after_delete')
    def book_after_delete(mapper, connection, target):
        create_audit_log(connection, 'book', target.id, 'DELETE', target.to_dict(), None)

    @event.listens_for(Branch, 'after_insert')
    def branch_after_insert(mapper, connection, target):
        create_audit_log(connection, 'branch', target.id, 'INSERT', None, target.to_dict())

    @event.listens_for(Branch, 'after_update')
    def branch_after_update(mapper, connection, target):
        old_values = {}
        for attr in inspect(target).attrs:
            hist = attr.load_history()
            if hist.has_changes():
                old_values[attr.key] = hist.deleted[0] if hist.deleted else None
        create_audit_log(connection, 'branch', target.id, 'UPDATE', old_values, target.to_dict())

    @event.listens_for(Branch, 'after_delete')
    def branch_after_delete(mapper, connection, target):
        create_audit_log(connection, 'branch', target.id, 'DELETE', target.to_dict(), None)

def register_validation_hooks():
    """
    Регистрация хуков для валидации данных
    """
    @event.listens_for(Book, 'before_insert')
    @event.listens_for(Book, 'before_update')
    def validate_book(mapper, connection, target):
        from app.exceptions import ValidationError
        current_year = datetime.now().year
        if target.year < 1000 or target.year > current_year + 1:
            raise ValidationError(f"Недопустимый год издания: {target.year}")
        if target.pages <= 0:
            raise ValidationError("Количество страниц должно быть больше нуля")
        if target.cost < 0:
            raise ValidationError("Стоимость не может быть отрицательной")
        if target.copies_available < 0:
            raise ValidationError("Количество экземпляров не может быть отрицательным")

    @event.listens_for(Branch, 'before_insert')
    @event.listens_for(Branch, 'before_update')
    def validate_branch(mapper, connection, target):
        from app.exceptions import ValidationError
        if not target.name or target.name.strip() == '':
            raise ValidationError("Название филиала не может быть пустым")
        if not target.location or target.location.strip() == '':
            raise ValidationError("Адрес филиала не может быть пустым")

def register_automation_hooks():
    """
    Регистрация хуков для автоматических действий
    """
    @event.listens_for(Book.times_issued, 'set')
    def update_book_popularity(target, value, oldvalue, initiator):
        # Проверяем, что oldvalue — число
        if not isinstance(oldvalue, int):
            return
        if value is not None and oldvalue is not None and value > oldvalue:
            print(f"Книга '{target.title}' стала популярнее: {value} выдач")

    @event.listens_for(Book.copies_available, 'set')
    def check_book_availability(target, value, oldvalue, initiator):
        # Проверяем, что oldvalue — число
        if not isinstance(oldvalue, int):
            return
        if value is not None and value <= 0 and oldvalue > 0:
            print(f"ВНИМАНИЕ: Закончились экземпляры книги '{target.title}'")
        elif value is not None and value > 0 and oldvalue <= 0:
            print(f"Книга '{target.title}' снова доступна ({value} экз.)")

    @event.listens_for(db.session, 'before_commit')
    def before_commit(session):
        for obj in session.dirty:
            if hasattr(obj, 'updated_at'):
                obj.updated_at = datetime.utcnow()

    @event.listens_for(db.session, 'after_commit')
    def after_commit(session):
        print("Изменения успешно сохранены в базе данных")

    @event.listens_for(db.session, 'after_rollback')
    def after_rollback(session):
        print("Транзакция отменена, изменения не сохранены")

def create_audit_log(connection, table_name, record_id, action, old_values, new_values):
    """
    Создание записи в журнале аудита
    """
    try:
        old_json = json.dumps(old_values, default=str, ensure_ascii=False) if old_values else None
        new_json = json.dumps(new_values, default=str, ensure_ascii=False) if new_values else None
        insert_stmt = """
            INSERT INTO audit_log (table_name, record_id, action, old_values, new_values, timestamp)
            VALUES (:table_name, :record_id, :action, :old_values, :new_values, :timestamp)
        """
        connection.execute(
            db.text(insert_stmt),
            {
                "table_name": table_name,
                "record_id": record_id,
                "action": action,
                "old_values": old_json,
                "new_values": new_json,
                "timestamp": datetime.utcnow()
            }
        )
    except Exception as e:
        print(f"Ошибка при создании записи аудита: {e}")

@event.listens_for(Book, 'before_delete')
def prevent_book_deletion_if_issued(mapper, connection, target):
    if target.times_issued > target.copies_available:
        from app.exceptions import ValidationError
        raise ValidationError(
            f"Невозможно удалить книгу '{target.title}' - есть выданные экземпляры"
        )

@event.listens_for(Branch, 'before_delete')
def prevent_branch_deletion_if_has_books(mapper, connection, target):
    if target.books.count() > 0:
        from app.exceptions import ValidationError
        raise ValidationError(
            f"Невозможно удалить филиал '{target.name}' - в нем есть книги"
        )
