from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class StaffForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password (leave empty to keep current)', validators=[Optional()])
    role = SelectField('Role', choices=[('Employee', 'Employee'), ('Admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Save Staff')
