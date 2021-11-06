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
@app.route("/tokeninfo")
def tokeninfo():
    try:
        token_q = str(request.args.get("token"))
    except:
        flask.abort(400)
    return GameshubApi.tokeninfo(token_q)
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
@app.route("/getaccount")
def viewacc():
    try:
        query = str(request.args.get('username')) # /logout/?token=TOKEN
    except:
        flask.abort(400)
    if query:
        return GameshubApi.getAccountView(query)
@app.route("/accsearch")
def accsearch():
    try:
        query = str(request.args.get('q')) # /logout/?token=TOKEN
    except:
        flask.abort(400)
    if query:
        data = json.loads(GameshubApi.accountSearch(query))
        out = ""
        for i in range(len(data)):
            ele = data[i]
            inp = "<a href='https://gameshub.netlify.app/gamehubapi/viewacc?q="+ele["Username"]+"'>"+ele['Username']+"</a><br>"
            out += inp
        return out
@app.route("/setpet")
def setpet():
    try:
        token_query = str(request.args.get('token')) # /logout/?token=TOKEN
        name_query = str(request.args.get('name')) # /logout/?token=TOKEN
        values_query = str(request.args.get('action'))
    except:
        flask.abort(400)
    if token_query and name_query and values_query:
        return "success", 200 #GameshubApi.setPet(token_query,name_query,values_query)
@app.route("/awardAdvancement")
def awardAdvancement():
    try:
        token_query = str(request.args.get('token')) # /logout/?token=TOKEN
        advance_id_query = str(request.args.get('id')) # /logout/?token=TOKEN
    except:
        flask.abort(400)
    if token_query and advance_id_query:
        GameshubApi.awardAdvancement(token_query,advance_id_query)
        return "success", 200
@app.route("/awardmoney")
def awardmoney():
    try:
        token_query = str(request.args.get('token')) # /logout/?token=TOKEN
        amount = int(request.args.get('amount')) # /logout/?token=TOKEN
    except:
        flask.abort(400)
    if token_query and amount:
        GameshubApi.awardMoney(token_query,amount)
        return "success", 200