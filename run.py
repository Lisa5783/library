# run.py
"""
Точка входа для Flask приложения системы управления библиотекой
"""

import os
from flask_migrate import upgrade
from app import create_app, db
from app.models import Book, Branch, Faculty, book_faculties


app = create_app()


@app.shell_context_processor
def make_shell_context():
    """
    Контекст для Flask shell
    Добавляет модели в контекст для удобной работы в shell
    """
    return {
        'db': db,
        'Book': Book,
        'Branch': Branch,
        'Faculty': Faculty,
        'book_faculties': book_faculties
    }


@app.cli.command()
def init_db():
    """
    Инициализация базы данных
    Создает все таблицы и добавляет тестовые данные
    """
    print("Создание таблиц базы данных...")
    db.create_all()
    
    print("Добавление тестовых данных...")
    add_sample_data()
    
    print("База данных инициализирована!")


@app.cli.command()
def reset_db():
    """
    Сброс базы данных
    Удаляет все таблицы и создает их заново с тестовыми данными
    """
    print("Удаление существующих таблиц...")
    db.drop_all()
    
    print("Создание таблиц базы данных...")
    db.create_all()
    
    print("Добавление тестовых данных...")
    add_sample_data()
    
    print("База данных сброшена и инициализирована!")


def add_sample_data():
    """
    Добавление тестовых данных в базу данных
    """
    # Проверяем, есть ли уже данные
    if Branch.query.count() > 0:
        print("Тестовые данные уже существуют")
        return
    
    try:
        # Создаем филиалы
        central_branch = Branch(
            name="Центральный филиал",
            location="ул. Пушкина, д. 1"
        )
        technical_branch = Branch(
            name="Технический филиал",
            location="пр. Науки, д. 15"
        )
        humanities_branch = Branch(
            name="Гуманитарный филиал",
            location="ул. Литературная, д. 8"
        )
        
        db.session.add_all([central_branch, technical_branch, humanities_branch])
        db.session.flush()  # Получаем ID без коммита
        
        # Создаем факультеты
        it_faculty = Faculty(
            name="Информационные технологии",
            description="Факультет информационных технологий и программирования"
        )
        math_faculty = Faculty(
            name="Математика и физика",
            description="Факультет математических и физических наук"
        )
        history_faculty = Faculty(
            name="История и филология",
            description="Факультет исторических и филологических наук"
        )
        engineering_faculty = Faculty(
            name="Инженерное дело",
            description="Факультет инженерных наук"
        )
        
        db.session.add_all([it_faculty, math_faculty, history_faculty, engineering_faculty])
        db.session.flush()
        
        # Создаем книги
        programming_book = Book(
            title="Основы программирования",
            authors="Иван Иванов, Петр Петров",
            publisher="Техническая литература",
            year=2023,
            pages=450,
            illustrations=120,
            cost=1500.0,
            copies_available=5,
            times_issued=23,
            branch_id=technical_branch.id
        )
        programming_book.faculties = [it_faculty, engineering_faculty]
        
        math_book = Book(
            title="Математический анализ",
            authors="Анна Смирнова",
            publisher="Университетское издательство",
            year=2022,
            pages=680,
            illustrations=85,
            cost=2200.0,
            copies_available=3,
            times_issued=45,
            branch_id=central_branch.id
        )
        math_book.faculties = [math_faculty, engineering_faculty]
        
        history_book = Book(
            title="История России",
            authors="Сергей Николаев",
            publisher="Историческое общество",
            year=2021,
            pages=520,
            illustrations=200,
            cost=1800.0,
            copies_available=7,
            times_issued=67,
            branch_id=humanities_branch.id
        )
        history_book.faculties = [history_faculty]
        
        python_book = Book(
            title="Python для начинающих",
            authors="Мария Козлова",
            publisher="Программист",
            year=2023,
            pages=320,
            illustrations=50,
            cost=1200.0,
            copies_available=8,
            times_issued=34,
            branch_id=technical_branch.id
        )
        python_book.faculties = [it_faculty]
        
        physics_book = Book(
            title="Общая физика",
            authors="Александр Петров, Елена Сидорова",
            publisher="Наука и техника",
            year=2022,
            pages=890,
            illustrations=300,
            cost=2800.0,
            copies_available=4,
            times_issued=56,
            branch_id=central_branch.id
        )
        physics_book.faculties = [math_faculty, engineering_faculty]
        
        db.session.add_all([
            programming_book, math_book, history_book, 
            python_book, physics_book
        ])
        
        # Коммитим все изменения
        db.session.commit()
        
        print("Тестовые данные добавлены:")
        print(f"- Филиалов: {Branch.query.count()}")
        print(f"- Факультетов: {Faculty.query.count()}")
        print(f"- Книг: {Book.query.count()}")
        
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при добавлении тестовых данных: {e}")
        raise


if __name__ == '__main__':
    # Проверяем переменную окружения для режима работы
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    port = int(os.environ.get('PORT', 5000))
    
    # Автоматическая инициализация БД при первом запуске
    with app.app_context():
        db.create_all()
        if Branch.query.count() == 0:
            print("Первый запуск - инициализация базы данных...")
            add_sample_data()
    
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                СИСТЕМА УПРАВЛЕНИЯ БИБЛИОТЕКОЙ                   ║
║                                                                  ║
║  Приложение запущено на: http://127.0.0.1:{port:<4}                ║
║  Режим отладки: {str(debug_mode):<7}                                     ║
║                                                                  ║
║  Доступные команды:                                              ║
║  • flask init-db    - инициализация БД                          ║
║  • flask reset-db   - сброс БД                                  ║
║  • flask shell      - интерактивная оболочка                    ║
║                                                                  ║
║  Документация API: http://127.0.0.1:{port}/api                     ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)