import os
import hashlib ## senha_hash

from flask import Flask, request, url_for, current_app
from flask_sqlalchemy import SQLAlchemy ## importar banco
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

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

    @propriedade
    def senha(self):
        raise AttributeError('Senha não é um atributo legível.')

    @senha.setter
    def senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
    
    def verifica_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def gerar_token_confirmar(self, token):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirma': self.id}).decode('utf-8')

    def confirmar(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirmado') != self.id:
            return False
        self.confirmado = True
        db.session.add(self)
        return True

    def gerar_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_senha(token, nova_senha):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        usuario = Usuario.query.get(data.get('reset'))
        if user is None:
            return False
        usuario.senha = nova_senha
        db.session.add(usuario)
        return True
