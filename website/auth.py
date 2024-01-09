from flask import Blueprint, render_template, request, flash, redirect, url_for,current_app
from .models import User,Quiz
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from . import db  
from flask_login import login_user, login_required, logout_user, current_user
import json
import uuid
from os import path

auth = Blueprint('auth', __name__)

# API + View Route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/profile")

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.get_profile'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

# Logout Route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# API + View Route
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect("/profile")
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('fullName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        image = request.files["profile_pic"]
        file_extension = image.filename.split(".")[-1]
        file_name = f'{uuid.uuid4().hex}.{file_extension}'

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
            
            img_path = path.join(current_app.config['UPLOAD_FOLDER'], file_name)
            image.save(img_path)
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='scrypt'),profile_pic=file_name)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user=current_user)

# View Route
@auth.route("/profile",methods=["GET"])
@login_required
def get_profile():
    profile_pic = User.query.filter_by(id=current_user.get_id()).first().toMap()["profile_pic"]
    return render_template("profile.html",user=current_user,profile_pic=profile_pic)