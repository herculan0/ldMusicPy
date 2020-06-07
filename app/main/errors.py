from flask import render_template, request, jsonify
from . import main


@main.app_errorhandler(403)
def nao_permitido(e):
    if request.accept_mimetypes.accept_html and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'acesso proibido'})
        response.status_code = 403
        return response
    return render_template('403.html'), 403


@main.app_errorhandler(404)
def pagina_nao_encontrada(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'pagina nao encontrada'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def erro_interno_servidor(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'erro interno no servidor'})
        response.status_code = 500
        return response
    return render_template('500.html'), 500
