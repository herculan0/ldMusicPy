from flask import render_template, flash, url_for, redirect
from flask_login import current_user, login_required
from ..models import UsuarioAnonimo, Usuario
from .. import db, login_manager
from . import main
from geopy.distance import geodesic
from .forms import (Instrumentos,
                    PerfilUsuario,
                    EditarPerfilInstrutor,
                    PerfilAdministrador,
                    Relatorio,
                    EditarPerfilForm)
login_manager.anonymous_user = UsuarioAnonimo


@login_manager.user_loader
def carrega_usuario(id):
    return Usuario.query.get(int(id))


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/perfil_administrador/", methods=['GET', 'POST'])
def perfil_administrador():
    administrador = PerfilAdministrador()
    return render_template("perfil_administrador.html",
                           administrador=administrador)


@main.route("/relatorio/", methods=['GET'])
def relatorio():
    relatorio = Relatorio()
    if relatorio.validate_on_submit():
        filtro = relatorio.filtro.data,
        busca = relatorio.busca.data
    return render_template("relatorio.html", relatorio=relatorio)


@main.route("/home/")
def home():
    usuarios = Usuario.query.order_by(Usuario.username).all()
    return render_template("home.html", usuarios=usuarios)


@main.route("/instrutor/")
def instrutor():
    user = Usuario.query.filter_by(tipoUsuario='instrutor').all()
    return render_template("instrutor.html", usuario =current_user, user=user)

@main.route("/alterar_email/<token>")
@login_required
def alterar_email(token):
    if current_user.alterar_email(token):
        db.session.commit()
        flash("Seu email foi atualizado com sucesso.")
    else:
        flash("Requisição inválida.")
    return redirect(url_for("main.index"))


@main.route("/perfil/")
def perfil():
    return render_template("perfil.html")


@main.route("/usuario/<username>")
def usuario(username):
    usuario = Usuario.query.filter_by(username=username).first_or_404()
    return render_template("usuario.html", usuario=usuario)


@main.route("/editar_pefil_instrutor/", methods=['GET', 'POST'])
def editar_perfil_instrutor():
    form = EditarPerfilInstrutor()
    if form.validate_on_submit():
        current_user.endereco = form.endereco.data
        current_user.urlVideo = form.urlVideo.data
        current_user.sobre_mim = form.sobre_mim.data
        current_user.instrumento = form.instrumento.data
        db.session.add(current_user)
        db.session.commit()
        flash("Seu perfil foi atualizado com sucesso")
        return redirect(url_for('main.usuario',
                                username=current_user.username))
    return render_template("editar_perfil_instrutor.html",
                           form=form)


@main.route("/editar_perfil_usuario/", methods=['GET', 'POST'])
def editar_perfil_usuario():
    form = EditarPerfilForm()
    if form.validate_on_submit():
        current_user.endereco = form.endereco.data
        current_user.instrumento = form.instrumento.data
        db.session.add(current_user)
        db.session.commit()
        flash("Seu perfil foi atualizado com sucesso")
        return redirect(url_for('main.usuario',
                                username=current_user.username))
    return render_template("editar_perfil_usuario.html",
                           form=form)
