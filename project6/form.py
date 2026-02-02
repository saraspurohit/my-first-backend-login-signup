from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import data_required,Email,Length

class RegistrationForm(FlaskForm):
    name=StringField("Full name",validators=[data_required()])
    email=StringField("Email",validators=[data_required(),Email()])
    password=PasswordField("Password",validators=[data_required(),Length(min=6)])
    submit=SubmitField("Register")