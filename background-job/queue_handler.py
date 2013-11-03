from leagueapi import legendaryapi
import os
import json
import time
import urllib

DATA_DIRECTORY = '/drive1/inhouse-data-dump'
SLEEP_TIME = 7200 # 2 hours in seconds
ADDITIONAL_SLEEP_TIME = 3600 # 1 hour in seconds

def handler(summonerName):
    print "Processing", summonerName
    legendaryApi = legendaryapi.LegendaryAPI()

    currentGameData = legendaryApi.getInProgressGameBySummonerName(summonerName)
    if currentGameData == None:
        print "Unable to get current game data for", summonerName
        return
    
    # write current game data to disk
    try:
        gameId = currentGameData['game']['id']
        print "Game id:", gameId
    except KeyError:
        print "No game ID found:", currentGameData
        
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
    
    summoners = []
    playerData = []
    try:
        playerData.extend(currentGameData['game']['teamOne']['array'])
        playerData.extend(currentGameData['game']['teamTwo']['array'])
        
        for player in playerData:
            summoners.append(player['summonerName'])
    except KeyError:
        print "Error getting summoner names"
        
    print "Summoners:", summoners
    
    # sleep, then check all summoner's match histories for the game ID
    print "Sleeping for %s seconds" % SLEEP_TIME
    time.sleep(SLEEP_TIME)
    
    for summoner in summoners:
        jsonOutputPath = os.path.join(gameDirectoryPath, "%s.json" % summoner)
        summonerUrlName = urllib.quote(summoner)
        recentGameData = legendaryApi.getRecentGamesBySummonerName(summonerUrlName)
        
        with open(jsonOutputPath, 'w') as outfile:
            json.dump(recentGameData, outfile, indent=2, sort_keys=True)
            
    # TODO add additional sleep time