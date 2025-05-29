from flask import Blueprint, render_template, current_app, flash, redirect, url_for
from flask_login import current_user
from interact.models import User
from functools import wraps

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        if current_user.role != 'admin':
            flash("You are not authorized to view this page")
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated_function

@admin_blueprint.route("/")
@admin_required
def index():
    users = User.query.filter(User.role != "admin").all()
    return render_template("index_admin.html", users=users)