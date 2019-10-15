from flaskblog import bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email
from flaskblog.Models.User import User
from flask_login import login_user


class Login(FlaskForm):
    email = StringField('Username', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    # We're gonna add a remember field to allow the user to stay login for a while after closing the browser using  secure cookies
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


    def checkLoginValidity(self,form):
        user = User.query.filter_by(email=form.email.data).first()
        if form.validate_on_submit():
            if user and bcrypt.check_password_hash(user.password, form.password.data):
               login_user(user,remember=form.remember_me.data)
               return True
            else:
                return False