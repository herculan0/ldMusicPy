from flask import request, url_for, redirect, flash, render_template
from flask_login import login_user, logout_user, login_required, current_user
from . import autenticacao
from ..models import Usuario
from ..email import enviar_email
from .forms import (LoginForm,
                    CadastroForm,
                    AlterarSenhaForm,
                    AlterarEmailForm,
                    RequisicaoResetaSenhaForm,
                    SenhaResetaForm)
from .. import db
from functools import partial
import os
from geopy import geocoders as geolocalizacao
geolocalizacao = geolocalizacao.GoogleV3(api_key=os.environ.get('API_MAPS'))


@autenticacao.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
    if not current_user.confirmado \
            and request.endpoint \
            and request.endpoint != "static":
        return redirect(url_for("autenticacao.nao_confirmado"))


@autenticacao.route("/nao_confirmado")
def nao_confirmado():
    if current_user.is_anonymous or current_user.confirmado:
        return redirect(url_for("main.index"))
    return render_template("autenticacao/nao_confirmado.html")


@autenticacao.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(
            email=form.email.data.lower()
        ).first()
        if usuario is not None and usuario.verifica_senha(form.senha.data):
            login_user(usuario, form.remember_me.data)
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("main.index")
            return redirect(next)
        flash("Email ou senha inválido.")
    return render_template("autenticacao/login.html", form=form)


@autenticacao.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você se deslogou com sucesso.")
    return redirect(url_for("main.index"))


@autenticacao.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
        localizacao = str("{} {} {}".format(
                                         form.rua.data,
                                         str(form.numero.data),
                                         form.cidade.data,
                                            )
                          )
        localizacao = geolocalizacao.geocode("'{}'".format(
                                    localizacao),
                                    exactly_one=True)
        endereco = str(localizacao)
        latitude = localizacao.latitude
        longitude = localizacao.longitude
        usuario = Usuario(
            email=form.email.data.lower(),
            nome=form.nome.data,
            username=form.username.data,
            senha=form.senha.data,
            rua=form.rua.data,
            numero=form.numero.data,
            cidade=form.cidade.data,
            endereco=endereco,
            latitude=latitude,
            longitude=longitude,
            tipoUsuario=form.tipoUsuario.data)
        db.session.add(usuario)
        db.session.commit()
        token = usuario.gerar_token_confirmar()
        enviar_email(
            usuario.email,
            "Confirme sua conta",
            "autenticacao/email/confirmar",
            usuario=usuario,
            token=token)
        flash("Um email de confirmação foi enviado para o seu email.")
        return redirect(url_for("autenticacao.login"))
    return render_template("autenticacao/cadastro.html", form=form)


@autenticacao.route("/confirmar/<token>")
@login_required
def confirmar(token):
    if current_user.confirmado:
        return redirect(url_for("main.index"))
    if current_user.confirmar(token):
        db.session.commit()
        flash("Conta confirmada com sucesso. Bem vindo!")
    else:
        flash("O Link de confirmação é inválido ou expirou.")
    return redirect(url_for("main.index"))


@autenticacao.route("/confirmar")
@login_required
def reenviar_confirmacao():
    token = current_user.gerar_token_confirmar()
    enviar_email(
        current_user.email,
        "Confirme sua Conta",
        "confirmar",
        usuario=current_user,
        token=token,
    )
    flash("Um novo email de confirmação foi enviado para o seu email.")
    return redirect(url_for("main.index"))


@autenticacao.route("/alterar-senha", methods=["GET", "POST"])
@login_required
def alterar_senha():
    form = AlterarSenhaForm()
    if form.validate_on_submit():
        if current_user.verifica_senha(form.senha_antiga.data):
            current_user.senha = form.senha.data
            db.session.add(current_user)
            db.session.commit()
            flash("Sua senha foi alterada com sucesso.")
            return redirect(url_for("main.index"))
        else:
            flash("Senha inválida.")
    return render_template("autenticacao/alterar_senha.html", form=form)


@autenticacao.route("/reset", methods=["GET", "POST"])
def requisicao_reset_senha():
    if not current_user.is_anonymous:
        return redirect(url_for("main.index"))
    form = RequisicaoResetaSenhaForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(
            email=form.email.data.lower()
        ).first()
        if usuario:
            token = usuario.gerar_reset_token()
            enviar_email(
                usuario.email,
                "Resetar sua senha",
                "autenticacao_resetar_senha",
                usuario=usuario,
                token=token,
            )
        flash(
            """Um email contendo as instruções para\
                    o reset de senha foi enviado para você"""
        )
        return redirect(url_for("autenticacao.login"))
    return render_template("autenticacao/reset_senha.html", form=form)


@autenticacao.route("/reset/<token>", methods=["GET", "POST"])
def reset_senha(token):
    if not current_user.is_anonymous:
        return redirect(url_for("main.index"))
    form = SenhaResetaForm()
    if form.validate_on_submit():
        if Usuario.reset_senha(token, form.senha.data):
            db.session.commit()
            flash("Sua senha foi atualizada com sucesso.")
            return redirect(url_for("autenticacao.login"))
        else:
            return redirect(url_for("main.index"))
    return render_template("autenticacao/reset_senha.html", form=form)


@autenticacao.route("/alterar_email", methods=["GET", "POST"])
@login_required
def requisicao_alterar_email():
    form = AlterarEmailForm()
    if form.validate_on_submit():
        if current_user.verifica_senha(form.senha.data):
            novo_email = form.email.data.lower()
            token = current_user.gerar_alterar_email_token(novo_email)
            enviar_email(
                novo_email,
                "Confirme seu endereço de email",
                "autenticacao.altera_email",
                usuario=current_user,
                token=token,
            )
            flash(
                "Enviamos Email contendo as instruções para confirmar"
                " o novo endereço de email "
                " foi enviado para você."
            )
            return redirect(url_for("main.index"))
        else:
            flash("Email ou senha inválido.")
    return render_template("autenticacao/alterar_email.html", form=form)
