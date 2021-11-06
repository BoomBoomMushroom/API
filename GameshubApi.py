import base64
import json
import os
import requests
import random
import hashlib
import time
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
def signup(username,password):
    accNameStatus = accountNameUpdater(username)
    if len(username) >= 3 and len(username) <= 16 and len(password) >= 7 and accNameStatus == True:
        print("Acc is good processing")
        try:
            accounts = getJsonFileContents("GameshubApi/accounts.json","main")
        except:
            accounts = []
        print("Gopt all accs")
        newAccountJson = {
            "Username": username,
            "Password": sha256HashString(sha256HashString(password)),
            "UUID": generateUUID(32),
            "IsBanned": False,
            "IsMuted": False,
            "Friends": [],
            "FriendRequests": [],
            "AccountCreationTime": time.time(),
            "GameshubData": {
                "Advancements": [
                    {"id":1,"header":"Welcome!","desc":"You get this achievement when you first sign up to Gameshub!","img":"None"},
                ],
                "Money": 50,
                "Purchases": [],
                "GameData": [],
            },
            "Misc": [],
        }
        print("Made accound Data")
        accounts.append(newAccountJson)
        print("appended Data")
        fileHolder = apiRepo.get_contents("GameshubApi/accounts.json","main")
        apiRepo.update_file(path=fileHolder.path,message="",content=json.dumps(accounts),sha=fileHolder.sha)
        print("updated file")
        return(f"Account {username} has been created")
    else:
        if len(username) >= 3 and len(username) <= 16:
            return(f"Account {username} couldn't be created because the Password is a lil weird!")
        else:
            return(f"Account {username} couldn't be created because the Username is a lil weird!")
        # return(f"Account {username} couldn't be created because the Username or Password is a lil weird!")
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
            for accToken in accountTokens:
                if accToken["Account"]["Username"] == username and accToken["Account"]["Password"] == sha256HashString(sha256HashString(password)):
                    try:
                        fileContents2 = getJsonFileContents("GameshubApi/accountTokens.json","main")
                    except:
                        fileContents2 = []
                    if fileContents2 != []:
                        fileContents2.pop( accountTokens.index(accToken) )
                        filePath2 = apiRepo.get_contents("GameshubApi/accountTokens.json","main")
                        apiRepo.update_file(filePath2.path,"",json.dumps(fileContents2),filePath2.sha)
                        break

            generatedToken = generateToken(16)
            print("Generated new token")
            try:
                fileContents = getJsonFileContents("GameshubApi/accountTokens.json","main")
            except:
                fileContents = []
            appendData = {
                "Token": generatedToken,
                "Account": account,
            }
            print("append Data is made")
            fileContents.append(appendData)
            filePath = apiRepo.get_contents("GameshubApi/accountTokens.json","main")
            apiRepo.update_file(path=filePath.path,message="",content=json.dumps(fileContents),sha=filePath.sha,branch="main")
            print("added append data to acctokens file")
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
def accountNameUpdater(username):
    try:
        accounts = getJsonFileContents("GameshubApi/accounts.json","main")
    except:
        accounts = []
    useableCharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"
    g_chars = all([characters in useableCharacters for characters in username])
    dupe_name = False

    for ele in accounts:
        if ele.Username.lower() == username.lower():
            dupe_name = True
            pass
    if(g_chars==False or dupe_name == True):
        return False
    else:
        return True 
def getAccountData(token):
    try:
        accounts = getJsonFileContents("GameshubApi/accounts.json","main")
        accountTokens = getJsonFileContents("GameshubApi/accountTokens.json","main")
        advancementsJson = getJsonFileContents("GameshubApi/advancements.json","main")
    except:
        return "ERROR_WHILST_GETTING_DATA"
    
    for currentToken in accountTokens:
        if currentToken["Token"] == token:
            tokenIndex = accountTokens.index(currentToken)
            return currentToken["Account"]
    return "COULDNT_FIND_TOKEN"
