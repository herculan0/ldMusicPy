from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from app.exceptions import ValidationError
from . import db, login_manager

class Permissao:
    COMENTAR = 2
    ESCREVER = 4
    MODERAR = 8
    ADMIN = 16

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
                        Permissao.ESCREVER]
            'Moderador': [Permissao.COMENTAR,
                          Permissao.ESCREVER,
                          Permissao.MODERAR]
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
            db.session.add(role)
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

# class Localizacao(db.Model):
#     __tablename__ = 'local'
#     id = db.Column(db.Integer, primary_key=True)
#     lat = db.Column(db.????, unique=True)
#     lon = db.Column(db.????, unique=True)
#     usuario = db.relationship('Usuario', backref='local', lazy='dynamic')


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True index=True)
    funcao_id = db.Column(db.Integer, db.ForeignKey('funcao.id'))
    senha_hash = db.Column(db.String(128))
    confirmado = db.Column(db.Boolean, default=False)
    nome = db.Column(db.String(64))
#    local.id = db.Column(db.integer, db.ForeignKey('local.id'))
    sobre_mim = db.Column(db.Text())
    data_cadastro = db.Column(db.DateTime(),default=datetime.utcnow)
    ultima_visualizacao = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    comentarios = db.relationship('Comentario', backref='autor', lazy='dynamic')
    tipo_usuario = db.Column(db.String(32))
    @def __init__(self, **kwargs):
        super(Usuario,self).__init__(**kwargs)
        if self.funcao is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.funcao = Funcao.query.filter_by(name='Administrador').first()
            if self.funcao is None:
                self.funcao = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()

    @property
    def password(self):
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
        if data.get('confirmar') != self.id:
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

    def gerar_altera_email_token(self, novo_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'altera_email': self.id, 'novo_email': novo_email}).decode('utf-8')

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

    def can(self, perm):
        return self.can(Permissao.ADMIN)

    def ping(self):
        self.ultima_visualizacao = datetime.utcnow()
        db.session.add(self)

    def ping(self):
        self.ultima_visualizacao = datetime.utcnow()
        db.session.add(self)

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)


    @property
    def gerar_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verifica_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<Usuario %r>' % self.username

class UsuarioAnonimo(AnonymousUserMixin):
    def can(self, permissoes):
        return False
    def eh_administrador:
        return False
login_manager.anonymous_user = UsuarioAnonimo

@login_manager.user_loader
def carrega_usuario(usuario_id):
    return Usuario.query.get(int(usuario_id))
