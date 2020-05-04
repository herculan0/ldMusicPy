from flask import (Flask, Blueprint)
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from pymysql import connect
#from config import config
from flask_login import LoginManager

#bp = Blueprint('autenticacao', __name__, url_prefix='/autenticacao')
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)

    #app.config.from_object(config[config_name])
    #config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    # ...

    # associar rotas e páginas de erro aqui

    #app.register_blueprint(autenticacao.bp)
    login_manager.init_app(app)
    login_manager.login_view = 'autenticacao.login'
    #...
    return app
