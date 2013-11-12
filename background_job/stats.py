from db import mongo_dao
from leagueapi import legendaryapi
from pytz import timezone
import pytz
from datetime import datetime

BLUE_TEAM_ID = 100
PURPLE_TEAM_ID = 200

DEFAULT_TIME_ZONE = 'US/Pacific'

# stat names

WIN = "WIN"
LOSE = "LOSE"
LEVEL = "LEVEL"

# if these are not present, assume value is 0
KILLS = "CHAMPIONS_KILLED"
DEATHS = "NUM_DEATHS"
ASSISTS = "ASSISTS"
DAMAGE_TAKEN = "TOTAL_DAMAGE_TAKEN"
WARDS_PLACED = "WARD_PLACED"
GOLD_EARNED = "GOLD_EARNED"
MINIONS_KILLED = "MINIONS_KILLED"
DAMAGE_DEALT_TO_CHAMPIONS = "TOTAL_DAMAGE_DEALT_TO_CHAMPIONS"
JUNGLE_MONSTERS_KILLED = "NEUTRAL_MINIONS_KILLED"

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
            gameList.append((str(createDatetime), gameId))
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
    
def getNumberOfGamesChampionWon(championName):
    championId = legendaryapi.getChampionIdFromName(championName)
    gameResults = mongo_dao.getGameResultsIncludingChampion(championId)
    
    wins = 0
    for gameResult in gameResults:
        statsArray = gameResult['statistics']['array']
        wins = wins + _getStatisticByName(statsArray, WIN)
    return wins
    
def getChampionPickRate(championName):
    return 1.0 * getNumberOfGamesChampionIsPicked(championName) / getTotalGames()

def getChampionBanRate(championName):
    return 1.0 * getNumberOfGamesChampionIsBanned(championName) / getTotalGames()

def getChampionContestRate(championName):
    return 1.0 * getNumberOfGamesChampionIsContested(championName) / getTotalGames()
    
def getChampionWinRate(championName):
    return 1.0 * getNumberOfGamesChampionWon(championName) / getNumberOfGamesChampionIsPicked(championName)
    
def getAllChampionWinRates(minGames=1):
    """Returns a sorted list of champions, wins, losses, and winrate.
    """
    winrates = []
    
    for championId in legendaryapi.getAllChampionIds():
        championName = legendaryapi.getChampionNameFromId(championId)
        numGames = getNumberOfGamesChampionIsPicked(championName)
        if numGames >= minGames:
            winrateEntry = {}
            winrateEntry['champion'] = championName
            winrateEntry['won'] = getNumberOfGamesChampionWon(championName)
            winrateEntry['lost'] = numGames - winrateEntry['won']
            winrateEntry['winrate'] = getChampionWinRate(championName)
            
            winrates.append(winrateEntry)
            
    return sorted(winrates, key=lambda winrate: winrate['winrate'], reverse=True)
    
def getAllChampionContestRates(minGames=1):
    contestRates = []
    
    for championId in legendaryapi.getAllChampionIds():
        championName = legendaryapi.getChampionNameFromId(championId)
        numGames = getNumberOfGamesChampionIsContested(championName)
        if numGames >= minGames:
            contestRateEntry = {}
            contestRateEntry['champion'] = championName
            contestRateEntry['picked'] = getNumberOfGamesChampionIsPicked(championName)
            contestRateEntry['banned'] = getNumberOfGamesChampionIsBanned(championName)
            contestRateEntry['contested'] = getNumberOfGamesChampionIsContested(championName)
            contestRateEntry['contestRate'] = getChampionContestRate(championName)
            contestRates.append(contestRateEntry)
    
    return sorted(contestRates, key=lambda contestRate: contestRate['contestRate'], reverse=True)
    
