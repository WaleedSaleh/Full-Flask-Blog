from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import EqualTo, Length, DataRequired

class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=50)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), Length(min=6, max= 50),EqualTo('password')])
    submit = SubmitField('Reset Password')