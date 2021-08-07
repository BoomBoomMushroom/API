import flask
from flask import request

app = flask.Flask(__name__)


@app.route("/")
def home():
    print(f"Hello {request.method} user!")
    return f"Hello {request.method} user!"
