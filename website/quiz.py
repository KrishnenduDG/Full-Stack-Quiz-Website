from flask import Blueprint, render_template,jsonify,request
from flask_login import login_required, current_user
from .models import Quiz,User
from . import db

quiz = Blueprint('quiz', __name__)

# View Route
@quiz.route("/",methods=["GET"])
@login_required
def quiz_route():
    return render_template("quiz.html",user=current_user)


# API + View Route
@quiz.route("/result",methods=["GET","POST"])
@login_required
def get_quiz_result():
    if request.method == "POST":
        request_body = request.json
        print(current_user.get_id())

        new_quiz = Quiz(user_id=current_user.get_id(),question_count=request_body["questionCount"],time=request_body["time"],correct=request_body["correct"],incorrect = request_body["incorrect"])
        db.session.add(new_quiz)
        db.session.commit()

        return jsonify(status="success")

    return render_template("result.html",user=current_user)


# API Route
@quiz.route("/summary",methods=["GET","POST"])
@login_required
def get_quiz_summary():
    quiz_summary = list(map(lambda q: q.toMap(), Quiz.query.filter_by(user_id = current_user.get_id()).all()))
    profile_data = User.query.filter_by(id=current_user.get_id()).first()

    return jsonify(status="Success",profile = profile_data.toMap(),data=quiz_summary)