from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, PasswordField
from wtfforms.validators import DataRequired, Length, Email, URL

class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Me mantenha logado!')
    submit = SubmitField('Entrar')


class SignupForm(FlaskForm):
    primeiroNome = StringField('Primeiro Nome:', validators=[DataRequired()])
    ultimoNome = StringField('Último Nome:')
    email = StringField('Email:', validators=[Email(), DataRequired()])
    dataNascimento = DataField('Data de Nascimento: ', validators=[DataRequired()])
    senha = PasswordField('Senha: ' validators=[DataRequired()])
    confirmaSenha = PasswordField('Confirmar Senha ' validators=[DataRequired(), EqualTo(senha)])
    funcao = RadioField('Aluno ou Instrutor', validators=[DataRequired()])
    videoURL = StringField('Link do Vídeo: ', validator=[URL()])
    submit = SubmitField('Cadastrar')
