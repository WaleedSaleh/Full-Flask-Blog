from wtforms import StringField,SubmitField,Label
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import Email, DataRequired, Length
from flaskblog.Models.User import User
from flask_login import current_user


class UpdateProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username',validators=[DataRequired(), Length(min=6, max=30)])
    picture = FileField('Upload Picture', validators=[FileAllowed(('png','jpg','jpeg'))])
    submit = SubmitField('Update')

    def checkEmail(self, email):
        print("Entered 1")
        if email != current_user.email:
            user = User.query.filter_by(email=email).first()
            if user:
                return False
        return True

    def checkUsername(self, username):
        print("Entered 2")
        if username != current_user.username:
            user = User.query.filter_by(username=username).first()
            if user:
                return False
        return True
