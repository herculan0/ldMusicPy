from ldm import app
from flask import render_template, request, flask, session, url_for, redirect, current_app, send_from_directory
from .auth/forms import CadastroForm, LoginForm
from flask.ext.mail import Message, Mail
from models import db, Usuario

mail = Mail()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
@app.route('/home')
def home():
    return render_template('main.html',
                           current_time=datetime.utcnow())

@app.route('/about')
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/usuario/<name>')
def get_usuario(id):
    usuario = load_usuario(id)
    if not usuario:
        abort(404)
    return render_template('usuario.html', usuario=usuario)

@bp.route('/perfil')
def perfil():
    if 'email' not in session:
        return redirect(url_for('cadastro'))
    usuario = usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        return redirect(url_for('cadastro'))
    else:
        return render_template('perfil.html')

@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(current_app.config.get('MEDIA_ROOT'),filename)
