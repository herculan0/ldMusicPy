from flask import Blueprint
rotas = Blueprint('rotas', __name__)

from .index import *


#@rotas.route("/instrumentos")
#def instrumentos():
#     return render_template("instrumento.html")

#@rotas.route("/cadastrar")
#def cadastrar():
#    return render_template("cadastro.html")

##ROTA PARA CREATE-RUD
#@rotas.route("/cadastro", methods=['GET','POST'])
#def cadastro():
#    if request.method == "POST":

#        nome = request.form.get("nome")
#        email = request.form.get("email")
#        senha = request.form.get("senha")

#        if nome and email and senha :
#            aluno = Aluno(nome,email, senha)
#            db.session.add(aluno)
#            db.session.commit()

#    return redirect(url_for("index"))
##ROTA PARA C-READ-UD#
#@rotas.route("/lista")
#def lista():
#    alunos = Aluno.query.all()
#    return render_template("lista.html",alunos=alunos)

##ROTA PARA CRU-DELETE#
#@rotas.route("/excluir/<int:id>")
#def excluir(id):
#    aluno = Aluno.query.filter_by(_id=id).first()
#    db.session.delete(aluno)
#    db.session.commit()

#    alunos = Aluno.query.all()
#    return render_template("lista.html", alunos=alunos)

#@rotas.route("/atualizar/<int:id>", methods=['GET', 'POST'])
#def atualizar(id):
#    aluno = Aluno.query.filter_by(_id=id).first()

#    if request.method == "POST":
#        nome = request.form.get("nome")
#        email = request.form.get("email")
#        senha = request.form.get("senha")

#        if nome and email and senha :
#            aluno.nome = nome
#            aluno.email = email

#            db.session.commit()

#            return redirect(url_for("lista"))

#    return render_template("atualizar.html", aluno=aluno)


