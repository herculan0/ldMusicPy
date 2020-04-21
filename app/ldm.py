from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:ldmusic@db:3306/ldMusic?charset=utf8mb4'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'ldmusic2020'

db = SQLAlchemy(app)

class Aluno(db.Model):
    __tablename__ = 'aluno'
    __id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(64))
    email = db.Column(db.String(45))
    senha = db.Column(db.String(11))

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha


db.create_all()

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")


@app.route("/cadastro", methods=['GET','POST'])
def cadastro():
    if request.method == "POST":

        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")

        if nome and email and senha :
            aluno = Aluno(nome,email, senha)
            db.session.add(aluno)
            db.session.commit()

    return redirect(url_for("index"))

@app.route("/lista")
def lista():
    alunos = Aluno.query.all()
    return render_template("lista.html",alunos=alunos)

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')
