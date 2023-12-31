from flask import Blueprint, render_template, request, flash, redirect, url_for
from .model_user import User
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Authenticates the user login.

    Returns:
        rendered_template: Rendered HTML template for the login page.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('bp_home.do_home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login/login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    """
    Logs out the user.

    Returns:
        redirect: Redirects the user to the login page.
    """
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """
    Handles the user sign-up process.

    Returns:
        rendered_template: Rendered HTML template for the sign-up page.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('bp_home.do_home'))

    return render_template("login/sign_up.html", user=current_user)


@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password(user_id):
    """
    Resets the user password.

    Args:
        user_id (int): The ID of the user.

    Returns:
        redirect: Redirects the user to the login page.
    """
    # Retrieve the user data from the database
    user = User.query.get(user_id)

    if user:
        if request.method == 'POST':
            user.email = request.form.get('email')
            user.password = request.form.get('password')

            db.session.commit()
            flash('Password updated successfully', 'success')
            return redirect(url_for('auth.login'))

        return render_template('login/reset_password.html', email=user.email, password=user.password)
    else:
        flash('Email not found', 'error')

    return redirect(url_for('auth.login'))
