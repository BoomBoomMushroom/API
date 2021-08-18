import flask
from flask import request
import json
import GameshubApi

app = flask.Flask(__name__)


@app.route("/")
def home():
    return f"Hello {request.method} user!"
@app.route("/gcPublishLvl")
def gcPublishLvl():
    try:
        jsonSent = request.json
        htmlData = jsonSent["HTML"]
        gameInfoData = jsonSent["GameInfo"]
    except:
        jsonSent = {}
    GameshubApi.gameCreatorPublishLevel(htmlData,gameInfoData)
@app.route("/gcGetLvls")
def gcGetLvls():
    return json.dumps(GameshubApi.getGameCreatorLevels())
@app.route("/checkUsername")
def checkUsername():
    try:
        user_query = str(request.args.get('username')) # /logout/?username=USERNAME
    except:
        flask.abort(400)
    if user_query:
        if len(user_query) >= 3 and len(user_query) <= 16:
            return GameshubApi.checkUsername(user_query)
        else:
            return "False"
@app.route("/signup")
def signup():
    try:
        user_query = str(request.args.get('username')) # /logout/?username=USERNAME
        pass_query = str(request.args.get('password')) # /logout/?username=PASSWORD
    except:
        flask.abort(400)
    if user_query and pass_query:
        GameshubApi.signup(user_query,pass_query)
        return "success", 200
@app.route("/delacc",)
def delacc():
    try:
        token_query = str(request.args.get('token')) # /logout/?token=TOKEN
    except:
        flask.abort(400)
    if token_query:
        GameshubApi.deleteAccount(token_query)
        return "success", 200
@app.route("/login")
def login():
    try:
        user_query = str(request.args.get('username')) # /logout/?username=USERNAME
        pass_query = str(request.args.get('password')) # /logout/?username=PASSWORD
        print(str(request.args.get("password")))
    except:
        flask.abort(400)
    if user_query and pass_query:
        loginResponse = GameshubApi.login(user_query,pass_query)
        return loginResponse
@app.route("/logout")
def logout():
    try:
        token_query = str(request.args.get('token')) # /logout/?token=TOKEN
    except:
        flask.abort(400)
    if token_query:
        GameshubApi.logout(token_query)
        return "success", 200
