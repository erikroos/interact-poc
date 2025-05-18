from interact import db, app
from interact.teachers.models import User
from werkzeug.security import generate_password_hash

new_user = User(username="admin", password=generate_password_hash(app.config["DEFAULT_ADMIN_PASS"]))

with app.app_context():
    # Remove all existing
    User.query.delete()
    db.session.commit()
    # Then add new
    db.session.add(new_user)
    db.session.commit()