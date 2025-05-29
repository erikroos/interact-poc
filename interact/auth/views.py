from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from interact import db
from interact.auth.forms import LoginForm, RegistrationForm
from interact.models import User

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        user = User(reg_form.username.data, generate_password_hash(reg_form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Thank you for registering as a teacher! You can now log in.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=reg_form)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next = request.args.get('next')
            if next == None or not next[0] == '/':
                if user.role == "admin":
                    next = url_for("admin.index")
                else:
                    next = url_for('teachers.index')
            return redirect(next)
        else:
            flash("Incorrect login")

    return render_template("login.html", form=login_form)

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are now logged out")
    return redirect(url_for('home'))