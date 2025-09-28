from flask import render_template, redirect, url_for, flash, request
from app.branches import bp
from app import db
from app.models import Branch
from app.branches.forms import BranchForm

@bp.route('/')
def list():
    branches = Branch.query.all()
    return render_template('branches/list.html', branches=branches, title='Список филиалов')

@bp.route('/add', methods=['GET', 'POST'])
def add():
    form = BranchForm()
    if form.validate_on_submit():
        branch = Branch(
            name=form.name.data,
            location=form.location.data
        )
        db.session.add(branch)
        db.session.commit()
        flash('Филиал успешно добавлен!', 'success')
        return redirect(url_for('branches.list'))
    return render_template('branches/add.html', form=form, title='Добавить филиал')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    branch = Branch.query.get_or_404(id)
    form = BranchForm(obj=branch)
    if form.validate_on_submit():
        form.populate_obj(branch)
        db.session.commit()
        flash('Филиал обновлен!', 'success')
        return redirect(url_for('branches.list'))
    return render_template('branches/edit.html', form=form, title='Редактировать филиал')

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    branch = Branch.query.get_or_404(id)
    db.session.delete(branch)
    db.session.commit()
    flash('Филиал удален!', 'success')
    return redirect(url_for('branches.list'))
