import os
import hashlib
import bleach
#from dotenv import load_dotenv
#dotenv_path = os.path.join(os.path.dirname(__file__) '.env.')

from flask import Flask, request, url_for, current_app, redirect, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

from flask_bootstrap import Bootstrap
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy ## importar banco
from flask_login import LoginManager, UserMixin, AnonymousUserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from threading import Thread

from flask_moment import Moment


### cria objetos das bibliotecas ###
db = SQLAlchemy()
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
login_manager = LoginManager()
pagedown = PageDown()

### instancia um objeto da aplicação chamado app ##
app = Flask(__name__)


### configuração importada em .env e config.py onde colocaremos as variáveis de
#ambiente necessárias ###
app.config.from_object(os.environ['APP_SETTINGS'])


### instancia um objetos da aplicacao###
bootstrap.init_app(app)
mail.init_app(app)
db.init_app(app)
login_manager.init_app(app)
moment.init_app(app)
pagedown.init_app(app)
## MODELS ###

### cria classe para dar permissões aos usuários ###
class Permissao:
    COMENTAR = 2
    ESCREVER = 4
    ADMIN = 16 

### classe funcao, onde invoca permissoes para admin ou usuario comum ###
class Funcao(db.Model):
    __tablename__ = 'funcao'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True)
    padrao = db.Column(db.Boolean, default=False, index=True)
    permissoes = db.Column(db.Integer)
    usuarios = db.relationship('Usuario', backref='funcao', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Funcao, self).__init__(**kwargs)
        if self.permissoes is None:
            self.permissoes = 0

    @staticmethod
    def inserir_funcoes():
        funcoes = {
            'Usuario': [Permissao.COMENTAR,
                        Permissao.ESCREVER],
            'Administrador':[Permissao.COMENTAR,
                             Permissao.ESCREVER,
                             Permissao.ADMIN]
        }
        funcao_padrao = 'Usuario'
        for f in funcoes:
            funcao = Funcao.query.filter_by(nome=f).first()
            if funcao is None:
                funcao = Funcao(nome=f)
            funcao.reset_permissoes(perm)
            for perm in funcoes[f]:
                funcao.add_permissao(perm)
            funcao.padrao = (funcao.nome == funcao_padrao)
            db.session.add(funcao)
        db.session.commit()

    def add_permissao(self, perm):
        if not self.tem_permissao(perm):
            self.permissoes += perm

    def remover_permissao(self):
        self.permissoes = 0

    def tem_permissao(self, perm):
        return self.permissoes & perm == perm

    def __repr__(self):
        return '<Funcao %f>' % self.nome

### classe usuário ###
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128))
    funcao_id = db.Column(db.String, db.ForeignKey('funcao.id'))
#    tipo_usuario = db.Column(db.String(25), nullable=False)
    sobre_mim = db.Column(db.Text())
    data_cadastro = db.Column(db.DateTime(), default=datetime.utcnow)
    confirmado = db.Column(db.Boolean, default=1)

    def __init__(self, **kwargs):
        super(Usuario, self).__init__(**kwargs)
    
    @property
    def senha(self):
        raise AttributeError('Senha não é um atributo legível.')

    ### gera o hash da senha para guardar no banco ###
    @senha.setter
    def senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
    
    ### verifica se o hash bate com a senha ###
    def verifica_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    ### gerar token para confirmação de email ###
    def gerar_token_confirmar(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirmar': self.id}).decode('utf-8')
    
    ### usuário precisa confirmar no email o cadastro ###
    def confirmar(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirmar') != self.id:
            return False
        self.confirmado = True
        db.session.add(self)
        return True

    ### gerar o token para reset de senha ###
    def gerar_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirmar': self.id}).decode('utf-8')

    ### recriar senha usuário ###

    @staticmethod
    def reset_senha(token, nova_senha):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        usuario = Usuario.query.get(data.get('reset'))
        if user is None:
            return False
        usuario.senha = nova_senha
        db.session.add(usuario)
        return True

    ### cria um token para alteração do email ###
    def gerar_altera_email_token(self, novo_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'altera_email': self.id, 'novo_email': novo_email}).decode('utf-8')

    ### altera o email no banco ###
    def altera_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('altera_email') != self.id:
            return False
        novo_email = data.get('novo_email')
        if novo_email is None:
            return False
        if self.query.filter_by(email=novo_email).first() is not None:
            return False
        self.email = novo_email
        self.avatar_hash = self.gravatar_hash()
        db.session.add(self)
        return True

    ### adiciona permissão de admin ###
    def perm(self, perm):
        return self.can(Permissao.ADMIN)

    ### atualiza a ultima_visualizacao do usuario no banco ###
    def ping(self):
        self.ultima_visualizacao = datetime.utcnow()
        db.session.add(self)
    
    ### gera um hash para o avatar do usuario ###
    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    ### gera um avatar ###
    def gravatar(self, size=100, default='identicon', rating='g'):
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

### cria usuário anônimo retornando falso para qualquer permissão ###
class UsuarioAnonimo(AnonymousUserMixin):
    def can(self,permissoes):
        return False
    def administrador():
        return False
with app.app_context():
    db.create_all()

login_manager.anonymous_user = UsuarioAnonimo

## método para carregar usuário ##
@login_manager.user_loader
def carrega_usuario(id):
    return Usuario.query.get(int(id))

#### formularios de login, cadastro e recupera/altera senha e reset email###

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64),
                                             Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar de mim')
    submit = SubmitField('Entrar')

class CadastroForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64),
                                             Email()])
    username = StringField('Usuario', validators=[
        DataRequired(), Length(1,64),
        Regexp('^[A-Za-z][A-Za-z0-9.]*$', 0,
               'Nomes de Usuário devem conter somente letras, números ou pontos')
    ])
    senha = PasswordField('Senha', validators=[DataRequired(), EqualTo('senha2', message='Senhas não são iguais.')])
    senha2 = PasswordField('Confirmar Senha', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')
    
    ### valida se o email já existe ###
    def validar_email(self, field):
        if Usuario.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email já em está em uso.')
    ### valida se o username ja foi cadastrado
    def validar_username(self, field):
        if Usuario.query.filter_by(username=field.data.lower()).first():
            raise ValidationError('Usuario já cadastrado')


class AlterarSenhaForm(FlaskForm):
    senha_antiga = PasswordField('Senha Antiga', validators = [DataRequired()])
    senha = PasswordField('Nova Senha', validators=[
        DataRequired(), EqualTo('senha2', message='As senhas devem ser iguais.')])
    senha2 = PasswordField('Confirmar Nova Senha',
                           validators=[DataRequired()])
    submit = SubmitField('Atualizar Senha')

class RequisicaoResetaSenhaForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64),
                                             Email()])
    submit = SubmitField('Resetar Senha')

class SenhaResetaForm(FlaskForm):
    senha = PasswordField('Nova Senha', validators=[
        DataRequired(), EqualTo('senha2', message='As senhas devem ser iguais.')])
    senha2 = PasswordField('Confirmar Nova Senha',
                           validators=[DataRequired()])
    submit = SubmitField('Resetar Senha')

class AlterarEmailForm(FlaskForm):
    email = StringField('Novo Email', validators=[DataRequired(), Length(1,64),
                                             Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Atualizar Endereço de Email')

    def validar_email(self, field):
        if Usuario.query.filter_by(field.data.lower()).first():
            raise ValidationError('Email já está Cadastrado.')

#### funções de envio de email####
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_mail(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['LDM_MAIL_SUBJECT_PREFIX'] + ' ' + subject, sender=app.config['LDM_MAIL_SENDER'],
            recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

#### ROTAS (/, /sobre, /login, /cadastro,  /<instrumento>, /<instrutor>, /<aluno>) ####

### cria uma rota para o / ou seja 127.0.0.1:5000 ou localhost:5000 ###
@app.route('/')
def index():
    return render_template('index.html')


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmado \
                and request.endpoint \
                and request.endpoint != 'static':
            return redirect(url_for('nao_confirmado'))

@app.route('/nao_confirmado')
def nao_confirmado():
    if current_user.is_anonymous or current_user.confirmado:
        return redirect(url_for('index'))
    return render_template('/nao_confirmado.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data.lower()).first()
        if usuario is not None and usuario.verifica_senha(form.senha.data):
            login_user(usuario, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('index')
            return redirect(next)
        flash('Email ou senha inválido.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você se deslogou com sucesso.')
    return redirect(url_for('index'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
        usuario = Usuario(email =form.email.data.lower(),
                          username=form.username.data,
                          senha=form.senha.data)
        db.session.add(usuario)
        db.session.commit()
        token = usuario.gerar_token_confirmar()
        send_mail(usuario.email, 'Confirme sua conta',
                   'confirmar', usuario=usuario, token=token)
        flash('Um email de confirmação foi enviado para o seu email.')
        return redirect(url_for('login'))
    return render_template('cadastro.html', form=form)

@app.route('/confirmar/<token>')
@login_required
def confirmar(token):
    if current_user.confirmado:
        return redirect(url_for('index'))
    if current_user.confirmar(token):
        db.session.commit()
        flash('Conta confirmada com sucesso. Bem vindo!')
    else:
        flash('O Link de confirmação é inválido ou expirou.')
    return redirect(url_for('index'))

@app.route('/confirmar')
@login_required
def reenviar_confirmacao():
    token = current_user.gerar_token_confirmar()
    send_mail(current_user.email, 'Confirme sua Conta', 'confirmar',
            usuario=current_user, token=token)
    flash('Um novo email de confirmação foi enviado para o seu email.')
    return redirect(url_for('index'))

@app.route('/alterar-senha', methods=['GET', 'POST'])
@login_required
def alterar_senha():
    form = AlterarSenhaForm()
    if form.validate_on_submit():
        if current_user.verifica_senha(form.senha_antiga.data):
            current_user.senha = form.senha.data
            db.session.add(current_user)
            db.session.commit()
            flash('Sua senha foi alterada com sucesso.')
            return redirect(url_for('index'))
        else:
            flash('Senha inválida.')
    return render_template("alterar_senha.html", form=form)

@app.route('/reset', methods=['GET', 'POST'])
def requisicao_reset_senha():
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    form = RequisicaoResetaSenhaForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data.lower()).first()
        if usuario:
            token = usuario.gerar_reset_token()
            send_mail(usuario.email, 'Resetar sua senha', 'resetar_senha',
                usuario=usuario, token=token)
        flash('Um email contendo as instruções para o reset de senha foi enviado para você')
        return redirect(url_for('login'))
    return render_template('reset_senha.html', form=form)  
