from os import abort
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
        requestJson = json.loads(request.json)
    except:
        flask.abort(400)
    if requestJson:
        if len(requestJson["Username"]) >= 3 and len(requestJson["Username"]) <= 16:
            return GameshubApi.checkUsername(requestJson["Username"])
        else:
            return False
@app.route("/signup", methods=["POST"])
def signup():
    try:
        requestJson = json.loads(request.json)
    except:
        flask.abort(400)
    if requestJson:
        GameshubApi.signup(requestJson["Username"],requestJson["Password"])
        return "success", 200
@app.route("/delacc", methods=["POST"])
def delacc():
    try:
        requestJson = json.loads(request.json)
    except:
        flask.abort(400)
    if requestJson:
        GameshubApi.deleteAccount(requestJson["Token"])
        return "success", 200
@app.route("/login", methods=["GET"])
def login():
    try:
        requestJson = json.loads(request.json)
    except:
        flask.abort(400)
    if requestJson:
        return GameshubApi.login(requestJson["Username"],requestJson["Password"])
@app.route("/logout", methods=["POST"])
def logout():
    try:
        requestJson = json.loads(request.json)
    except:
        flask.abort(400)
    if requestJson:
        GameshubApi.logout(requestJson["Token"])
        return "success", 200
