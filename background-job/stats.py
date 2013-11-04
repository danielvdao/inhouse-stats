from db import mongo_dao
from leagueapi import legendaryapi

def getTotalGames():
    return len(mongo_dao.getAllGameIds())

def getNumberOfGamesChampionIsPicked(championName):
    championId = legendaryapi.getChampionIdFromName(championName)
    timesPicked = 0
    
    gameIds = mongo_dao.getAllGameIds()
    for gameId in gameIds:
        gameData = mongo_dao.getGameById(gameId)
        for pick in gameData['game']['playerChampionSelections']['array']:
            if championId == pick['championId']:
                timesPicked = timesPicked + 1
                break
    
    return timesPicked

def getNumberOfGamesChampionIsBanned(championName):
    championId = legendaryapi.getChampionIdFromName(championName)
    timesBanned = 0
    
    gameIds = mongo_dao.getAllGameIds()
    for gameId in gameIds:
        gameData = mongo_dao.getGameById(gameId)
        for ban in gameData['game']['bannedChampions']['array']:
            if championId == ban['championId']:
                timesBanned = timesBanned + 1
                break
        
    return timesBanned
    
def getNumberOfGamesChampionIsContested(championName):
    return getNumberOfGamesChampionIsPicked(championName) + getNumberOfGamesChampionIsBanned(championName)
    
def getChampionPickRate(championName):
    return 1.0 * getNumberOfGamesChampionIsPicked(championName) / getTotalGames()

def getChampionBanRate(championName):
    return 1.0 * getNumberOfGamesChampionIsBanned(championName) / getTotalGames()

def getChampionContestRate(championName):
    return 1.0 * getNumberOfGamesChampionIsContested(championName) / getTotalGames()
    
def getCompleteGameInfo(gameId):
    """Returns a dictionary of game info.
    Format specified in google doc TODO
    """
    pass