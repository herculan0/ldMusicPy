import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy ## importar banco
from flask_login import LoginManager, UserMixin

### instancia um objeto da aplicação chamado app ##
app = Flask(__name__)


### configuração importada em .env e config.py onde colocaremos as variáveis de
#ambiente necessárias ###
app.config.from_object(os.environ['APP_SETTINGS'])


### instancia um objeto do SQLAlchemy(banco) chamado db ###
db = SQLAlchemy(app)


#### ROTAS (/, /sobre, /login, /cadastro,  /<instrumento>, /<instrutor>, /<aluno>) ####

### cria uma rota para o / ou seja 127.0.0.1:5000 ou localhost:5000 ###
@app.route('/')
def index():
    return "Olá, usuário!"

## MODELS ###

### classe usuário ###
class Usuario(UserMixin,db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128))
    tipo_usuario = db.Column(db.String(25), nullable=False)
    sobre_mim = db.Column(db.Text())
    data_cadastro = db.Column(db.DateTime(), default=datetime.utcnow)
    confirmado = db.Column(db.Boolean, default=False)
    def __init__(self, **kwargs):
        super(Usuario, self).__init__(**kwargs)

