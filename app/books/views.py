from flask import render_template, redirect, url_for, flash, request
from app.books import bp
from app import db
from app.models import Book
from app.books.forms import BookForm

@bp.route('/')
def list():
    books = Book.query.all()
    return render_template('books/list.html', books=books, title='Список книг')

@bp.route('/add', methods=['GET', 'POST'])
def add():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            authors=form.authors.data,
            publisher=form.publisher.data,
            year=form.year.data,
            pages=form.pages.data,
            illustrations=form.illustrations.data,
            cost=form.cost.data,
            copies_available=form.copies_available.data,
            branch_id=form.branch_id.data  # если используете выбор филиала
        )
        db.session.add(book)
        db.session.commit()
        flash('Книга успешно добавлена!', 'success')
        return redirect(url_for('books.list'))
    return render_template('books/add.html', form=form, title='Добавить книгу')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        form.populate_obj(book)
        db.session.commit()
        flash('Книга успешно обновлена!', 'success')
        return redirect(url_for('books.list'))
    return render_template('books/edit.html', form=form, title='Редактировать книгу')

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Книга удалена!', 'success')
    return redirect(url_for('books.list'))
