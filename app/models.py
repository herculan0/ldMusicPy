from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, PasswordField
from wtforms.validators import DataRequired, Length, Email, URL, EqualTo
import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
import pymysql
from ldMusicPy import app



con = pymysql.connect(host='db',
                      user='admin',
                      password='ldmusic',
                      db='ldMusic',
                      charset='utf8mb4')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:ldmusic@db:3306/ldMusic?charset=utf8mb4'
db = SQLAlchemy(app)




class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Me mantenha logado!')
    submit = SubmitField('Entrar')


class CadastroForm(FlaskForm):
    primeiroNome = StringField('Primeiro Nome:', validators=[DataRequired()])
    ultimoNome = StringField('Último Nome:')
    email = StringField('Email:', validators=[Email(),
                                              DataRequired()])
    senha = PasswordField('Senha: ', validators=[DataRequired(),
                                                 EqualTo('confirmaSenha', message='As senhas devem ser Iguais')])
    confirmaSenha = PasswordField('Confirmar Senha ')
    funcao = RadioField('Aluno ou Instrutor', validators=[DataRequired()])
    videoURL = StringField('Link do Vídeo: ', validator=[URL()])
    submit = SubmitField('Cadastrar')


class Usuario(UserMixin, db.Model):
    __table__='usuario'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String(64), unique=True, index=True)
    primeiroNome = db.Column(db.String(64))
    ultimoNome = db.Column(db.String(64))
    nome = db.Column(db.String(128))
    email = db.Column(db.String(45), unique=True)
    #senha_hash =
    funcao_id = db.Column(db.String(11), dbForeignKey('funcoes.id'))

    def __init__(self, nome, email, senha):
        self.primeironome = primeironome
        self.segundonome = segundonome
        self.email = email
        self.senha = senha
        self.nome = primeironome + " " + ultimonome

class Funcao(db.Model):
    __table__='funcoes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(64))

    def __init__(self, nome):
        self.nome = nome


