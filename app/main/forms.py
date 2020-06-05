from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class EditarPerfilForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    endereco = StringField('Endereço', validators=[Length(1, 180)])
    sobre_mim = TextAreaField('Sobre mim')
    submit = SubmitField('Atualizar')

class Relatorio(FlaskForm):
    filtro = SelectField('Filtro', choices=[('n', 'Nome'),('instrumento', 'Instrumento'),('cidade', 'Cidade')])
    busca = StringField('Busca', validators=[Length(1, 180)])