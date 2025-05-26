from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from interact import db
from interact.teachers.forms import LoginForm, NewSeminarForm, EnrollForm, NewSlideForm, RegistrationForm
from interact.teachers.models import User, Seminar, Student, Slide, Answer

teachers_blueprint = Blueprint('teachers', __name__, template_folder='templates')

@teachers_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        user = User(reg_form.username.data, generate_password_hash(reg_form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Thank you for registering as a teacher! You can now log in.')
        return redirect(url_for('teachers.login'))
    return render_template('register.html', form=reg_form)

@teachers_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('teachers.index')
            return redirect(next)
        else:
            flash("Incorrect login")

    return render_template("login.html", form=login_form)

@teachers_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logged out")
    return redirect(url_for('home'))

@teachers_blueprint.route("/")
@login_required
def index():
    seminars = Seminar.query.filter_by(user_id=current_user.id).all()
    for seminar in seminars:
        seminar.nr_joined_students = Student.query.filter_by(seminar_id=seminar.id, joined=True).count()
    return render_template("index_teachers.html", seminars=seminars)

@teachers_blueprint.route('/create', methods=["GET", "POST"])
@login_required
def create():
    new_form = NewSeminarForm()
    if request.method == "POST":
        if new_form.validate_on_submit():
            new_seminar = Seminar(new_form.name.data, new_form.nr_students.data, current_user.id)
            db.session.add(new_seminar)
            db.session.commit()
            return redirect(url_for("teachers.index"))
        else:
            flash("Form not filled in correctly")
        
    return render_template("new_seminar.html", form=new_form)

@teachers_blueprint.route('/activate/<int:id>')
@login_required
def activate(id:int):
    seminar = Seminar.query.filter_by(id=id, user_id=current_user.id).first()
    if seminar is None:
        flash("Unknown or invalid seminar")
        return redirect(url_for("teachers.index"))
    if seminar.active == False:
        seminar.active = True
        db.session.commit()
        flash(f"Seminar is now open. Use code <b>{seminar.code}</b> to share.")
    else:
        seminar.active = False
        db.session.commit()
        flash("Seminar closed")
    return redirect(url_for("teachers.index"))

@teachers_blueprint.route("/enroll/<int:id>", methods=["POST", "GET"])
@login_required
def enroll(id:int):
    seminar = Seminar.query.filter_by(id=id, user_id=current_user.id).first()
    if seminar is None:
        flash("Unknown or invalid seminar")
        return redirect(url_for("teachers.index"))
    students = Student.query.filter_by(seminar_id=id).all()
    form = EnrollForm()
    if request.method == "POST":
        if form.validate_on_submit():
            for i in range(seminar.nr_students):
                name = request.form.get(f"name{i}")
                if name is not None and len(name) > 0 and Student.query.filter_by(name=name, seminar_id=id).first() is None: # only add new students
                    new_student = Student(name, seminar.id)
                    db.session.add(new_student)
            db.session.commit()
            flash("Students enrolled in seminar")
            return redirect(url_for("teachers.index"))
        else:
            flash("Form not filled in correctly")

    return render_template("enroll_teachers.html", form=form, seminar=seminar, students=students)

@teachers_blueprint.route("/delete/<int:id>")
@login_required
def delete(id:int):
    seminar = Seminar.query.filter_by(id=id, user_id=current_user.id).first()
    if seminar is None:
        flash("Unknown or invalid seminar")
        return redirect(url_for("teachers.index"))
    db.session.delete(seminar)
    db.session.commit()
    flash("Seminar deleted")
    return redirect(url_for("teachers.index"))

@teachers_blueprint.route("/edit/<int:id>")
@login_required
def edit(id:int):
    seminar = Seminar.query.filter_by(id=id, user_id=current_user.id).first()
    if seminar is None:
        flash("Unknown or invalid seminar")
        return redirect(url_for("teachers.index"))
    gf_slide_present = Slide.query.filter_by(seminar_id=id, type=2).count() > 0
    return render_template("seminar.html", seminar=seminar, gf_slide_present=gf_slide_present)

@teachers_blueprint.route('/slide-preview/<int:id>')
@login_required
def slide_preview(id):
    slide = Slide.query.filter_by(id=id).first()
    if slide is None:
        return "Cannot find slide", 404
    return render_template("slide_preview.html", slide=slide, nr_slides=len(slide.seminar.slides))

@teachers_blueprint.route("/add_slide/<int:id>/<int:type>", methods=["POST", "GET"])
@login_required
def add_slide(id:int, type:int):
    NR_ANSWERS = 3
    seminar = Seminar.query.filter_by(id=id, user_id=current_user.id).first()
    if seminar is None:
        flash("Unknown or invalid seminar")
        return redirect(url_for("teachers.index"))
    form = NewSlideForm()
    if request.method == "POST":
        if form.validate_on_submit():
            new_slide = Slide(type, form.title.data, len(seminar.slides) + 1, id, form.text.data)
            db.session.add(new_slide)
            db.session.commit()
            if type == 0:
                # Process question slide specifics
                for i in range(1, NR_ANSWERS+1):
                    new_answer = Answer(request.form.get(f"answer{i}"), request.form.get("answer_correct") == str(i), new_slide.id)
                    db.session.add(new_answer)
                db.session.commit()
            elif type == 2:
                # Process group forming slide specifics
                new_slide.gf_type = request.form.get("gf_type")
                new_slide.gf_nr_per_group = request.form.get("gf_nr_per_group")
                db.session.commit()
            flash(f"Slide added")
            return redirect(url_for("teachers.edit", id=id, type=type))
        else:
            flash("Form not filled in correctly")

    return render_template("add_slide.html", form=form, type=type, seminar=seminar, nr_answers=NR_ANSWERS)

@teachers_blueprint.route('/seminar/<int:seminar_id>/slide/<int:id>/delete')
@login_required
def delete_slide(seminar_id, id):
    slide = Slide.query.filter_by(id=id).first()
    db.session.delete(slide)
    db.session.commit()
    flash("Slide deleted")
    return redirect(url_for("teachers.edit", id=seminar_id))

@teachers_blueprint.route('/seminar/<int:seminar_id>/slide/<int:id>/up')
@login_required
def move_slide_up(seminar_id, id):
    slide = Slide.query.filter_by(id=id).first()
    if slide.slide_order > 1:
        prev_slide = Slide.query.filter_by(seminar_id=seminar_id, slide_order=slide.slide_order-1).first()
        prev_slide.slide_order += 1
        slide.slide_order -= 1
        db.session.commit()
    return redirect(url_for("teachers.edit", id=seminar_id))

@teachers_blueprint.route('/seminar/<int:seminar_id>/slide/<int:id>/down')
@login_required
def move_slide_down(seminar_id, id):
    slide = Slide.query.filter_by(id=id).first()
    nr_slides = Slide.query.filter_by(seminar_id=seminar_id).count()
    if slide.slide_order < nr_slides:
        next_slide = Slide.query.filter_by(seminar_id=seminar_id, slide_order=slide.slide_order+1).first()
        next_slide.slide_order -= 1
        slide.slide_order += 1
        db.session.commit()
    return redirect(url_for("teachers.edit", id=seminar_id))

@teachers_blueprint.route("/dashboard/<int:id>")
@login_required
def dashboard(id:int):
    seminar = Seminar.query.filter_by(id=id, user_id=current_user.id).first()
    if seminar is None:
        flash("Unknown or invalid seminar")
        return redirect(url_for("teachers.index"))
    return render_template("dashboard.html", seminar=seminar)

@teachers_blueprint.route("/dashboard/demo")
@login_required
def demo():
    from interact.lib.demo import populate_for_demo
    populate_for_demo(current_user.id)
    flash("Demo seminar set up")
    return redirect(url_for("teachers.index"))