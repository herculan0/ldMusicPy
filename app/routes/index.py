from flask import render_template
from . import rotas

@rotas.route("/")
def index():
     return render_template("main.html")
