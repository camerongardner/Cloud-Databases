# models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login

# The classes are used to create the necessary tables and columns
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), default='user', nullable=False)  # 'admin' or 'user'
    enrollments = db.relationship('Enrollment', backref='student', lazy='dynamic')

    # The following functions are used to hash user passwords, compare password
    # hashes and set user configurations.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
   
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
   
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username}>'

class Degree(db.Model):
    __tablename__ = 'degrees'

    id = db.Column(db.Integer, primary_key=True)
    degree_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    enrollments = db.relationship('Enrollment', backref='degree', lazy='dynamic')

    def __repr__(self):
        return f'<Degree {self.degree_name}>'

class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    degree_id = db.Column(db.Integer, db.ForeignKey('degrees.id'), nullable=False)
    enrolled_on = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    def __repr__(self):
        return f'<Enrollment User:{self.user_id} Degree:{self.degree_id}>'

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
