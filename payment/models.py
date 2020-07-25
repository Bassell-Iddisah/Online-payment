from payment import db, login_manager
from flask_login import UserMixin



@login_manager.user_loader
def load_user(Student_id):
    return Student.query.get(Student_id)


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.username}', '{self.email}', '{self.password}')"
