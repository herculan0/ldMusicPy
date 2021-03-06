import logging
import traceback
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from . import db
from functools import partial


class Permissao:
    COMENTAR = 2
    AVALIAR = 4
    ADMIN = 16


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuario"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    nome = db.Column(db.String(180))
    senha_hash = db.Column(db.String(128))
    funcao_id = db.Column(db.Integer, db.ForeignKey("funcao.id"))
    sobre_mim = db.Column(db.Text())
    data_cadastro = db.Column(db.DateTime(), default=datetime.utcnow)
    confirmado = db.Column(db.Boolean, default=1)
    tipoUsuario = db.Column(db.String(30), nullable=False)
    rua = db.Column(db.String(64))
    numero = db.Column(db.Text())
    cidade = db.Column(db.String(64))
    endereco = db.Column(db.Text())
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    instrumento = db.Column(db.String(32))
    admin = db.Column(db.Boolean, default=0)
    urlVideo = db.Column(db.String(64))

    def __init__(self, **kwargs):
        super(Usuario, self).__init__(**kwargs)

    @property
    def senha(self):
        raise AttributeError("Senha não é um atributo legível.")

    # gera o hash da senha para guardar no banco #
    @senha.setter
    def senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    # verifica se o hash bate com a senha #
    def verifica_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    # gerar token para confirmação de email #
    def gerar_token_confirmar(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"confirmar": self.id}).decode("utf-8")

    # usuário precisa confirmar no email o cadastro #
    def confirmar(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except Exception as e:
            logging.error(traceback.format_exc(e))
            return False
        if data.get("confirmar") != self.id:
            return False
        self.confirmado = True
        db.session.add(self)
        return True

    # gerar o token para reset de senha #
    def gerar_reset_token(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"confirmar": self.id}).decode("utf-8")

    # recriar senha usuário #

    @staticmethod
    def reset_senha(token, nova_senha):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except Exception as e:
            logging.error(traceback.format_exc(e))
            return False
        usuario = Usuario.query.get(data.get("reset"))
        if usuario is None:
            return False
        usuario.senha = nova_senha
        db.session.add(usuario)
        return True

    def gerar_alterar_email_token(self, novo_email, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps(
            {"alterar_email": self.id, "novo_email": novo_email}
        ).decode("utf-8")

    def alterar_email(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except Exception as e:
            logging.error(traceback.format_exc(e))
            return False
        if data.get("alterar_email") != self.id:
            return False
        novo_email = data.get("novo_email")
        if novo_email is None:
            return False
        if self.query.filter_by(email=novo_email).first() is not None:
            return False
        self.email = novo_email
        db.session.add(self)
        return True

    # adiciona permissão de admin #
    def perm(self, perm):
        return self.can(Permissao.ADMIN)

    # atualiza a ultima_visualizacao do usuario no banco #
    def ping(self):
        self.ultima_visualizacao = datetime.utcnow()
        db.session.add(self)


class UsuarioAnonimo(AnonymousUserMixin):
    def can(self, permissoes):
        return False

    def admin():
        Usuario.admin = 0
        return

    def confirmado():
        Usuario.confirmado = None
        return


class Funcao(db.Model):
    __tablename__ = "funcao"
    table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True)
    padrao = db.Column(db.Boolean, default=False, index=True)
    permissoes = db.Column(db.Integer)
    usuarios = db.relationship("Usuario", backref="funcao", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Funcao, self).__init__(**kwargs)
        if self.permissoes is None:
            self.permissoes = 0

    @staticmethod
    def inserir_funcoes():
        funcoes = {
            "Usuario": [Permissao.COMENTAR, Permissao.AVALIAR],
            "Administrador": [
                Permissao.COMENTAR,
                Permissao.AVALIAR,
                Permissao.ADMIN,
            ],
        }
        funcao_padrao = "Usuario"
        for f in funcoes:
            funcao = Funcao.query.filter_by(nome=f).first()
            if funcao is None:
                funcao = Funcao(nome=f)
            funcao.reset_permissoes()
            for perm in funcoes[f]:
                funcao.add_permissao(perm)
            funcao.padrao = funcao.nome == funcao_padrao
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
        return "<Funcao %f>" % self.nome
