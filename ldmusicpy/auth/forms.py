from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64),
                                             Email()])
    senha = PasswordField('Sennha', validators=[DataRequired()])
    remember_me = BooleanField('Me mantenha Logado')
    submit = SubmitField('Entrar')

class CadastroForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64),
                                             Email()])
    usuario = StringField('Usuário', validators=[
        DataRequired(), Length(1,64),
        Regexp('^[A-Za-z][A-Za-z0-9.]*$', 0,
               'Nomes de Usuário devem conter somente letras, números ou pontos')
    ])
    senha = PasswordField('Senha', validators=[DataRequired(), EqualTo('confirmaSenha', message='Senhas não são iguais.')])
    confirmaSenha = PasswordField('Confirmar Senha', validators=[DataRequired()])
    primeiroNome = StringField('Primeiro Nome', validators[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z]*$', 0,
               'Nomes devem conter apenas texto.')])
    ultimoNome = StringField('Último Nome', validators[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z]*$', 0,
               'Nomes devem conter apenas texto.')])
    submit = SubmitField('Cadastrar')

    def validar_email(self, field):
        if Usuario.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email já em está em uso.')

    def validar_usuario(self, field):
        if Usuario.query.filter_by(usuario=field.data.lower()).first():
            raise ValidationError('Usuario já cadastrado')

# Criar Formulário para Alteração de Senha


# Criar formulário para Solicitação Reset de Senha


# Criar formulário para Reset de Senha


# Criar Formulário para Alteração de Email



