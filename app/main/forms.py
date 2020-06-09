from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, Email


class EditarPerfilForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    endereco = StringField('Endereço', validators=[Length(1, 180)])
    sobre_mim = TextAreaField('Sobre mim')
    submit = SubmitField('Atualizar')

class Relatorio(FlaskForm):
    filtro = SelectField('Filtro', choices=[('nome', 'Nome'),('instrumento', 'Instrumento'),('cidade', 'Cidade')])
    usuario = SelectField('Usuario', choices=[('aluno', 'aluno'),('instrutor', 'instrutor')])
    busca = StringField('Busca', validators=[Length(1, 180)])

class PerfilAdministrador(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
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
    email = StringField(
        "Email", validators=[DataRequired(), Length(1, 64), Email()]
    )
    endereco = TextAreaField(
        "Endereço", validators=[DataRequired(), Length(1, 180)]
    )

class PerfilUsuario(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
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
    email = StringField(
        "Email", validators=[DataRequired(), Length(1, 64), Email()]
    )
    endereco = TextAreaField(
        "Endereço", validators=[DataRequired(), Length(1, 180)]
    )

    instrumento = SelectField('Instrumento', choices=[('violao', 'violao'),('bateria', 'bateria'),('guitarra', 'guitarra')])
    nivel_conhecimento = SelectField('Nivel', choices=[('nenhum', 'nenhum'),('basico', 'basico'),('medio', 'medio'), ('avancado', 'avancado')])

class Instrumentos(FlaskForm):
    instrumento = SelectField('Instrumento', choices=[('violao', 'violao'),('bateria', 'bateria'),('guitarra', 'guitarra')])
