from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import Length, DataRequired


class Posts(FlaskForm):
    post_field = TextAreaField("What's going on today ?", validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired(),Length(min=5)])
    submit = SubmitField('Post')

