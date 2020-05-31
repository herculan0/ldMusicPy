from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextAreaField,
    RadioField,
)
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Usuario


class LoginForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Length(1, 64), Email()]
    )
    senha = PasswordField("Senha", validators=[DataRequired()])
    remember_me = BooleanField("Lembrar de mim")
    submit = SubmitField("Entrar")


class CadastroForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Length(1, 80), Email()]
    )
    username = StringField(
        "Usuario",
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(
                "^[A-Za-z][A-Za-z0-9.]*$",
                0,
                "Nomes de Usuário devem conter somente letras,números ou pontos",
            ),
        ],
    )
    senha = PasswordField(
        "Senha", validators=[DataRequired(), EqualTo("senha2")]
    )
    senha2 = PasswordField("Confirmar Senha", validators=[DataRequired()])
    endereco = TextAreaField(
        "Endereço", validators=[DataRequired(), Length(1, 180)]
    )
    tipoUsuario = RadioField(
        "Você é Aluno ou Instrutor?",
        choices=[("Aluno", "aluno"), ("Instrutor", "instrutor")],
    )
    submit = SubmitField("Cadastrar")

    def validar_email(self, field):
        if Usuario.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("Email já em está em uso.")

    def validar_username(self, field):
        if Usuario.query.filter_by(username=field.data.lower()).first():
            raise ValidationError("Usuario já cadastrado")


class AlterarSenhaForm(FlaskForm):
    senha_antiga = PasswordField("Senha Antiga", validators=[DataRequired()])
    senha = PasswordField(
        "Nova Senha",
        validators=[
            DataRequired(),
            EqualTo("senha2", message="As senhas devem ser iguais."),
        ],
    )
    senha2 = PasswordField("Confirmar Nova Senha", validators=[DataRequired()])
    submit = SubmitField("Atualizar Senha")


class RequisicaoResetaSenhaForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Length(1, 64), Email()]
    )
    submit = SubmitField("Resetar Senha")


class SenhaResetaForm(FlaskForm):
    senha = PasswordField(
        "Nova Senha",
        validators=[
            DataRequired(),
            EqualTo("senha2", message="As senhas devem ser iguais."),
        ],
    )
    senha2 = PasswordField("Confirmar Nova Senha", validators=[DataRequired()])
    submit = SubmitField("Resetar Senha")


class AlterarEmailForm(FlaskForm):
    email = StringField(
        "Novo Email", validators=[DataRequired(), Length(1, 64), Email()]
    )
    senha = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Atualizar Endereço de Email")

    def validar_email(self, field):
        if Usuario.query.filter_by(field.data.lower()).first():
            raise ValidationError("Email já está Cadastrado.")