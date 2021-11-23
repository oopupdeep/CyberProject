from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def test_page():
    return render_template("test.html")