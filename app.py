import os
import json
from flask import Flask, request, redirect, url_for, render_template, jsonify, Blueprint
from werkzeug import secure_filename
import pickle
from quiz import create_quiz
import uuid

UPLOAD_FOLDER = 'uploads'
QUIZZES_FOLDER = 'quizzes'

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] == "txt"

@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        this = request.files['this'].read()
        that = request.files['that'].read()
        hash = uuid.uuid4().hex
        quiz = create_quiz(this, that)
        with open(os.path.join(QUIZZES_FOLDER, hash + '.p'), 'wb') as file:
            pickle.dump(quiz, file)
        return redirect(url_for('display_quiz', quiz_id=hash))
    else:
        return render_template("index.html")


@app.route('/quiz_questions/<quiz_id>', methods=['GET'])
def get_quiz_questions(quiz_id):
    with open(os.path.join(QUIZZES_FOLDER,  quiz_id + '.p'), 'rb') as f:
        quiz = pickle.load(f)
    return jsonify({'quiz': quiz})

@app.route('/quiz/<quiz_id>', methods=['GET', 'POST'])
def display_quiz(quiz_id):
    return render_template("quiz.html")


if __name__ == "__main__":
    app.run()
