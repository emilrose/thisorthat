import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename

import quiz

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] == "txt"


@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        file = file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "success"
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
