import base64
import json
import os
from flask import Flask, Response, abort, request
from github import Github
from pprint import pprint

token = "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"
fileName = "gameCreatorLevels.json"
repoName = "BoomBoomMushroom/GameHub"

app = Flask(__name__)

g = Github(token)
user = g.get_user()
for currentRepo in user.get_repos():
    if currentRepo.full_name == repoName:
        repo = currentRepo

def publishLevel(data):
    repoBranch = repo.get_branch("api")
    file = repo.get_contents(fileName,"api")

    if data != None:
        repo.update_file(path=file.path,message="",content=json.dumps(data),sha=file.sha,branch="api")
    else:
        repo.update_file(path=file.path,message="",content=json.dumps([]),sha=file.sha,branch="api")

def gameCreatorPublishLevel(html,gameInfo):
    repoBranch = repo.get_branch("api")
    if gameInfo["Name"]:
        gameName = gameInfo["Name"]
        infoFile = repo.create_file("CreatorGames/"+gameName+"/info.json","",json.dumps(gameInfo),"api")
        htmlFile = repo.create_file("CreatorGames/"+gameName+"/index.html","",html,"api")

@app.route('/gcPublishLvl')
def gcPublishLvl():
    print(request.method)
    return(request.method + ", request"), 200

app.run()
