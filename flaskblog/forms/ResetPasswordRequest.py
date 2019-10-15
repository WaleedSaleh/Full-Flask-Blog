from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flaskblog.Models.User import User
from flask import flash


class ResetPasswordRequest(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password Request')

    def checkEmail(self, email):
        user = User.query.filter_by(email=email).first()
        return True if user else flash('Email is inccorrect please sing up to be able to reset your password!', 'warning')
