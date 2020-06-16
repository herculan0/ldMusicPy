import googlemaps
import os
import re
from flask import render_template, flash, url_for, redirect, request
from flask_login import current_user, login_required
from ..models import UsuarioAnonimo, Usuario
from .. import db, login_manager
from . import main
from .forms import (Relatorio,
                    PerfilUsuario,
                    EditarPerfilInstrutor,
                    PerfilAdministrador,
                    Relatorio,
                    EditarPerfilForm)

gmaps = googlemaps.Client(key=os.environ.get('API_DISTANCIA'))
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


@main.route("/relatorio/", methods=['GET', 'POST'])
def relatorio():
    form = Relatorio(request.form)
    busca = form.busca.data
    filtro = form.filtro.data
    tipo_usuario = form.tipo_usuario.data
    if request.method == "POST":
        if busca == "":
            usuarios = Usuario.query.filter_by(tipoUsuario=tipo_usuario).all()
            return render_template('relatorio.html', form=form, usuarios=usuarios)
        elif filtro =='nome':
            usuarios = Usuario.query.filter_by(tipoUsuario=tipo_usuario, nome=busca).all()
            return render_template('relatorio.html', form=form, usuarios=usuarios)
        elif filtro == 'cidade':
            usuarios = Usuario.query.filter_by(tipoUsuario=tipo_usuario, cidade=busca).all()
            return render_template('relatorio.html', form=form, usuarios=usuarios)
        elif filtro == 'instrumento':
            usuarios = Usuario.query.filter_by(tipoUsuario=tipo_usuario, instrumento=busca).all()
            return render_template('relatorio.html', form=form, usuarios=usuarios)
    return render_template('relatorio.html', form=form)


@main.route("/home/")
def home():
    usuarios = Usuario.query.order_by(Usuario.username).all()
    return render_template("home.html", usuarios=usuarios)


@main.route("/instrutor/")
def instrutor():
    usuarios = Usuario.query.filter_by(tipoUsuario='instrutor').all()
    instrutores = []
    for instrutor in usuarios:
        dist = gmaps.distance_matrix(current_user.endereco, instrutor.endereco)
        km = dist.get("rows")[0].get("elements")[0].get("distance").get("text")
        km = str(re.findall(r"[-+]?\d*\.\d+|\d+", km)).strip('[]').strip("\'")
        km = float(km)
        if km <= 15:
            instrutores.append({'usuario': instrutor, 'dist': dist, 'km': km})
    return render_template("instrutor.html", instrutores=instrutores)


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
