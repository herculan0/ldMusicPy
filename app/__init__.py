import os
import hashlib
import bleach
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__) '.env.')


from flask import Flask, request, url_for, current_app
from flask_sqlalchemy import SQLAlchemy ## importar banco
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime



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

### cria classe para dar permissões aos usuários ###
class Permissao:
    COMENTAR = 2
    ESCREVER = 4
    ADMIN = 16 


### classe funcao, onde invoca permissoes para admin ou usuario comum ###
class Funcao(db.Model):
    __tablename__ = 'funcao'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True)
    padrao = db.Column(db.Boolean, default=False, index=True)
    permissoes = db.Column(db.Integer)
    usuario = db.relationship('Usuario', backref='funcao', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Funcao, self).__init__(**kwargs)
        if self.permissoes is None:
            self.permissions = 0

    @staticmethod
    def inserir_funcoes():
        funcoes = {
            'Usuario': [Permissao.COMENTAR,
                        Permissao.ESCREVER],
            'Administrador':[Permissao.COMENTAR,
                             Permissao.ESCREVER,
                             Permissao.ADMIN]
        }
        funcao_padrao = 'Usuario'
        for f in funcoes:
            funcao = Funcao.query.filter_by(nome=f).first()
            if funcao is None:
                funcao = Funcao(nome=f)
            funcao.resetar_permissoes(perm)
            for perm in funcoes[f]:
                funcao.add_permissao(perm)
            funcao.padrao = (funcao.nome == funcao_padrao)
            db.session.add(funcao)
        db.session.commit()

    def add_permissao(self, perm):
        if not self.tem_permissao(perm):
            self.permissoes += perm

    def remover_permissao(self):
        self.permissoes = 0

    def tem_permissao(self, perm):
        return self.permissoes & perm == perm

    def __repr__(self):
        return '<Funcao %f>' % self.nome

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

    ### gera o hash da senha para guardar no banco ###
    @senha.setter
    def senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
    
    ### verifica se o hash bate com a senha ###
    def verifica_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    ### gerar token para confirmação de email ###
    def gerar_token_confirmar(self, token):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirma': self.id}).decode('utf-8')
    
    ### usuário precisa confirmar no email o cadastro ###
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

    ### gerar o token para reset de senha ###
    def gerar_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    ### recriar senha usuário ###

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

    ### cria um token para alteração do email ###
    def gerar_altera_email_token(self, novo_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'altera_email': self.id, 'novo_email': novo_email}).decode('utf-8')

    ### altera o email no banco ###
    def altera_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('altera_email') != self.id:
            return False
        novo_email = data.get('novo_email')
        if novo_email is None:
            return False
        if self.query.filter_by(email=novo_email).first() is not None:
            return False
        self.email = novo_email
        self.avatar_hash = self.gravatar_hash()
        db.session.add(self)
        return True

    ### adiciona permissão de admin ###
    def perm(self, perm):
        return self.can(Permissao.ADMIN)

    ### atualiza a ultima_visualizacao do usuario no banco ###
    def ping(self):
        self.ultima_visualizacao = datetime.utcnow()
        db.session.add(self)
    
    ### gera um hash para o avatar do usuario ###
    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    ### gera um avatar ###
    def gravatar(self, size=100, default='identicon', rating='g'):
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)



### cria usuário anônimo retornando falso para qualquer permissão ###
class UsuarioAnonimo(AnonymousUserMixin):
    def can(self,permissoes):
        return False
    def administrador:
        return False

login_manager.anonymous_user = UsuarioAnonimo

## método para carregar usuário ##
@login_manager.user_loader
def carrega_usuario(id):
    return Usuario.query.get(int(id))


#### formularios de login, cadastro e recupera/altera senha e reset email###

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64),
                                             Email()])
    senha = PasswordField('Sennha', validators=[DataRequired()])
    remember_me = BooleanField('Me mantenha Logado')
    submit = SubmitField('Entrar')

class CadastroForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64),
                                             Email()])
    username = StringField('Usuario', validators=[
        DataRequired(), Length(1,64),
        Regexp('^[A-Za-z][A-Za-z0-9.]*$', 0,
               'Nomes de Usuário devem conter somente letras, números ou pontos')
    ])
    senha = PasswordField('Senha', validators=[DataRequired(), EqualTo('senha2', message='Senhas não são iguais.')])
    senha2 = PasswordField('Confirmar Senha', validators=[DataRequired()])
    nome = StringField('Nome Completo', validators[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z]*$', 0,
               'Nomes devem conter apenas texto.')])
    submit = SubmitField('Cadastrar')
    
    ### valida se o email já existe ###
    def validar_email(self, field):
        if Usuario.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email já em está em uso.')
    ### valida se o username ja foi cadastrado
    def validar_username(self, field):
        if Usuario.query.filter_by(username=field.data.lower()).first():
            raise ValidationError('Usuario já cadastrado')


class AlterarSenhaForm(FlaskForm):
    senha_antiga = PasswordField('Senha Antiga', validators = [DataRequired()])
    senha = PasswordField('Nova Senha', validators=[
        DataRequired(), EqualTo('senha2', message='As senhas devem ser iguais.')])
    senha2 = PasswordField('Confirmar Nova Senha',
                           validators=[DataRequired()])
    submit = SubmitField('Atualizar Senha')

class RequisicaoResetaSenhaForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64),
                                             Email()])
    submit SubmitField('Resetar Senha')

class SenhaResetaForm(FlaskForm):
    senha = PasswordField('Nova Senha', validators=[
        DataRequired(), EqualTo('senha2', message='As senhas devem ser iguais.')])
    senha2 = PasswordField('Confirmar Nova Senha',
                           validators=[DataRequired()])
    submit = SubmitField('Resetar Senha')


