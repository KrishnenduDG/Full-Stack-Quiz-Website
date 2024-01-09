from . import db
from flask_login import UserMixin



class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    profile_pic = db.Column(db.String(100))
    def toMap(self):
        return {
            "email":self.email,
            "name":self.first_name,
            "profile_pic": self.profile_pic
        }   

class Quiz(db.Model):
    __tablename__ = "quiz"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete="CASCADE"),nullable=False)
    question_count = db.Column(db.Integer)
    time = db.Column(db.Integer)
    correct = db.Column(db.Integer)
    incorrect = db.Column(db.Integer)
    

    def toMap(self):
        return {
            "question_count":self.question_count,
            "time":self.time,
            "correct" : self.correct,
            "incorrect" : self.incorrect
        }   