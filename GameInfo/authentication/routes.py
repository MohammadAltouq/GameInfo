from flask import Blueprint, render_template, redirect, request, url_for, flash
from GameInfo.forms import UserSignupForm, UserSigninForm
from GameInfo.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder= 'auth_templates')


@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserSignupForm()
    try:
        if request.method == "POST" and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            username = form.username.data
            password = form.password.data

            user = User(first_name, last_name, email, username, password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have succesfully created a user account {email}', "user-created")

            return redirect(url_for('auth.signin'))

    except:
        flash('Invalid Form Data: Please Check Your Form')
        # raise Exception('Invalid Form Data: Please Check Your Form')
        
        
    return render_template('signup.html', form = form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserSigninForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash("you were succesfully logged in via Email/Password","auth-success")
                return redirect(url_for('site.profile'))
    except:
        raise Exception('Invalid Form DATA: please check your form and try again')

    return render_template('signin.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))