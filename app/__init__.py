import os
import pymysql
import cryptography
from flask import Flask
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from pymysql import connect
from flask_migrate import Migrate


connection = pymysql.connect(host=os.getenv('DB_URL'),
                             user=os.getenv('DB_USER'),
                             password=os.getenv('DB_PASS'),
                             db='ldmusic',
                             charset='utf8mb4')

# cria objetos das bibliotecas #
db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
pagedown = PageDown()
manager = Manager()

login_manager = LoginManager()
login_manager.login_view = 'autenticacao.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(os.environ["APP_SETTINGS"])
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)
    # manager = manager(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .autenticacao import autenticacao as autenticacao_blueprint
    app.register_blueprint(autenticacao_blueprint)
    return app

# @manager.command
# def create_db():
# db.create_all()


# @manager.command
# def drop_db():
# db.drop_all()


# @manager.command
# def create_admin():
# db.session.add(Usuario("ad@min.com", "admin"))