def setPet(token,name,action):
    try:
        accounts = getJsonFileContents("GameshubApi/accounts.json","main")
        pets = getJsonFileContents("GameshubApi/pets.json","main")
        accountTokens = getJsonFileContents("GameshubApi/accountTokens.json","main")
        advancementsJson = getJsonFileContents("GameshubApi/advancements.json","main")
    except:
        return "ERROR_WHILST_GETTING_DATA"
    account = getAccountData(token)
    if not "pets" in account:
        account.update({"Pets":[]})
    
    if action=="sell":
        hasPet = False
        for pet in account["Pets"]:
            if pet["Pet"]["DisplayName"] == name:
                hasPet = True
        
        if hasPet == False: return "No Pet Found!"
        else:
            for pet in account["Pets"]:
                pet["Pet"]["Count"]
                if pet["Pet"]["DisplayName"] == name and pet["Pet"]["CanSell"] == True and int(pet["Pet"]["Count"]) > int(0):
                    pet["Pet"]["Count"] -= 1
    elif action == "box_open":
        print(account)
        won = random.choice(list(pets.values()))
        hasPet = False
        hasMoney = False

        for pet in account["Pets"]:
            if pet["Pet"]["DisplayName"] == won.DisplayName:
                hasPet = True
                break
        if hasPet==True:
            for pet in account["Pets"]:
                if pet["Pet"]["DisplayName"] == won.DisplayName:
                    pet["Count"] += 1
                    break
        else:
            appender = {
                "Pet": won,
                "Count": 1
            }
            account["Pets"].append(appender)
        print(won)

    for i in range(len(accounts)):
        acc = accounts[i]
        print(acc["UUID"]==account["UUID"])
        if acc["UUID"] == account["UUID"]:
            account[i] = account
            break
    filePath = apiRepo.get_contents("GameshubApi/accounts.json","main")
    apiRepo.update_file(path=filePath.path,message="",content=json.dumps(accounts),sha=filePath.sha)
    updateToken(token)
    return account
def tokeninfo(token):
    try:
        accounts = getJsonFileContents("GameshubApi/accounts.json","main")
        accountTokens = getJsonFileContents("GameshubApi/accountTokens.json","main")
        advancementsJson = getJsonFileContents("GameshubApi/advancements.json","main")
    except:
        return "ERROR_WHILST_GETTING_DATA"
    
    for currentToken in accountTokens:
        if currentToken["Token"] == token:
            tokenIndex = accountTokens.index(currentToken)
            return currentToken["Account"]
    return "COULDNT_FIND_TOKEN"
def getAccountView(inputUsername):
    try:
        accounts = getJsonFileContents("GameshubApi/accounts.json","main")
        advancementsJson = getJsonFileContents("GameshubApi/advancements.json","main")
    except:
        return "ERROR_WHILST_GETTING_DATA"
    for currentAccount in accounts:
        if currentAccount["Username"] == inputUsername:
            viewerAccount = currentAccount
            viewerAccountIndex = accounts.index(viewerAccount)
            break
    try:
        del viewerAccount["Password"]
        return viewerAccount
    except:
        return "INVALID_ACCOUNT_USERNAME"
def accountSearch(prefix):
    try:
        accounts = getJsonFileContents("GameshubApi/accounts.json","main")
        advancementsJson = getJsonFileContents("GameshubApi/advancements.json","main")
    except:
        return "ERROR_WHILST_GETTING_DATA"
    
    accountUsernames = None
    if prefix=="*":
        accountUsernames = [x for x in accounts if x["Username"].lower().startswith("")]
    else:
        accountUsernames = [x for x in accounts if x["Username"].lower().startswith(prefix.lower())]
    return json.dumps(accountUsernames)
def awardMoney(token,amount):
    try:
        accounts = getJsonFileContents("GameshubApi/accounts.json","main")
        accountTokens = getJsonFileContents("GameshubApi/accountTokens.json","main")
        advancementsJson = getJsonFileContents("GameshubApi/advancements.json","main")
    except:
        return "ERROR_WHILST_GETTING_DATA"
    
    originAccount = accounts[accounts.index(token["Account"])]
    originAccount["GameshubData"]["Money"] += int(amount)

    filePath = apiRepo.get_contents("GameshubApi/accounts.json","main")
    apiRepo.update_file(path=filePath.path,message="",content=json.dumps(accounts),sha=filePath.sha)
    updateToken(token)
    return f"GIVEN_{originAccount['Username']}_{str(amount)}_MONEYS"
