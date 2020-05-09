from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import redirect
from flask import current_app
from flask import send_from_directory
from flask import Blueprint
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import pymysql
from . import autenticacao



#from flask_login import LoginManager

# bp = Blueprint('autenticacao', __name__, url_prefix='/autenticacao')
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
#login_manager = LoginManager()

# def create_app():
app = Flask(__name__)

bootstrap.init_app(app)
#mail.init_app(app)
moment.init_app(app)
app.register_blueprint(autenticacao.bp)
    # associar rotas e páginas de erro aqui
    #app.register_blueprint(autenticacao.bp)
    #login_manager.init_app(app)
    #login_manager.login_view = 'autenticacao.login'
    #...

con = pymysql.connect(host='db',
                      user='admin',
                      password='ldmusic',
                      db='ldMusic',
                      charset='utf8mb4')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:ldmusic@db:3306/ldMusic?charset=utf8mb4'
app.config['SECRET_KEY'] = 'ldmusic'
db = SQLAlchemy(app)

#    return app


@app.route('/')
@app.route('/home')
def home():
    return render_template('main.html')

@app.route('/about')
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/usuario/<name>')
def get_usuario(id):
    usuario = load_usuario(id)
    if not usuario:
        abort(404)
    return render_template('usuario.html', usuario=usuario)

@app.route('/perfil')
def perfil():
    if 'email' not in session:
        return redirect(url_for('cadastro'))
    usuario = usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        return redirect(url_for('cadastro'))
    else:
        return render_template('perfil.html')
