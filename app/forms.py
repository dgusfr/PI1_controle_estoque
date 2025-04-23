from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    """
    Formulário de login.
    """
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=2, max=64)])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me') # Campo para 'Lembrar-me'
    submit = SubmitField('Entrar')