from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                 flash('Logged in succesfully!', category='sucess')
                 login_user(user, remember=True)
                 return redirect(url_for('views.home'))

            else:
                flash('incorrect password, try again', category='error')
        else:
            flash('Email doesnt exist',category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('email must be greater than 3 char', category='error')
            pass
        elif len(first_name) < 2:
            flash('firstName must be greater than 1 char', category='error')
            pass
        elif password1 != password2:
            flash('password dont match', category='error')
            pass
        elif len(password1) < 6:
            flash('Password to short. At least 6char.', category='error')
            pass
        else:
            # add user to database
            new_user = User(email=email, first_name=first_name,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Acc created', category='success')
            return redirect(url_for('views.home'))

        print(email, first_name, password1, password2)
    return render_template('sign_up.html', user=current_user)
