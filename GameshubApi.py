import base64
import json
import os
import requests
import random
import hashlib
from github import Github
from pprint import pprint

token = "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"
gcLvlsfileName = "gameCreatorLevels.json"
repoName = "BoomBoomMushroom/GameHub"
apiRepoName = "BoomBoomMushroom/API"

g = Github(token)
user = g.get_user()
for currentRepo in user.get_repos():
    if currentRepo.full_name == repoName:
        repo = currentRepo
    if currentRepo.full_name == apiRepoName:
        apiRepo = currentRepo
def getJsonFileContents(FilePath,branch):
    return json.loads(apiRepo.get_contents(FilePath,branch).decoded_content)
def publishLevel(data):
    repoBranch = repo.get_branch("api")
    file = repo.get_contents(gcLvlsfileName,"api")

    if data != None:
        repo.update_file(path=file.path,message="",content=json.dumps(data),sha=file.sha)
    else:
        repo.update_file(path=file.path,message="",content=json.dumps([]),sha=file.sha)
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
def sha256HashString(string: str):
    encodedString = string.encode()
    return hashlib.sha256(string.encode()).hexdigest()
def checkUsername(username):
    if not len(username) >= 3 and not len(username) <= 16:
        return False

    try:
        accounts = getJsonFileContents("GameshubApi/accounts.json","main")
        ava = True
        for account in accounts:
            if account['Username'] == username:
                ava = False
        return ava
    except:
        accounts = []
        return True
def signup(username,password):
    if len(username) >= 3 and len(username) <= 16 and len(password) >= 8:
        try:
            accounts = getJsonFileContents("GameshubApi/accounts.json","main")
        except:
            accounts = []
        usernameAvailable = True
        for account in accounts:
            if account["Username"]:
                if account["Username"] == username:
                    usernameAvailable = False
                    break;
        if usernameAvailable == True:
            newAccountJson = {
                "Username": username,
                "Password": sha256HashString(sha256HashString(password)),
                "UUID": generateUUID(32),
                "IsBanned": False,
                "IsMuted": False,
                "Friends": [],
                "FriendRequests": [],
                "GameshubData": [],
                "Misc": [],
            }
            accounts.append(newAccountJson)
            fileHolder = apiRepo.get_contents("GameshubApi/accounts.json","main")
            apiRepo.update_file(path=fileHolder.path,message="",content=json.dumps(accounts),sha=fileHolder.sha)
            return(f"Account {username} has been created")
        else:
            return "Username is already taken!"
    else:
        return(f"Account {username} couldn't be created because the Username or Password is a lil weird!")
def login(username,password):
    try:
        accounts = getJsonFileContents("GameshubApi/accounts.json","main")
        accountTokens = getJsonFileContents("GameshubApi/accountTokens.json","main")
    except:
        accounts = []
        accountTokens = []
    for account in accounts:
        try:
            accUsername = account["Username"]
            accPassword = account["Password"]
        except:
            accUsername = "INVALID_USER_NAME"
            accPassword = "INVALID_ACC_PASSWORD"
        if accUsername == username and accPassword == sha256HashString(sha256HashString(password)):
            varX = 0
            while varX < len(accountTokens):
                accToken = accountTokens[varX]
                if accToken["Account"]["Username"] == username and accToken["Account"]["Password"] == sha256HashString(sha256HashString(password)):
                    try:
                        fileContents2 = getJsonFileContents("GameshubApi/accountTokens.json","main")
                    except:
                        fileContents2 = []
                    if fileContents2 != []:
                        fileContents2.pop(varX)
                        filePath2 = apiRepo.get_contents("GameshubApi/accountTokens.json","main")
                        apiRepo.update_file(filePath2.path,"",json.dumps(fileContents2),filePath2.sha)
                        break;

            generatedToken = generateToken(16)
            try:
                fileContents = getJsonFileContents("GameshubApi/accountTokens.json","main")
            except:
                fileContents = []
            appendData = {
                "Token": generatedToken,
                "Account": account,
            }
            fileContents.append(appendData)
            filePath = apiRepo.get_contents("GameshubApi/accountTokens.json","main")
            apiRepo.update_file(path=filePath.path,message="",content=json.dumps(fileContents),sha=filePath.sha,branch="main")
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
    try:
        accountTokens = getJsonFileContents("GameshubApi/accountTokens.json","main")
    except:
        accountTokens = []
    i = 0
    while i < len(accountTokens):
        CurrentToken = accountTokens[i]
        if CurrentToken["Token"]:
            if CurrentToken["Token"] == token:
                accountTokens.pop(i)
                filePath = apiRepo.get_contents("GameshubApi/accountTokens.json","main")
                apiRepo.update_file(path=filePath.path,message="",content=json.dumps(accountTokens),sha=filePath.sha)
                return(f"Logged out!")
        i+=1
