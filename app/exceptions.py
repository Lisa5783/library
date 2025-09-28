# app/exceptions.py
"""
Пользовательские исключения и обработчики ошибок для системы управления библиотекой
"""

from flask import render_template, request, jsonify
from werkzeug.exceptions import HTTPException
import logging


class LibraryBaseException(Exception):
    """Базовое исключение для системы библиотеки"""
    
    def __init__(self, message, status_code=500, payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        """Преобразование исключения в словарь для JSON ответа"""
        result = dict(self.payload or ())
        result['error'] = self.message
        result['status_code'] = self.status_code
        return result


class BookNotFoundError(LibraryBaseException):
    """Исключение: книга не найдена"""
    
    def __init__(self, book_id=None, message=None):
        if message is None:
            message = f"Книга с ID {book_id} не найдена" if book_id else "Книга не найдена"
        super().__init__(message, status_code=404)
        self.book_id = book_id


class BranchNotFoundError(LibraryBaseException):
    """Исключение: филиал не найден"""
    
    def __init__(self, branch_id=None, message=None):
        if message is None:
            message = f"Филиал с ID {branch_id} не найден" if branch_id else "Филиал не найден"
        super().__init__(message, status_code=404)
        self.branch_id = branch_id


class FacultyNotFoundError(LibraryBaseException):
    """Исключение: факультет не найден"""
    
    def __init__(self, faculty_id=None, message=None):
        if message is None:
            message = f"Факультет с ID {faculty_id} не найден" if faculty_id else "Факультет не найден"
        super().__init__(message, status_code=404)
        self.faculty_id = faculty_id


class ValidationError(LibraryBaseException):
    """Исключение: ошибка валидации данных"""
    
    def __init__(self, message, field=None):
        super().__init__(message, status_code=400)
        self.field = field


class DuplicateEntryError(LibraryBaseException):
    """Исключение: дублирование записи"""
    
    def __init__(self, message, field=None):
        super().__init__(message, status_code=409)
        self.field = field


class InsufficientCopiesError(LibraryBaseException):
    """Исключение: недостаточно экземпляров книги"""
    
    def __init__(self, book_title, requested, available):
        message = f"Недостаточно экземпляров книги '{book_title}'. Запрошено: {requested}, доступно: {available}"
        super().__init__(message, status_code=409)
        self.book_title = book_title
        self.requested = requested
        self.available = available


class DatabaseConnectionError(LibraryBaseException):
    """Исключение: ошибка подключения к базе данных"""
    
    def __init__(self, message="Ошибка подключения к базе данных"):
        super().__init__(message, status_code=500)


class PermissionDeniedError(LibraryBaseException):
    """Исключение: доступ запрещен"""
    
    def __init__(self, message="Доступ запрещен"):
        super().__init__(message, status_code=403)


def register_error_handlers(app):
    """
    Регистрация обработчиков ошибок в Flask приложении
    
    Args:
        app: Экземпляр Flask приложения
    """
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Обработчик ошибки 404"""
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Ресурс не найден',
                'message': 'Запрашиваемый ресурс не существует',
                'status_code': 404
            }), 404
        return render_template('errors/404.html', title='Страница не найдена'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Обработчик внутренних ошибок сервера"""
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Внутренняя ошибка сервера',
                'message': 'Произошла непредвиденная ошибка',
                'status_code': 500
            }), 500
        return render_template('errors/500.html', title='Ошибка сервера'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        """Обработчик ошибки 403"""
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Доступ запрещен',
                'message': 'У вас нет прав для выполнения этого действия',
                'status_code': 403
            }), 403
        return render_template('errors/403.html', title='Доступ запрещен'), 403
    
    @app.errorhandler(400)
    def bad_request_error(error):
        """Обработчик ошибки 400"""
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Неверный запрос',
                'message': 'Запрос содержит некорректные данные',
                'status_code': 400
            }), 400
        return render_template('errors/400.html', title='Неверный запрос'), 400
    
    @app.errorhandler(LibraryBaseException)
    def handle_library_exception(error):
        """Обработчик пользовательских исключений системы библиотеки"""
        app.logger.error(f"Library exception: {error.message}")
        
        if request.path.startswith('/api/'):
            return jsonify(error.to_dict()), error.status_code
        
        # Определяем шаблон для отображения ошибки
        template_map = {
            404: 'errors/404.html',
            400: 'errors/400.html',
            403: 'errors/403.html',
            409: 'errors/409.html',
            500: 'errors/500.html'
        }
        
        template = template_map.get(error.status_code, 'errors/500.html')
        
        return render_template(
            template,
            title='Ошибка',
            error_message=error.message,
            error_code=error.status_code
        ), error.status_code
    
    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        """Обработчик всех остальных исключений"""
        app.logger.error(f"Unhandled exception: {str(error)}", exc_info=True)
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Внутренняя ошибка сервера',
                'message': 'Произошла непредвиденная ошибка',
                'status_code': 500
            }), 500
        
        return render_template(
            'errors/500.html',
            title='Ошибка сервера',
            error_message='Произошла непредвиденная ошибка'
        ), 500
    
    # Настройка логирования ошибок
    if not app.debug:
        # В продакшене настраиваем файловое логирование
        import os
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = logging.FileHandler('logs/library.log')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Система управления библиотекой запущена')