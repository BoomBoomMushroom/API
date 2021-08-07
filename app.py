import flask
from flask import request
from flask import json

import GameshubApi

app = flask.Flask(__name__)


@app.route("/")
def home():
    return f"Hello {request.method} user!"
@app.route("/gcPublishLvl", methods=["POST"])
def gcPublishLvl():
    try:
        jsonSent = request.json
        htmlData = jsonSent["HTML"]
        gameInfoData = jsonSent["GameInfo"]
    except:
        jsonSent = {}
    GameshubApi.gameCreatorPublishLevel(htmlData,gameInfoData)
@app.route("/gcGetLvls", methods=["GET"])
def gcGetLvls():
    return json.dumps(GameshubApi.getGameCreatorLevels())
@app.route("/checkUsername", methods=["GET"])
def checkUsername():
    try:
        requestJson = request.json
        return GameshubApi.checkUsername(requestJson["Username"])
    except:
        flask.abort(400)
@app.route("/signup", methods=["POST"])
def signup():
    try:
        requestJson = request.json
        return GameshubApi.signup(requestJson["Username"],requestJson["Password"])
    except:
        flask.abort(400)
@app.route("/login", method=["GET"])
def login():
    try:
        requestJson = request.json
        return GameshubApi.login(requestJson["Username"],requestJson["Password"])
    except:
        flask.abort(400)
@app.route("/logout", method=["GET"])
def logout():
    try:
        requestJson = request.json
        return GameshubApi.logout(requestJson["Token"])
    except:
        flask.abort(400)
