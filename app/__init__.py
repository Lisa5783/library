# app/__init__.py
"""
Flask приложение для системы управления библиотекой
Использует Application Factory Pattern с Blueprint'ами
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from app.config import Config
from app.exceptions import register_error_handlers

# Создаем объекты расширений
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_class=Config):
    """
    Фабрика приложений Flask
    
    Args:
        config_class: Класс конфигурации
    
    Returns:
        Flask: Настроенное приложение Flask
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Регистрация Blueprint'ов
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.books import bp as books_bp
    app.register_blueprint(books_bp, url_prefix='/books')
    
    from app.branches import bp as branches_bp
    app.register_blueprint(branches_bp, url_prefix='/branches')
    
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Регистрация обработчиков ошибок
    register_error_handlers(app)
    
    # Регистрация хуков для SQLAlchemy
    from app.hooks import register_hooks
    register_hooks()
    
    return app


# Импорт моделей после создания объекта db
from app import models