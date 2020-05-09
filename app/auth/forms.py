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
    username = StringField('Usuario', validators=[
        DataRequired(), Length(1,64),
        Regexp('^[A-Za-z][A-Za-z0-9.]*$', 0,
               'Nomes de Usuário devem conter somente letras, números ou pontos')
    ])
    senha = PasswordField('Senha', validators=[DataRequired(), EqualTo('senha2', message='Senhas não são iguais.')])
    senha2 = PasswordField('Confirmar Senha', validators=[DataRequired()])
    nome = StringField('Nome Completo', validators[
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
    submit SubmitField('Resetar Senha')

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
