import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Olá, usuário!"

@app.route('/<usuario>')
def perfil():
    return jsonify(nome="{}".format(usuario))
