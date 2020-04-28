from flask import Flask, request, abort, redirect, render_template
from flask_bootstrap import Boostrap

def criar_app()
    app = Flask(__name__)
    Boostrap(app)

    return app

@app.route('/')
def index():
    return render_template(index.html)

@app.route('/u/<nome>')
def Usuario(nome):
    return render_template('usuario.html', name=name)

@app.route('/u/<id>')
    def get_usuario(id):
    usuario = carrega_usuario
    if not usuario:
        abort(404)
    return '<h1>Hello, {}!</h1>'.format(usuario.nome)


if __name__=='__main__':
    app.run()
