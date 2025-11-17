from flask import jsonify
from app.api import bp
from app.models import Book, Branch, Faculty

@bp.route('/books') #
def books_json():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

@bp.route('/branches')
def branches_json():
    branches = Branch.query.all()
    return jsonify([branch.to_dict() for branch in branches])

@bp.route('/faculties')
def faculties_json():
    faculties = Faculty.query.all()
    return jsonify([faculty.to_dict() for faculty in faculties])
