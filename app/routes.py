import logging
from flask import render_template
from flask import (request,
                   url_for,
                   redirect,
                   flash)
from flask_login import (login_user,
                         logout_user,
                         login_required,
                         current_user)
from .models import Usuario
from .forms import (LoginForm,
                    CadastroForm,
                    AlterarSenhaForm,
                    AlterarEmailForm,
                    RequisicaoResetaSenhaForm,
                    SenhaResetaForm)
from . import app, db, enviar_email

# ROTAS (/, /sobre, /login, /cadastro,
# /<instrumento>, /<instrutor>, /<aluno>) #


@app.route("/")
def index():
    return render_template("index.html")


# @app.before_request
# def before_request():
# if current_user.is_authenticated:
# current_user.ping()
# if (
# not current_user.confirmado
# and request.endpoint
# and request.endpoint != "static"
# ):
# return redirect(url_for("nao_confirmado"))


# @app.route("/nao_confirmado")
# def nao_confirmado():
# if current_user.is_anonymous or current_user.confirmado:
# return redirect(url_for("index"))
# return render_template("nao_confirmado.html")


@app.route("/login", methods=["GET", "POST"])
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
                next = url_for("index")
            return redirect(next)
        flash("Email ou senha inválido.")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você se deslogou com sucesso.")
    return redirect(url_for("index"))


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
        usuario = Usuario(
            email=form.email.data.lower(),
            username=form.username.data,
            # endereco=form.endereco.data,
            senha=form.senha.data,
        )
        db.session.add(usuario)
        db.session.commit()
        token = usuario.gerar_token_confirmar()
        enviar_email(
            usuario.email,
            "Confirme sua conta",
            "confirmar",
            usuario=usuario,
            token=token,
        )
        flash("Um email de confirmação foi enviado para o seu email.")
        return redirect(url_for("login"))
    return render_template("cadastro.html", form=form)


@app.route("/confirmar/<token>")
@login_required
def confirmar(token):
    if current_user.confirmado:
        return redirect(url_for("index"))
    if current_user.confirmar(token):
        db.session.commit()
        flash("Conta confirmada com sucesso. Bem vindo!")
    else:
        flash("O Link de confirmação é inválido ou expirou.")
    return redirect(url_for("index"))


@app.route("/confirmar")
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
    return redirect(url_for("index"))


@app.route("/alterar-senha", methods=["GET", "POST"])
@login_required
def alterar_senha():
    form = AlterarSenhaForm()
    if form.validate_on_submit():
        if current_user.verifica_senha(form.senha_antiga.data):
            current_user.senha = form.senha.data
            db.session.add(current_user)
            db.session.commit()
            flash("Sua senha foi alterada com sucesso.")
            return redirect(url_for("index"))
        else:
            flash("Senha inválida.")
    return render_template("alterar_senha.html", form=form)


@app.route("/reset", methods=["GET", "POST"])
def requisicao_reset_senha():
    if not current_user.is_anonymous:
        return redirect(url_for("index"))
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
                "resetar_senha",
                usuario=usuario,
                token=token,
            )
        flash(
            """Um email contendo as instruções para\
                    o reset de senha foi enviado para você"""
        )
        return redirect(url_for("login"))
    return render_template("reset_senha.html", form=form)


@app.route("/reset/<token>", methods=["GET", "POST"])
def reset_senha(token):
    if not current_user.is_anonymous:
        return redirect(url_for("index"))
    form = SenhaResetaForm()
    if form.validate_on_submit():
        if Usuario.reset_senha(token, form.senha.data):
            db.session.commit()
            flash("Sua senha foi atualizada com sucesso.")
            return redirect(url_for("login"))
        else:
            return redirect(url_for("index"))
    return render_template("/reset_senha.html", form=form)


@app.route("/alterar_email", methods=["GET", "POST"])
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
                "altera_email",
                usuario=current_user,
                token=token,
            )
            flash(
                "Enviamos Email contendo as instruções para confirmar"
                " o novo endereço de email "
                " foi enviado para você."
            )
            return redirect(url_for("index"))
        else:
            flash("Email ou senha inválido.")
    return render_template("/alterar_email.html", form=form)


@app.route("/home/")
def home():
    usuarios = Usuario.query.order_by(Usuario.username).all()
    return render_template("home.html", usuarios=usuarios)


@app.route("/alterar_email/<token>")
@login_required
def alterar_email(token):
    if current_user.alterar_email(token):
        db.session.commit()
        flash("Seu email foi atualizado com sucesso.")
    else:
        flash("Requisição inválida.")
    return redirect(url_for("index"))


@app.route("/usuario/<username>")
def usuario(username):
    usuario = Usuario.query.filter_by(username=username).first_or_404()
    return render_template("usuario.html", usuario=usuario)


@app.errorhandler(500)
def server_error(e):
    logging.exception('Ocorreu um erro durante a requisição.')
    return """
    Ocorreu um erro no servidor durante a requisição: <pre>{}</pre>
    Analise os logs para entender o que aconteceu.
    """.format(e), 500
