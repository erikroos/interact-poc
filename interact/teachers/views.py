from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from interact.teachers.forms import LoginForm
from interact.teachers.models import User

teachers_blueprint = Blueprint('teachers', __name__, template_folder='templates')

@teachers_blueprint.route("/")
def index():
    return render_template("index_teachers.html")

@teachers_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    feedback = None

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('teachers.index'))
        else:
            feedback = "Foutieve login."

    return render_template("login.html", form=login_form, feedback=feedback)

@teachers_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Je bent nu uitgelogd.")
    return redirect(url_for('home'))

@teachers_blueprint.route('/create')
@login_required
def create():
    return render_template("new_seminar.html")