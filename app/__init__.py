import os
from flask import Flask, current_app, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, AnonymousUserMixin
from flask_mail import Mail, Message
from threading import Thread

from flask_moment import Moment

from .models import Usuario

# cria objetos das bibliotecas #
db = SQLAlchemy()
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
login_manager = LoginManager()
pagedown = PageDown()
manager = Manager()

app = Flask(__name__)

app.config.from_object(os.environ["APP_SETTINGS"])

bootstrap.init_app(app)
mail.init_app(app)
db.init_app(app)
login_manager.init_app(app)
moment.init_app(app)
pagedown.init_app(app)
manager = Manager(app)


with app.app_context():
    db.create_all()


class UsuarioAnonimo(AnonymousUserMixin):
    def can(self, permissoes):
        return False

    def admin():
        return False


login_manager.anonymous_user = UsuarioAnonimo


@login_manager.user_loader
def carrega_usuario(id):
    return Usuario.query.get(int(id))


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def enviar_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(
        app.config["LDM_MAIL_SUBJECT_PREFIX"] + " " + subject,
        sender=app.config["LDM_MAIL_SENDER"],
        recipients=[to],
    )
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


# def calcula_distancia(latLongAluno, latLongInstrutor):
# latLongAluno

# @manager.command
# def create_db():
# db.create_all()


# @manager.command
# def drop_db():
# db.drop_all()


# @manager.command
# def create_admin():
# db.session.add(Usuario("ad@min.com", "admin"))
