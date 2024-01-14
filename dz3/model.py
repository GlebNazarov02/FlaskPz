from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    surname = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128),nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password) 

    def check_password(self, password):
        return check_password_hash(self.password, password)