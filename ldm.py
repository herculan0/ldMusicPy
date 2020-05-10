import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__, '.env'))
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

cov = None
if os.environ.get('flask_coverage)'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

# CONEXÃO DO DRIVER CONECTOR MYSQL #

# connection = pymysql.connect(host='127.0.0.1',
#                              user='admin',
#                              password='ldmusic',
#                              db='ldMusic',
#                              charset='utf8mb4')


import sys
import click
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import Permissao, Funcao, Usuario

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Usuario=Usuario, Permissao = Permissao, Funcao = Funcao)

@app.cli.command()
@click.option('--coverage/--no-coverage', default=False,
              help='Executando com cobertura do código.')
@click.argument('nome_testes', nargs=-1)
def test(coverage, nome_testes):
    """Executar testes unitários."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(sys.argv))

    import unittest
    if nome_testes:
        tests = unittest.TestLoader().loadTestsFromNames(nome_testes)
    else:
        tests = unittest.Test.Loader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Sumário:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir,'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML Version: file://%s/index.html' % covdir)
        COV.erase()

@app.cli.command()
@click.option('--length', default=25,
              help='Número de funções para incluir no perfil de relatório')
@click.option('--profile-dir', default=None,
              help='Diretório onde o perfil de arquivos de dados serão salvos')
def profile(length, profile_dir):
    """Iniciar a aplicação sobre o perfil de código"""
    from wekzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


@app.cli.command()
def deploy():
    """Executar tarefas de implementação"""

    upgrade()

    Funcao.inserir_funcoes()

