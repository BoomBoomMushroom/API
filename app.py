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
            usernameStatus = GameshubApi.checkUsername(user_query)
            if usernameStatus == False:
                return "False"
            elif usernameStatus == True:
                return "True"
            else:
                return usernameStatus
        else:
            return "False"
@app.route("/acceptfriendreq")
def acceptfriendreq():
    try:
        token_query = str(request.args.get('token')) # /logout/?username=USERNAME
        uuid_query = str(request.args.get('uuid'))
    except:
        flask.abort(400)
    
    return GameshubApi.acceptFriendReq(token_query,uuid_query)
@app.route("/sendfriendreq")
def sendfriendreq():
    try:
        token_query = str(request.args.get('token')) # /logout/?username=USERNAME
        uuid_query = str(request.args.get('uuid'))
    except:
        flask.abort(400)
    
    return GameshubApi.sendFriendRequest(token_query,uuid_query)
@app.route("/getaccountdata")
def getaccountdata():
    try:
        token_query = str(request.args.get('token')) # /logout/?username=USERNAME
    except:
        flask.abort(400)
    
    return GameshubApi.getAccountData(token_query)
@app.route("/awardadvancement")
def awardadvancement():
    try:
        token_query = str(request.args.get('token')) # /logout/?username=USERNAME
        advancement_id_query = str(request.args.get('advance_id')) # /logout/?username=USERNAME
    except:
        flask.abort(400)
    
    return GameshubApi.awardAdvancement(token_query,int(advancement_id_query))
@app.route("/updateacc")
def updateacc():
    try:
        uuid_query = str(request.args.get('uuid')) # /logout/?username=USERNAME
    except:
        flask.abort(400)
    
    return GameshubApi.updateAcc(uuid_query)
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
        #GameshubApi.deleteAccount(token_query)
        return GameshubApi.deleteAccount(token_query), 200
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
