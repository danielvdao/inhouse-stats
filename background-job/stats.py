from db import mongo_dao
from leagueapi import legendaryapi

BLUE_TEAM_ID = 100
PURPLE_TEAM_ID = 200

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
    
def getBlueSideWins():
    blueSideWins = 0
    
    gameIds = mongo_dao.getAllGameIds()
    for gameId in gameIds:
        gameResults = mongo_dao.getResultsForGameId(gameId)
        for gameResult in gameResults:
            win = _didPlayerWinFromResult(gameResult)
            teamId = gameResult['teamId']
            
            if win:
                if teamId == BLUE_TEAM_ID:
                    blueSideWins = blueSideWins + 1
            else:
                if teamId == PURPLE_TEAM_ID:
                    blueSideWins = blueSideWins + 1
            
            break # we only need 1 result to figure out who wins
    
    return blueSideWins
    
def getPurpleSideWins():
    return getTotalGames() - getBlueSideWins()

def getBlueSideWinRate():
    return 1.0 * getBlueSideWins() / getTotalGames()

def getPurpleSideWinRate():
    return 1.0 * getPurpleSideWins() / getTotalGames()
    
def getCompleteGameInfo(gameId):
    """Returns a dictionary of game info.
    Format specified in google doc TODO
    """
    pass
    
# HELPERS

def _didPlayerWinFromResult(gameResult):
    for stat in gameResult['statistics']['array']:
        if stat['statType'] == 'WIN':
            return True
        elif stat['statType'] == 'LOSE':
            return False
            
    raise Exception('Game result did not have WIN or LOSE:\n %s' % gameResult)