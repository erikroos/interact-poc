from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import json
import os

### App configuration

app = Flask(__name__)

config_path = os.path.join(os.path.dirname(__file__), "config.json")
try:
    app.config.from_file(config_path, load=json.load)
except Exception as e:
    print(f"Error loading config file ({config_path}) from {__file__}: {e}")

### ORM

db = SQLAlchemy()
db.init_app(app)

migrate = Migrate(app, db)

from sqlalchemy import event

with app.app_context():
    @event.listens_for(db.engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

### Login manager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'teachers.login'

from interact.teachers.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register Blueprints

from interact.students.views import students_blueprint
app.register_blueprint(students_blueprint, url_prefix="/students")

from interact.teachers.views import teachers_blueprint
app.register_blueprint(teachers_blueprint, url_prefix="/teachers")

from interact.admin.views import admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix="/admin")