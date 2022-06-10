import os
from flask import Flask
from app.db import DB
# from flask_login import LoginManager

# login = LoginManager()

# login.login_view = 'main.login'
# login.login_message = 'Please log in to access this page.'

db = DB(os.environ.get('DB_URL'))

def create_app():
    app = Flask(__name__)
    # login.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app