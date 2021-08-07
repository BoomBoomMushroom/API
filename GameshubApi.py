import base64
import json
import os
import requests
import random
#import hashlib
from github import Github
from pprint import pprint

token = "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"
gcLvlsfileName = "gameCreatorLevels.json"
repoName = "BoomBoomMushroom/GameHub"

g = Github(token)
user = g.get_user()
for currentRepo in user.get_repos():
    if currentRepo.full_name == repoName:
        repo = currentRepo

def publishLevel(data):
    repoBranch = repo.get_branch("api")
    file = repo.get_contents(gcLvlsfileName,"api")

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
def getGameCreatorLevels():
    try:
        levels = json.loads(requests.get("https://raw.githubusercontent.com/BoomBoomMushroom/GameHub/api/gameCreatorLevels.json"))
    except:
        levels = []
    return levels
def checkUsername(username):
    accountUrl = "https://raw.githubusercontent.com/BoomBoomMushroom/GameHub/api/accounts.json"
    try:
        accounts = json.loads(requests.get(accountUrl))
    except:
        accounts = []
    if accounts == []:
        return True
    else:
        for account in accounts:
            if account["Username"]:
                if account["Username"] == username:
                    return False
        return True
def signup(username,password):
    if len(username) >= 3 and len(username) <= 16 and len(password) >= 6:
        accountUrl = "https://raw.githubusercontent.com/BoomBoomMushroom/GameHub/api/accounts.json"
        try:
            accounts = json.loads(requests.get(accountUrl))
        except:
            accounts = []
        usernameAvailable = True
        for account in accounts:
            if account["Username"]:
                if account["Password"]:
                    if checkUsername(account["Username"]) == False:
                        usernameAvailable = False
                        break;
        if usernameAvailable == True:
            newAccountJson = {
                "Username": username,
                "Password": password, #hashlib.sha256(hashlib.sha256(password))
            }
            accounts.append(newAccountJson)
            fileHolder = repo.get_contents("accounts.json","api")
            repo.update_file(path=fileHolder.path,message="",content=json.dumps(accounts),sha=fileHolder.sha,branch="api")
            return(f"Account {username} has been created")
def login(username,password):
    accountUrl = "https://raw.githubusercontent.com/BoomBoomMushroom/GameHub/api/accounts.json"
    try:
        accounts = json.loads(requests.get(accountUrl))
    except:
        accounts = []
    sha256hashedPasswordx2 = password #hashlib.sha256(hashlib.sha256(password))
    for account in accounts:
        if account["Username"]:
            if account["Username"] == username:
                if account["Passoword"]:
                    if account["Password"] == sha256hashedPasswordx2:
                        print("Password Matches")
                        generatedToken = generateToken(16)
                        try:
                            fileContents = json.loads(requests.get("https://raw.githubusercontent.com/BoomBoomMushroom/GameHub/api/accountTokens.json"))
                        except:
                            fileContents = []
                        appendData = {
                            "Token": generatedToken,
                            "Account": account,
                        }
                        fileContents.append(appendData)
                        filePath = repo.get_contents("accountTokens.json","api")
                        repo.update_file(path=filePath.path,message="",content=fileContents,sha=filePath.sha,branch="api")
                        return generatedToken
    return "INVALID_ACCOUNT_TOKEN"
def tokenLogin(token):
    tokenResponse = checkToken(token)
    if tokenResponse["TokenStatus"] == True:
        account = tokenResponse["Account"]
        return account
    else:
        return {}
def logout(token):
    tokensUrl = "https://raw.githubusercontent.com/BoomBoomMushroom/GameHub/api/accountTokens.json"
    try:
        allTokens = json.dumps(requests.get(tokensUrl))
    except:
        allTokens = []
    i = 0
    while i < len(allTokens):
        CurrentToken = allTokens[i]
        if CurrentToken["Token"]:
            if CurrentToken["Token"] == token:
                allTokens.pop(i)
                filePath = repo.get_contents("accountTokens.json","api")
                repo.update_file(path=filePath.path,message="",content=allTokens,sha=filePath.sha,branch="api")
                return(f"Logged out!")
def checkToken(token):
    tokensUrl = "https://raw.githubusercontent.com/BoomBoomMushroom/GameHub/api/accountTokens.json"
    try:
        allTokens = json.dumps(requests.get(tokensUrl))
    except:
        allTokens = []
    if allTokens == []:
        return {"TokenStatus":False,"Account":None}
    else:
        for currentToken in allTokens:
            if currentToken["Token"]:
                if currentToken["Token"] == token:
                    return {"TokenStatus":True,"Account":currentToken["Account"]}
def deleteAccount(token):
    tokenResponse = checkToken(token)
    if tokenResponse["TokenStatus"]:
        if tokenResponse["TokenStatus"] == True:
            if tokenResponse["Account"]:
                account = tokenResponse["Account"]
                accountUrl = "https://raw.githubusercontent.com/BoomBoomMushroom/GameHub/api/accounts.json"
                try:
                    accounts = json.loads(requests.get(accountUrl))
                except:
                    accounts = []
                if account["Username"]:
                    if account["Password"]:
                        i = 0
                        while i < len(accounts):
                            searchingAccount = accounts[i]
                            if searchingAccount["Username"]:
                                if searchingAccount["Username"] == account["Username"]:
                                    if searchingAccount["Password"]:
                                        if searchingAccount["Password"] == account["Password"]:
                                            accounts.pop(i)
                                            filePath = repo.get_contents("accounts.json","api")
                                            repo.update_file(path=filePath.path,message="",content=accounts,sha=filePath.sha, branch="api")
                                            return(f"Deleted")
def generateToken(tokenLength):
    tokenCharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVQRSTUV0123456789"
    token = ""
    def tokenGen():
        token2 = ""
        while len(token2) < tokenLength:
            token2 += tokenCharacters[random.randint(0,len(tokenCharacters))]
        if checkToken(token2)["TokenStatus"] == False:
            return token2
        else:
            return tokenGen()
    token = tokenGen()
    return token