def acceptFriendReq(token,friendeUUID):
    try:
        accounts = getJsonFileContents("GameshubApi/accounts.json","main")
        accountTokens = getJsonFileContents("GameshubApi/accountTokens.json","main")
        advancementsJson = getJsonFileContents("GameshubApi/advancements.json","main")
    except:
        return "ERROR_WHILST_GETTING_DATA"
    
    for currentToken in accountTokens:
        if currentToken["Token"] == token:
            tokenIndex = accountTokens.index(currentToken)
    tokenStatus = checkToken(token)
    if tokenStatus["TokenStatus"] == True:
        for currentAccount in accounts:
            if currentAccount["UUID"] == friendeUUID:
                friendeAccount = currentAccount
                break


        originsAccount = accounts[accounts.index(accountTokens[tokenIndex]["Account"])]
        try:
            frequestIndex = originsAccount["FriendRequests"].index({"sender":friendeAccount["UUID"]})
        except:
            return "ALREADY_FRIENDS"

        if len(originsAccount["Friends"])+1 >= 1:
            awardAdvancement(token,2)

        friendeAccount["Friends"].append(originsAccount["UUID"])
        originsAccount["Friends"].append(friendeAccount["UUID"])
        
        originsAccount["FriendRequests"].pop(frequestIndex)

        filePath = apiRepo.get_contents("GameshubApi/accounts.json","main")
        apiRepo.update_file(path=filePath.path,message="",content=json.dumps(accounts),sha=filePath.sha)

        for currentToken in accountTokens:
            if currentToken["Account"]["UUID"] == friendeAccount["UUID"]:
                newFriendToken = currentToken
                awardMoney(newFriendToken,100)
                updateToken(newFriendToken)
                break
        updateToken(token)
        awardMoney(token,100)
        return "NEW_FRIENDS"
    else:
        return "INVALID_TOKEN"
def sendFriendRequest(tokenOfSender,ElementOfReciever):
    # Element is always UUID
    try:
        accounts = getJsonFileContents("GameshubApi/accounts.json","main")
        accountTokens = getJsonFileContents("GameshubApi/accountTokens.json","main")
        advancementsJson = getJsonFileContents("GameshubApi/advancements.json","main")
    except:
        return "ERROR_WHILST_GETTING_DATA"
    
    for currentToken in accountTokens:
        if currentToken["Token"] == tokenOfSender:
            tokenIndexOfSender = accountTokens.index(currentToken)
            senderAccount = accountTokens[tokenIndexOfSender]["Account"]
            break
    for account in accounts:
        if account["UUID"] == ElementOfReciever:
            reciever = account
            break
    tokenOfReciever = "INVALID_TOKEN"
    for currentToken in accountTokens:
        if currentToken["Account"]["UUID"] == ElementOfReciever:
            tokenOfReciever = currentToken
            break
    # friend request structure
    # {
    #    "sender": "SenderAccountUUID",
    # }
    def senderAcc():
        for currentToken in accountTokens:
            if currentToken["Token"] == tokenOfSender:
                tokenIndexOfSender = accountTokens.index(currentToken)
                senderAccount = accountTokens[tokenIndexOfSender]["Account"]
                return senderAccount or None
                break
    senderAccc = senderAcc()
    if not senderAccc == None:
        prebuildRequest = {
            "sender": senderAcc()["UUID"]
        }
    else:
        return "SENDER_ACCOUNT_NOT_FOUND"
    try:
        indexer = reciever["FriendRequests"].index(prebuildRequest)
    except:
        indexer = {"Indexer":False}
    if indexer == {"Indexer":False}:
        reciever["FriendRequests"].append(prebuildRequest)
        filePath = apiRepo.get_contents("GameshubApi/accounts.json","main")
        apiRepo.update_file(path=filePath.path,message="",content=json.dumps(accounts),sha=filePath.sha)
        updateToken(tokenOfReciever)
        return "FRIEND_REQUEST_SENT"
    else:
        return "SENDER_HAS_ALREADY_SEND_REQUEST_TO_THE_RECIVER"
