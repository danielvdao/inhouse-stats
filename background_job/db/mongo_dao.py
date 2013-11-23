import pymongo
from pymongo.mongo_client import DuplicateKeyError

dao = pymongo.MongoClient()

DB_NAME = "inhouse_stats"
GAME_COLLECTION_NAME = "games" 
GAME_RESULT_COLLECTION_NAME = "game_results" # individual summoner results
SUMMONERS_COLLECTION_NAME = "summoners"

ID_KEY_NAME = "_id"

db = dao[DB_NAME]

def insertGame(gameJsonData):
    # set _id to game ID
    gameId = gameJsonData['game']['id']
    gameJsonData[ID_KEY_NAME] = gameId
    
    db[GAME_COLLECTION_NAME].insert(gameJsonData)

def insertGameResult(gameResultJsonData):
    # let _id be autogenerated
    db[GAME_RESULT_COLLECTION_NAME].insert(gameResultJsonData)
    
def insertSummoner(summonerId, summonerName):
    # remove all white space and make whole string lowercase
    normalizedName = "".join(summonerName.split()).lower()
    summoner = {
        '_id': summonerId,
        'name': summonerName,
        'normalized_name': normalizedName
    }
    
    try:
        db[SUMMONERS_COLLECTION_NAME].insert(summoner)
    except DuplicateKeyError:
        pass # do nothing
        
def getAllGameIds():
    cursor = db[GAME_COLLECTION_NAME].find(fields={"_id": True})
    
    gameIds = []
    for element in cursor:
        gameIds.append(element['_id'])
    return gameIds
    
def getGameById(gameId):
    return db[GAME_COLLECTION_NAME].find_one({"_id": gameId})
    
def getResultsForGameId(gameId):
    results = []
    
    cursor = db[GAME_RESULT_COLLECTION_NAME].find({'gameId': gameId})
    for element in cursor:
        results.append(element)
    
    return results
    
def getSummonersForGameId(gameId):
    summoners = []
    
    game = db[GAME_COLLECTION_NAME].find_one({'_id': gameId})
    for summoner in game['game']['playerChampionSelections']['array']:
        summoners.append(summoner['summonerInternalName'])
    
    return summoners
    
def getAllGamesIncludingChampion(championId):
    results = []
    
    cursor = db[GAME_COLLECTION_NAME].find(
        {
            '$or':[
                {'game.playerChampionSelections.array.championId' : championId}, 
                {'game.bannedChampions.array.championId': championId}
             ]
        }
    )
    for element in cursor:
        results.append(element)
    
    return results
    
def getGameResultsIncludingChampion(championId):
    results = []
    
    cursor = db[GAME_RESULT_COLLECTION_NAME].find({'championId':championId})
    for element in cursor:
        results.append(element)
    
    return results
    
def getGameResultsForSummonerName(summonerName):
    summonerId = getSummonerIdFromName(summonerName)
    gameResults = []
    
    for cursor in db[GAME_RESULT_COLLECTION_NAME].find({"userId": summonerId}):
        gameResults.append(cursor)
    
    return gameResults
    
def getGameIdsWithSummonersOnSameTeam(summoners):
    summonerIds = [getSummonerIdFromName(summoner) for summoner in summoners]
    
    cursor = db[GAME_COLLECTION_NAME].find({
        '$or': [
            {'$and': [{'game.teamOne.array.accountId':summonerId} for summonerId in summonerIds]},
            {'$and': [{'game.teamTwo.array.accountId':summonerId} for summonerId in summonerIds]}
        ]
    })
    
    return [element['_id'] for element in cursor]

def getGameIdsMissingResults():
    """Checks to see if all game ids have results. Return a list of game ids that don't.
    """
    missingGameIds = []
    
    allGameIds = getAllGameIds()
    for gameId in allGameIds:
        if not getResultsForGameId(gameId):
            missingGameIds.append(gameId)
    
    return missingGameIds
    
def getSummonerNameFromId(summonerId):
    try:
        return db[SUMMONERS_COLLECTION_NAME].find_one({"_id": summonerId})['name']
    except:
        return None

def getSummonerIdFromName(summonerName):
    normalizedName = "".join(summonerName.split()).lower()
    try:
        return db[SUMMONERS_COLLECTION_NAME].find_one({"normalized_name": normalizedName})['_id']
    except:
        return None
        
def getStylizedSummonerName(summonerName):
    normalizedName = "".join(summonerName.split()).lower()
    try:
        return db[SUMMONERS_COLLECTION_NAME].find_one({"normalized_name": normalizedName})['name']
    except:
        return None