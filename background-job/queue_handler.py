from leagueapi import legendaryapi
import os
import json
import time
import urllib
from db import mongo_dao

DATA_DIRECTORY = '/drive1/inhouse-data-dump'
SLEEP_TIME = 7200 # 2 hours in seconds
ADDITIONAL_SLEEP_TIME = 3600 # 1 hour in seconds

def handler(summonerName):
    print "Processing", summonerName

    currentGameData = legendaryapi.getInProgressGameBySummonerName(summonerName)
    if currentGameData == None:
        print "Unable to get current game data for %s. Player may not be in a game." % summonerName
        return
    
    if not isInHouseGame(currentGameData):
        return
    
    # write current game data to disk
    try:
        gameId = currentGameData['game']['id']
        print "Game id:", gameId
    except KeyError:
        print "No game ID found:", currentGameData
        return
        
    gameDirectoryPath = os.path.join(DATA_DIRECTORY, str(gameId))
    if not os.path.exists(gameDirectoryPath):
        os.mkdir(gameDirectoryPath)
    else:
        # this directory already exists
        print "Game ID %s already exists" % gameId
        return
        
    gameDataFileName = os.path.join(gameDirectoryPath, "%s.json" % gameId)
    with open(gameDataFileName, 'w') as outfile:
        json.dump(currentGameData, outfile, indent=2, sort_keys=True)
        print "Game data saved to", gameDataFileName
        
        mongo_dao.insertGame(currentGameData)
        print "Game data written to MongoDB"
    
    summoners = []
    playerData = []
    try:
        playerData.extend(currentGameData['game']['teamOne']['array'])
        playerData.extend(currentGameData['game']['teamTwo']['array'])
        
        for player in playerData:
            summoners.append(player['summonerName'])
    except KeyError:
        print "Error getting summoner names"
        return
        
    print "Summoners:", summoners
    
    # sleep, then check all summoner's match histories for the game ID
    print "Sleeping for %s seconds" % SLEEP_TIME
    time.sleep(SLEEP_TIME)

    saveSummonerStatsForGameId(gameId, summoners)
    
def saveSummonerStatsForGameId(gameId, summoners):
    gameDirectoryPath = os.path.join(DATA_DIRECTORY, str(gameId))
    
    for summoner in summoners:
        jsonOutputPath = os.path.join(gameDirectoryPath, "%s.json" % summoner)
        summonerUrlName = urllib.quote(summoner)
        
        gameIdExists = False
        while not gameIdExists:
            recentGameData = legendaryapi.getRecentGamesBySummonerName(summonerUrlName)
            gameIdExists = gameIdExistsInRecentGames(gameId, recentGameData)
            if not gameIdExists:
                print "Game id %s is not in %s's recent history. Sleeping for %s and retrying" % (gameId, summoner, ADDITIONAL_SLEEP_TIME)
                time.sleep(ADDITIONAL_SLEEP_TIME)
        
        with open(jsonOutputPath, 'w') as outfile:
            game = getGameFromRecentGamesById(gameId, recentGameData)
            
            json.dump(game, outfile, indent=2, sort_keys=True)
            print "Summoner game history saved to", jsonOutputPath
            
            mongo_dao.insertGameResult(game)
            print "%s game history saved to MongoDB" % summoner
            
def gameIdExistsInRecentGames(gameId, recentGameJsonData):
    for gameStats in recentGameJsonData['gameStatistics']['array']:
        if gameStats['gameId'] == gameId:
            return True
    
    return False
    
def getGameFromRecentGamesById(gameId, recentGameJsonData):
    for gameStats in recentGameJsonData['gameStatistics']['array']:
        if gameStats['gameId'] == gameId:
            return gameStats
    
    return None
    
def isInHouseGame(gameData):
    """Criteria:
    - PRACTICE_GAME or CUSTOM_GAME type
    - 10 players in game
    - No bots
    """
    
    currentGameType = gameData['game']['gameType']
    if currentGameType != "CUSTOM_GAME" and currentGameType != "PRACTICE_GAME":
        print "Not in house game. Current game type is", currentGameType
        return False
    
    teamOneArray = gameData['game']['teamOne']['array']
    teamTwoArray = gameData['game']['teamTwo']['array']
    players = []
    players.extend(teamOneArray)
    players.extend(teamTwoArray)
    
    numPlayers = len(players)
    if numPlayers < 10:
        print "Not in house game. Number of players is", numPlayers
        return False
        
    for player in players:
        if 'summonerId' not in player:
            print "Not in house game. There are bots!"
            return False
        
    return True