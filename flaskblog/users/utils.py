import secrets
import os
from flask import url_for, redirect,flash, current_app
from werkzeug.utils import secure_filename
from PIL import Image
from flaskblog import db, bcrypt, mail
from flask_login import current_user
from flask_mail import Message as MailMessage

def updateUserInfo(form):
    if form.checkUsername(form.username.data) and form.checkEmail(form.email.data):
        current_user.email = form.email.data
        current_user.username = form.username.data
        db.session.commit()
        flash("Your Information Updated Successfully", 'success')
        return redirect(url_for('profile'))
    else:
        if not form.checkUsername(form.username.data) and not form.checkEmail(form.email.data):
            flash('Email and Username already taken, Please Try another ones', 'danger')
            pass
        elif not form.checkUsername(form.username.data):
            flash('Username already taken, Please Try another one', 'danger')
        elif not form.checkEmail(form.email.data):
            flash('Email already taken, Please Try another one', 'danger')


def save_iamge(image):
    random_hex = secrets.token_hex(8)
    _, ext_name = os.path.splitext(image.filename)
    image_name = secure_filename(random_hex + ext_name)
    image_path = os.path.join(current_app.root_path, 'static/imgs/profile_pics/', image_name)
    # saving image and specify the size using the pillow library
    # ---------------------
    image_size = (125, 125)
    im = Image.open(image)
    im.thumbnail(image_size)
    im.save(image_path)
    # ---------------------
    return image_name

def send_reset_email(user):
    token = user.reset_token()
    try:
        msg = MailMessage(subject='Password Reset Request',
                          sender='no-reply@demo.com',
                          recipients=[user.email])

        msg.body = f'''To reset your password please visit the following link
        {url_for('reset_password', token=token, _external=True)}
        If you didn't make this request, Ignore this email and nothing is gonna change.
        '''''
        mail.send(message=msg)
    except Exception as e:
        raise e

def new_password(form, user):
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if bcrypt.check_password_hash(hashed_password, form.password.data):
            user.password = hashed_password
            db.session.commit()
            flash('Your password Changed Successfully, You can login now :)', 'success')
            return redirect(url_for('login'))