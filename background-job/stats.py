from db import mongo_dao
from leagueapi import legendaryapi
from pytz import timezone
import pytz
from datetime import datetime

BLUE_TEAM_ID = 100
PURPLE_TEAM_ID = 200

DEFAULT_TIME_ZONE = 'US/Pacific'

def getTotalGames():
    return len(mongo_dao.getAllGameIds())
    
def getAllGamesWithDate():
    """Returns a list of tuples of (game date, game id)
    """
    gameList = []
    
    gameIds = mongo_dao.getAllGameIds()
    for gameId in gameIds:
        # the time is stored in game results
        gameResults = mongo_dao.getResultsForGameId(gameId)
        
        # we only need one game result to get the time, so break after 1
        for gameResult in gameResults:
            createDateString = gameResult['createDate']
            createDatetime = _convertUtcDatetimeStringToDatetimeWithTimeZone(createDateString, DEFAULT_TIME_ZONE)
            gameList.append((createDatetime, gameId))
            break
    
    # sort
    return sorted(gameList, key=lambda game: game[0])

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
    
def getSummonerStatsForGameId(gameId, summonerName):
    """
    Level
    KDA
    CS
    Gold earned
    Damage dealt to champions
    Wards placed
    Jungle creeps killed
    """
    summonerId = legendaryapi.getAccountIdBySummonerName(summonerName)
    summonerStats = {}
    
    # TODO
    
    return summonerStats
    
# HELPERS

def _didPlayerWinFromResult(gameResult):
    for stat in gameResult['statistics']['array']:
        if stat['statType'] == 'WIN':
            return True
        elif stat['statType'] == 'LOSE':
            return False
            
    raise Exception('Game result did not have WIN or LOSE:\n %s' % gameResult)
    
def _convertUtcDatetimeStringToDatetimeWithTimeZone(utcString, timeZoneString):
    """UTC string is Riot's format.
    """
    unlocalizedDatetime = datetime.strptime(utcString, "%b %d, %Y %X %p")
    utcDatetime = pytz.utc.localize(unlocalizedDatetime)
    
    targetTimeZone = timezone(timeZoneString)
    targetDatetime = utcDatetime.astimezone(targetTimeZone)
    
    return targetDatetime