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
        requestJson = request.json
        if requestJson["Username"]:
            return GameshubApi.checkUsername(requestJson["Username"])
    except:
        abort(400)
@app.route("/signup", methods=["POST"])
def checkUsername():
    try:
        requestJson = request.json
        if requestJson["Username"] and requestJson["Password"]:
            return GameshubApi.signup(requestJson["Username"],requestJson["Password"])
    except:
        abort(400)
@app.route("/delacc",method=["POST"])
def delacc():
    try:
        requestJson = request.json
        if requestJson["Token"]:
            return GameshubApi.deleteAccount(requestJson["Token"])
    except:
        abort(400)
@app.route("/login",method=["GET"])
def login():
    try:
        requestJson = request.json
        if requestJson["Username"] and requestJson["Password"]:
            return GameshubApi.login(requestJson["Username"],requestJson["Password"])
    except:
        abort(400)
@app.route("/logout",method=["GET"])
def logout():
    try:
        requestJson = request.json
        if requestJson["Token"]:
            return GameshubApi.logout(requestJson["Token"])
    except:
        abort(400)
