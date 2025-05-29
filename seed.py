from interact import db, app
from interact.models import User
from werkzeug.security import generate_password_hash

new_user = User("admin", generate_password_hash(app.config["DEFAULT_ADMIN_PASS"]), "admin")

with app.app_context():
    # Remove all existing
    User.query.delete()
    db.session.commit()
    # Then add new
    db.session.add(new_user)
    db.session.commit()