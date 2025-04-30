from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from interact import db
from interact.teachers.forms import LoginForm, NewSeminarForm
from interact.teachers.models import User, Seminar

teachers_blueprint = Blueprint('teachers', __name__, template_folder='templates')

@teachers_blueprint.route("/")
def index():
    seminars = Seminar.query.all()
    return render_template("index_teachers.html", seminars=seminars)

@teachers_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('teachers.index'))
        else:
            flash("Incorrect login")

    return render_template("login.html", form=login_form)

@teachers_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logged out")
    return redirect(url_for('home'))

@teachers_blueprint.route('/create', methods=["GET", "POST"])
@login_required
def create():
    new_form = NewSeminarForm()
    if request.method == "POST":
        if new_form.validate_on_submit():
            new_seminar = Seminar(new_form.name.data)
            db.session.add(new_seminar)
            db.session.commit()
            return redirect(url_for("teachers.index"))
        else:
            flash("Form not filled in correctly")
        
    return render_template("new_seminar.html", form=new_form)

@teachers_blueprint.route('/activate/<int:id>')
@login_required
def activate(id:int):
    seminar = Seminar.query.filter_by(id=id).first()
    if seminar.active == False:
        seminar.active = True
        db.session.commit()
        flash(f"Seminar is now open. Use code <b>{seminar.code}</b> to share.")
    else:
        seminar.active = False
        db.session.commit()
        flash("Seminar closed")
    return redirect(url_for("teachers.index"))