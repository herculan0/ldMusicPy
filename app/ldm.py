from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql

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

#CRIANDO CLASSE ALUNO#

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

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")

#ROTA PARA CREATE-RUD
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
#ROTA PARA C-READ-UD#
@app.route("/lista")
def lista():
    alunos = Aluno.query.all()
    return render_template("lista.html",alunos=alunos)

#ROTA PARA CRU-DELETE#
@app.route("/excluir/<int:id>")
def excluir(id):
    aluno = Aluno.query.filter_by(_id=id).first()
    db.session.delete(aluno)
    db.session.commit()

    alunos = Aluno.query.all()
    return render_template("lista.html", alunos=alunos)

@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    aluno = Aluno.query.filter_by(_id=id).first()

    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")

        if nome and email and senha :
            aluno.nome = nome
            aluno.email = email

            db.session.commit()

            return redirect(url_for("lista"))

    return render_template("atualizar.html", aluno=aluno)

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')
