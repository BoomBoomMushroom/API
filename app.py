import os
#os.system('pip install PyGithub')

import flask
from flask import request
import json
import GameshubApi
import random

app = flask.Flask(__name__)

def responseMake(r):
  resp = flask.Response(json.dumps(r))
  resp.headers['Access-Control-Allow-Origin'] = "*"
  return resp

@app.route("/")
def home():
    return responseMake("Hello "+request.method+" user!")
@app.route("/checkUsername")
def checkUsername():
    try:
        user_query = str(request.args.get('username')) # /logout/?username=USERNAME
    except:
        flask.abort(400)
    if user_query:
        if len(user_query) >= 3 and len(user_query) <= 16:
            return responseMake(GameshubApi.checkUsername(user_query))
        else:
            return responseMake("False")
@app.route("/tokeninfo")
def tokeninfo():
    try:
        token_q = str(request.args.get("token"))
    except:
        flask.abort(400)
    return responseMake(GameshubApi.tokeninfo(token_q))
@app.route("/signup")
def signup():
    try:
        user_query = str(request.args.get('username')) # /logout/?username=USERNAME
        pass_query = str(request.args.get('password')) # /logout/?username=PASSWORD
    except:
        flask.abort(400)
    if user_query and pass_query:
        GameshubApi.signup(user_query,pass_query)
        return responseMake("success"), 200
@app.route("/delacc",)
def delacc():
    try:
        token_query = str(request.args.get('token')) # /logout/?token=TOKEN
    except:
        flask.abort(400)
    if token_query:
        GameshubApi.deleteAccount(token_query)
        return responseMake("success"), 200
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
        return responseMake(loginResponse)
@app.route("/logout")
def logout():
    try:
        token_query = str(request.args.get('token')) # /logout/?token=TOKEN
    except:
        flask.abort(400)
    if token_query:
        GameshubApi.logout(token_query)
        return responseMake("success"), 200
@app.route("/getaccount")
def viewacc():
    try:
        query = str(request.args.get('username'))
    except:
        flask.abort(400)
    if query:
        return responseMake(GameshubApi.getAccountView(query))
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
            inp = "<a href='https://gameshub.dev/gamehubapi/viewacc?q="+ele["Username"]+"'>"+ele['Username']+"</a><br>"
            out += inp
        return responseMake(out)
@app.route("/badgeupdate")
def badgeupdate():
    try:
        token_query = str(request.args.get('username')) # /logout/?token=TOKEN
        name_query = str(request.args.get('name')) # /logout/?token=TOKEN
        values_query = str(request.args.get('action'))
    except:
        flask.abort(400)
    if token_query and name_query and values_query:
       return responseMake("Success"), 200 # GameshubApi.badgeEdit(token_query,name_query,values_query)
@app.route("/setpet")
def setpet():
    try:
        token_query = str(request.args.get('token')) # /logout/?token=TOKEN
        name_query = str(request.args.get('name')) # /logout/?token=TOKEN
        values_query = str(request.args.get('action'))
    except:
        flask.abort(400)
    if token_query and name_query and values_query:
        #deta = GameshubApi.setPet(token_query,name_query,values_query)
        return responseMake("success"), 200
@app.route("/awardAdvancement")
def awardAdvancement():
    try:
        token_query = str(request.args.get('token')) # /logout/?token=TOKEN
        advance_id_query = str(request.args.get('id')) # /logout/?token=TOKEN
    except:
        flask.abort(400)
    if token_query and advance_id_query:
        GameshubApi.awardAdvancement(token_query,advance_id_query)
        return responseMake("success"), 200
@app.route("/awardmoney")
def awardmoney():
    try:
        token_query = str(request.args.get('token')) # /logout/?token=TOKEN
        amount = int(request.args.get('amount')) # /logout/?token=TOKEN
    except:
        flask.abort(400)
    if token_query and amount:
        d = GameshubApi.awardMoney(token_query,amount)
        return responseMake(d), 200
@app.route("/getshop")
def getShop():
  d = GameshubApi.getShop()
  return responseMake(d), 200
@app.route("/buy")
def buyItem():
  try:
    id = str(request.args.get('id'))
    token = str(request.args.get('token'))
  except:
    return responseMake("Failed to get params!"), 400
  d = GameshubApi.buyItem(id,token)
  return responseMake(d), 200
@app.route("/getcustomgames")
def getCustomGames():
  d = GameshubApi.getCustomGames()
  return responseMake(d), 200
@app.route("/publishcustomgame")
def publishCustomGame():
  try:
    world = str(request.args.get('world'))
    token = str(request.args.get('token'))
  except:
    flask.abort(400)
  d = GameshubApi.publishCustomGame(world,token)
  return responseMake(d), 200
app.run(host="0.0.0.0",port=7777)