from flask import Blueprint, render_template, request, redirect, url_for, flash
from flaskblog import db
from flask_login import current_user, login_required, logout_user
from flaskblog.users.utils import save_iamge, updateUserInfo, new_password, send_reset_email
from flaskblog.forms.LoginForm import Login
from flaskblog.forms.RegistrationForm import Registration
from flaskblog.forms.UpdateProfileForm import UpdateProfileForm
from flaskblog.forms.ResetPasswordRequest import ResetPasswordRequest
from flaskblog.forms.ResetPassword import ResetPassword
from flaskblog.Models.User import User

users = Blueprint('users', __name__, template_folder='templates')


@users.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_page.home'))
    # creating an instance of the LoginForm to pass it to the view
    form = Login()
    if request.method == 'POST':
        if form.checkLoginValidity(form):
            next = request.args.get(
                'next')
            return redirect(url_for('main_page.home', username=current_user.username)) if next else redirect(
                url_for('main_page.index', username=current_user.username))
        else:
            flash(f"{form.email.data} and/or Password are incorrect. Please try again!", 'danger')

    return render_template('login.html', title="Login", form=form)


@users.route('/registration', methods=['GET', 'POST'])
def registration():
    # this issue is checking for the user if logged on or not and to customize the routes for the logged on user
    if current_user.is_authenticated:
        return redirect(url_for('main_page.home'))
    # creating an instance of the form to pass it to the view
    form = Registration()
    if request.method == "POST":
        if form.checkValidity(form):
            return redirect(url_for('users.login'))
        else:
            pass
    return render_template('registration.html', title="Registration", form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            current_user.image_file = save_iamge(form.picture.data)
            db.session.commit()
        updateUserInfo(form)
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    image_file = url_for('static', filename='imgs/profile_pics/' + current_user.image_file)
    return render_template('profile.html', title=current_user.username + ' Profile', image_file=image_file,
                           current_user=current_user, form=form)


@users.route('/request-reset-password', methods=['POST', 'GET'])
def request_reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))
    form = ResetPasswordRequest()
    if form.validate_on_submit():
        if form.checkEmail(form.email.data):
            user = User.query.filter_by(email=form.email.data).first()
            send_reset_email(user)
            flash('An email with instruction to reset your password has been sent', 'info')
            return redirect(url_for('users.login'))
        else:
            pass
    return render_template('reset_password_request.html', form=form, title='Reset Password Request')


@users.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))
    user = User.verify_token(token)
    if user is None:
        flash("The requested token is invalid or expired", 'warning')
        return redirect(url_for('users.request_reset_password'))
    form = ResetPassword()
    new_password(form, user)
    return render_template('reset_password.html', form=form, title='Reset Password')
