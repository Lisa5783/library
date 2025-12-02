from flask import Blueprint

bp = Blueprint('books', __name__)

from app.books import views
