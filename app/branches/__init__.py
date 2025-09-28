from flask import Blueprint

bp = Blueprint('branches', __name__)

from app.branches import views
