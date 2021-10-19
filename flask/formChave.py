from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ChaveForm(FlaskForm):
    nome = StringField('Nome da chave', validators=[DataRequired()])
    enviar = SubmitField('CADASTRAR')