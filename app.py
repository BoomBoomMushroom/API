import flask
from flask import request

app = flask.Flask(__name__)


@app.route("/")
def home():
    arg = request.args['arg1']
    return f"Hello {request.method} user!"