def getAllSummonerWinRates(minGames=1):
    # TODO sort this by wins instead of %?
    pass
    
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
    # TODO game specific info. we only have summoner specific data for now.
    gameInfo = []
    
    gameResults = mongo_dao.getResultsForGameId(gameId)
    for gameResult in gameResults:
        summonerId = gameResult['userId']
        gameInfo.append(getSummonerStatsForGameId(gameId, summonerId))
    
    return gameInfo
    
def getSummonerNamesForGameId(gameId):
    game = mongo_dao.getGameById(gameId)
    
    summoners = []
    playerData = []
    playerData.extend(game['game']['teamOne']['array'])
    playerData.extend(game['game']['teamTwo']['array'])
    
    for player in playerData:
        summoners.append(player['summonerName'])
            
    return summoners
    
def getSummonerStatsForGameIdBySummonerName(gameId, summonerName):
    summonerId = mongo_dao.getSummonerIdFromName(summonerName)
    return getSummonerStatsForGameId(gameId, summonerId, summonerName)
    
def getSummonerStatsForGameId(gameId, summonerId, summonerName=None):
    """
    Champion
    Win?
    Level
    KDA
    CS
    Jungle creeps killed
    Gold earned
    Damage dealt to champions
    Damage taken
    Wards placed
    """
    summonerStats = {}
    if summonerName is None:
        summonerName = mongo_dao.getSummonerNameFromId(summonerId) # TODO REMOVE THIS API CALL
    
    gameResults = mongo_dao.getResultsForGameId(gameId)
    gameResult = _getResultFromGameResultsBySummonerId(gameResults, summonerId)
    if gameResult is None:
        return None
        
    statsArray = gameResult['statistics']['array']
    
    summonerStats['Summoner'] = summonerName
    summonerStats['Game ID'] = gameId
    summonerStats['Game Date'] = str(_convertUtcDatetimeStringToDatetimeWithTimeZone(gameResult['createDate'], DEFAULT_TIME_ZONE))
    summonerStats['Champion'] = legendaryapi.getChampionNameFromId(gameResult['championId'])
    summonerStats['Won'] = _getStatisticByName(statsArray, WIN) == 1
    summonerStats['Level'] = _getStatisticByName(statsArray, LEVEL)
    summonerStats['Kills'] = _getStatisticByName(statsArray, KILLS)
    summonerStats['Deaths'] = _getStatisticByName(statsArray, DEATHS)
    summonerStats['Assists'] = _getStatisticByName(statsArray, ASSISTS)
    summonerStats['Jungle Monsters Killed'] = _getStatisticByName(statsArray, JUNGLE_MONSTERS_KILLED)
    summonerStats['Minions Killed'] = _getStatisticByName(statsArray, MINIONS_KILLED) + summonerStats['Jungle Monsters Killed']
    summonerStats['Gold Earned'] = _getStatisticByName(statsArray, GOLD_EARNED)
    summonerStats['Damage Dealt To Champions'] = _getStatisticByName(statsArray, DAMAGE_DEALT_TO_CHAMPIONS)
    summonerStats['Damage Taken'] = _getStatisticByName(statsArray, DAMAGE_TAKEN)
    summonerStats['Wards Placed'] = _getStatisticByName(statsArray, WARDS_PLACED)
    
    return summonerStats
    
def getSummonerStatsForAllGames(summonerName):
    summonerId = mongo_dao.getSummonerIdFromName(summonerName)
    
    stats = []
    for gameId in mongo_dao.getAllGameIds():
        singleGameStats = getSummonerStatsForGameId(gameId, summonerId, summonerName)
        if singleGameStats is not None:
            stats.append(singleGameStats)
        
    return stats
    
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
    
def _getStatisticByName(statsArray, statName):
    """If a stat can't be found, we assume its value is 0.
    """
    for stat in statsArray:
        if stat['statType'] == statName:
            return stat['value']
    return 0
    
def _getResultFromGameResultsBySummonerId(gameResults, summonerId):
    for gameResult in gameResults:
        if gameResult['userId'] == summonerId:
            return gameResult
            
    return None