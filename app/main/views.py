from flask import render_template, flash, url_for, redirect
from flask_login import current_user, login_required
from ..models import UsuarioAnonimo, Usuario
from .. import db, login_manager
from . import main
from .forms import EditarPerfilForm
login_manager.anonymous_user = UsuarioAnonimo


@login_manager.user_loader
def carrega_usuario(id):
    return Usuario.query.get(int(id))


@main.route("/")
def index():
    return render_template("index.html")

@main.route("/administrador/")
def administrador():
    return render_template("administrador.html")


@main.route("/home/")
def home():
    usuarios = Usuario.query.order_by(Usuario.username).all()
    return render_template("home.html", usuarios=usuarios)


@main.route("/alterar_email/<token>")
@login_required
def alterar_email(token):
    if current_user.alterar_email(token):
        db.session.commit()
        flash("Seu email foi atualizado com sucesso.")
    else:
        flash("Requisição inválida.")
    return redirect(url_for("main.index"))


@main.route("/usuario/<username>")
def usuario(username):
    usuario = Usuario.query.filter_by(username=username).first_or_404()
    return render_template("usuario.html", usuario=usuario)


@main.route('/editar-perfil', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = EditarPerfilForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.endereco = form.endereco.data
        current_user.sobre_mim = form.sobre_mim.data
        db.session.add(current_user._get_current_object())
        db.serssion.commit()
        flash("Seu perfil foi atualizado com sucesso")
        return redirect(url_for('.user', username=current_user.username))
    form.nome.data = current_user.nome
    form.endereco.data = current_user.endereco
    return render_template('editar_perfil.html', form=form)
