from flask import Blueprint

autenticacao = Blueprint('autenticacao', __name__)

from . import views