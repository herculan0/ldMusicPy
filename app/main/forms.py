from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class EditarPerfilForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    endereco = StringField('Endereço', validators=[Length(1, 180)])
    sobre_mim = TextAreaField('Sobre mim')
    submit = SubmitField('Atualizar')

# class Relatorio(FlaskForm):
#     filtro = StringField('filtro', validator=[DataRequired()])