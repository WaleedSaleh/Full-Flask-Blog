from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog import db
from flaskblog.Models.User import User


# importing the wtf_forms in order to make and validate the fields we want to use
# The stringField Represent the type of the field we want
# We pass the validator into a list
# importing the validator to validate the forms, by assigning the class we want to use.
# DataRequired specifies that the field can't be empty
# Length to assign the length of input
class Registration(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=6, max=30)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=30)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), Length(min=6, max=30),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')

    # ------------Validation Fields-----------------

    def checkValidity(self, form):
        if form.validate_on_submit():
           return True if self.saveUserToDatabase(form) else False

    def checkEmail(self, email):
        user = User.query.filter_by(email=email).first()
        if user:
            raise ValidationError("Email is taken, please try something else!")

    def checkUsername(self, username):
        user = User.query.filter_by(username=username).first()
        if user:
            raise ValidationError("Username is taken, please try something else!")

    def saveUserToDatabase(self, form):
        with db.session.no_autoflush:  # to avoid auto flush
            user = User(username=form.username.data, email=form.email.data)
            password = form.password.data
            username = form.username.data
            email = form.email.data
            user.setHashedPassword(password)
            db.session.add(user)
            username_query = User.query.filter_by(username=username).first()
            email_query = User.query.filter_by(email=email).first()
            try:
                if user.checkHashedPassword(password) and not username_query and not email_query:
                    db.session.commit()
                    flash(f"Account has been created, you can now login :) !", 'success')
                    return True
                else:
                    db.session.rollback()
                    flash("{} or {} already exist, Try another one!".format(username, email), 'info')
                    return False
            except Exception as e:
                raise ('Something went wrong through saving to database, ' + e)
            finally:
                db.session.close()

