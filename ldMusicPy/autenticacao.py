import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from .models import CadastroForm, LoginForm

bp = Blueprint('autenticacao', __name__, url_prefix='/autenticacao')

@bp.route('/cadastro', methods=['GET','POST'])
def cadastro():
    form = CadastroForm()

    if 'email' in session:
        return redirect(url_for('perfil'))

    if requested.method == 'POST':
        if form.validade == False:
            return render_template('cadastro.html', form=form)
        else:
            usuario = Usuario(form.primeiroNome.data,
                           form.ultimoNome.data,
                           form.email.data,
                           form.dataNascimento.data,
                           form.senha.data,
                           form.funcao.data,
                           form.videoURL.data)
            db.session.add(usuario)
            db.session.commit()
            session['usuario_id'] = usuario.id
            session['email'] = usuario.email
            return redirect(url_for('perfil'))

    return render_template('cadastro.html', form=form)

@bp.before_app_request
def carregar_usuario_logado():
    usuario_id = session.get('usuario_id')
    if usuario_id == None:
        g.usuario = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if 'email' in session:
        return redirect(url_for('perfil'))
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('entrar.html', form=form)
        else:
            email = form.email.data['email']
            senha = form.senha.data['senha']
            db = get_db()
            error = None
            usuario = db.execute(
                'SELECT * FROM usuario WHERE email = ?', (email,)
            ).fetchone()
            if usuario is None:
                error = 'Email Invalido.'
            elif not check_password_hash(usuario['senha'], senha):
                error = 'Senha incorreta.'

            if error is None:
                session.clear()
                session['usuario_id'] = usuario['id']
                return redirect(url_for('perfil'))
            flash(error)


    elif request.method == 'GET':
        return render_template('autenticacao/login.html', form=form)

@bp.route('/sair')
@bp.route('/logout')
def sair():
    session.clear()
    return redirect(url_for('home'))