def awardAdvancement(token,advancementId):
    try:
        accounts = getJsonFileContents("GameshubApi/accounts.json","main")
        accountTokens = getJsonFileContents("GameshubApi/accountTokens.json","main")
        advancementsJson = getJsonFileContents("GameshubApi/advancements.json","main")
    except:
        accounts = []
        accountTokens = []
    
    tokenStatusResp = checkToken(token)
    if tokenStatusResp["TokenStatus"] == True:
        i = 0
        while i < len(accounts)+1:
            try:
                currentAccount = accounts[i]
                if currentAccount == tokenStatusResp["Account"]:
                    for advancement in advancements:
                        if advancement["id"] == advancementId:
                            currentAccount["GameshubData"].update({"Advancements":[]})
                            currentAccount["GameshubData"]["Advancements"].append(advancement)
                            print(currentAccount,accounts)
                            filePath = apiRepo.get_contents("GameshubApi/accounts.json","main")
                            apiRepo.update_file(path=filePath.path,message="",content=json.dumps(accounts),sha=filePath.sha)

                            return f'ADVANCEMENT_ADDED_TO_{currentAccount["Username"]}'
                            break
            except:
                i = len(accounts)+2
                return "ACCOUNT_WASNT_FOUND"
            i += 1
    else:
        return "INVALID_ACCOUNT_TOKEN"
    return "DONE"
def checkToken(token):
    try:
        allTokens = getJsonFileContents("GameshubApi/accountTokens.json","main")
    except:
        allTokens = []
    if allTokens == []:
        return {"TokenStatus":False,"Account":None}
    else:
        for currentToken in allTokens:
            if currentToken["Token"]:
                if currentToken["Token"] == token:
                    return {"TokenStatus":True,"Account":currentToken["Account"]}
        return {"TokenStatus":False,"Account":None}
def deleteAccount(token):
    
    try:
        accountTokens = getJsonFileContents("GameshubApi/accountTokens.json","main")
        accounts = getJsonFileContents("GameshubApi/accounts.json","main")
    except:
        accountTokens = []
        accounts = []
    i = 0
    while i < len(accountTokens):
        CurrentToken = accountTokens[i]
        if CurrentToken["Token"]:
            if CurrentToken["Token"] == token:
                accountIndex = accounts.index(CurrentToken["Account"])
                if accountIndex != None:
                    accounts.pop(accountIndex)
                    filePath = apiRepo.get_contents("GameshubApi/accounts.json","main")
                    apiRepo.update_file(path=filePath.path,message="",content=json.dumps(accounts),sha=filePath.sha)
                
                accountTokens.pop(i)
                filePath = apiRepo.get_contents("GameshubApi/accountTokens.json","main")
                apiRepo.update_file(path=filePath.path,message="",content=json.dumps(accountTokens),sha=filePath.sha)
                return(f"Account Deleted!")
        i+=1
def generateUUID(length):
    uuidCharset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVQRSTUV0123456789"
    uuid = ""
    def tokenGen():
        uuid2 = ""
        while len(uuid2) < length:
            uuid2 += uuidCharset[random.randint(0,len(uuidCharset)-1)]
        if checkToken(uuid2)["TokenStatus"] == False:
            return uuid2
        else:
            return tokenGen()
    uuid = tokenGen()
    return uuid
def generateToken(tokenLength):
    tokenCharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVQRSTUV0123456789"
    token = ""
    def tokenGen():
        token2 = ""
        while len(token2) < tokenLength:
            token2 += tokenCharacters[random.randint(0,len(tokenCharacters)-1)]
        tokenRes = checkToken(token2)
        if tokenRes["TokenStatus"] == False:
            return token2
        else:
            return tokenGen()
    token = tokenGen()
    return token
