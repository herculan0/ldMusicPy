# coding:utf-8

from flask import Flask, render_template, request, url_for, redirect

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY'] = 'sqlite///db.sqlite'

db = SQLAlchemy(app)

class Administrador(db.Model):
    __tablename__ = 'administrador'
    __id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    email = db.Column(db.String)

    def __init__(self, nome, email):
        self.nome = nome
        self.email = email


db.create_all()

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")


@app.route("/cadastro", methods=['GET','POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")

        if nome and email:
            admin = Administrador(nome, email)
            db.session.add()

@app.route("/aluno")
def aluno():
    return render_template("aluno.html")

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')