def updateAcc(accountUUID,token):
    try:
        accounts = getJsonFileContents("GameshubApi/accounts.json","main")
    except:
        return "THERE_ARE_NO_ACCOUNTS"
    i = 0
    acc = {}
    while i < len(accounts)+1:
        try:
            currentAccount = accounts[i]
        except:
            return "COULD_NOT_FIND_ACCOUNT_WITH_UUID_"+accountUUID
        
        if currentAccount["UUID"] == accountUUID:
            acc = currentAccount
            if not "Advancements" in currentAccount["GameshubData"]:
                currentAccount["GameshubData"].update({"Advancements": [{"id":1,"header":"Welcome!","desc":"You get this achievement when you first sign up to Gameshub!","img":"None","reward":50}]})
            if not "Money" in currentAccount["GameshubData"]:
                currentAccount["GameshubData"].update({"Money":50})
            if not "Purchases" in currentAccount["GameshubData"]:
                currentAccount["GameshubData"].update({"Purchases": []})
            if not "GameData" in currentAccount["GameshubData"]:
                currentAccount["GameshubData"].update({"GameData":[]})
    filePath = apiRepo.get_contents("GameshubApi/accounts.json","main")
    apiRepo.update_file(path=filePath.path,message="",content=json.dumps(accounts),sha=filePath.sha)

    updateToken(token)
    return f"DONE_{json.dumps(acc)}"
def updateSpecialPrice():
    try:
        accounts = getJsonFileContents("GameshubApi/accounts.json","main")
        specialPrices = getJsonFileContents("GameshubApi/specialPrice.json","main")
        accountTokens = getJsonFileContents("GameshubApi/accountTokens.json","main")
        advancementsJson = getJsonFileContents("GameshubApi/advancements.json","main")
    except:
        return "ERROR_WHILST_GETTING_DATA"
    
    if int(specialPrices["expires"]) >= time.time():
        pass

    return "NOT_YET_COMPLETED"
def awardAdvancement(token,advancementId):
    try:
        accounts = getJsonFileContents("GameshubApi/accounts.json","main")
        accountTokens = getJsonFileContents("GameshubApi/accountTokens.json","main")
        advancementsJson = getJsonFileContents("GameshubApi/advancements.json","main")
    except:
        accounts = []
        accountTokens = []
        return "NO_ACCOUNTS"
    
    tokenStatusResp = checkToken(token)
    if tokenStatusResp["TokenStatus"] == True:
        try:
            accountIndex = accounts.index(tokenStatusResp["Account"])
        except:
            updateToken(token)
            try:
                accountIndex = accounts.index(tokenStatusResp["Account"])
            except:
                updateToken(token)
                return "ACCOUNT_TOKEN_NOT_UPDATED"
        currentAccount = accounts[accountIndex]
        for advancement in advancementsJson:
            if advancement["id"] == advancementId:
                for userAdvancement in currentAccount["GameshubData"]["Advancements"]:
                    if advancement == userAdvancement:
                        return "USER_ALREADY_HAS_THIS_ADVANCEMENT"
                
                currentAccount["GameshubData"]["Advancements"].append(advancement)
                currentAccount["GameshubData"]["Money"] += int(advancement["reward"])
                print(currentAccount,accounts)
                filePath = apiRepo.get_contents("GameshubApi/accounts.json","main")
                apiRepo.update_file(path=filePath.path,message="",content=json.dumps(accounts),sha=filePath.sha)
                updateAcc(currentAccount["UUID"],token)
                updateToken(token)

                return f'ADVANCEMENT_ADDED'
        return "CANNOT_FIND_ADVANCEMENT!"
    else:
        return "INVALID_ACCOUNT_TOKEN"
def updateToken(token):
    try:
        accounts = getJsonFileContents("GameshubApi/accounts.json","main")
        accountTokens = getJsonFileContents("GameshubApi/accountTokens.json","main")
        advancementsJson = getJsonFileContents("GameshubApi/advancements.json","main")
    except:
        return "NO_TOKENS"
    
    i = 0
    while i < len(accountTokens):
        try:
            currentAccountToken = accountTokens[i]
        except:
            return "TOKEN_DOSNT_EXIST"
        
        if token == "INVALID_TOKEN":
            return "INVALUD_TOKEN"
        if currentAccountToken["Token"] == token:
            x = 0
            while x < len(accounts):
                try:
                    currentAccount = accounts[x]
                except:
                    return "ACCOUNT_NOT_FOUND"
                if currentAccount["UUID"] == currentAccountToken["Account"]["UUID"]:
                    currentAccountToken["Account"] = currentAccount
                    filePath = apiRepo.get_contents("GameshubApi/accountTokens.json","main")
                    apiRepo.update_file(path=filePath.path,message="",content=json.dumps(accountTokens),sha=filePath.sha)
                    return "UPDATED_ACCOUNT"
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
