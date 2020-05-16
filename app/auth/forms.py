from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Password

class CadastroForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    nome = StringField('Primeiro Nome', validators=[DataRequired()])
    email = StringField ('Email', validators=[DataRequired(), Email])
    senha = StringField ('Senha', validators=[DataRequired(), Password])
