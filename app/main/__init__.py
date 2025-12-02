from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name="default"):
    app = Flask(__name__)
    # конфиг сюда
    db.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

