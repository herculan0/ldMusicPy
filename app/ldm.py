from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql
import routes

app = Flask(__name__)


# CONEXÃO DO DRIVER CONECTOR MYSQL #

connection = pymysql.connect(host='db',
                             user='admin',
                             password='ldmusic',
                             db='ldMusic',
                             charset='utf8mb4')

#CONEXÃO DO SQLALCHEMY (OBJECT RELATIONAL MODEL)#

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:ldmusic@db:3306/ldMusic?charset=utf8mb4'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.secret_key = 'ldmusic2020'

db = SQLAlchemy(app)

class Instrumento(db.Model):


#CRIANDO CLASSE ALUNO#
    __tablename__='instrumento'
    cod_instrumento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_instrumento = db.Column(db.String(45))

    def __init__(self, nome_instrumento):
        self.nome_instrumento = nome_instrumento

class Aluno(db.Model):

#MODELO DO BANCO DA CLASSE ALUNO
    __tablename__ = 'aluno'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(64))
    email = db.Column(db.String(45))
    senha = db.Column(db.String(11))
#MÉTODO CONSTRUTOR DA CLASSE ALUNO
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

#CRIA O BANCO DE DADOS DE ACORDO COM O INSTRUÍDO NOS BLOCOS ACIMA:(PODERÁ SER DELETADO, CASO O BANCO DE DADOS JÁ ESTEJA PRONTO)#
db.create_all()

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')
