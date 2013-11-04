import json
import urllib2
import os

getSummonerByNameUrl = "http://legendaryapi.com/api/v1.0/na/summoner/getSummonerByName/%s"
getRecentGamesByAccountIdUrl = "http://legendaryapi.com/api/v1.0/na/summoner/getRecentGames/%s"
retrieveInProgressGameBySummonerNameUrl  = "http://legendaryapi.com/api/v1.0/na/summoner/retrieveInProgressSpectatorGameInfo/%s"
getPublicSummonerDataByAccountIdUrl ="http://legendaryapi.com/api/v1.0/na/summoner/getAllPublicSummonerDataByAccount/%s"

CHAMPION_MAPPING_FILENAME = os.path.join(os.path.dirname(__file__), "champion_mapping.raw")

championIdToNameMap = {}
championNameToIdMap = {}

def init():
    # initialize champion lookup tables
    with open(CHAMPION_MAPPING_FILENAME) as file:
        for line in file:
            lineElements = line.split("=>")
            championId = int(lineElements[0].strip())
            championName = lineElements[1].strip()
            championIdToNameMap[championId] = championName
            championNameToIdMap[championName] = championId
            
init()

# END INIT

def getAccountIdBySummonerName(summonerName):
    url = getSummonerByNameUrl % summonerName
    print "Getting", url
    jsonObject = json.load(urllib2.urlopen(url))
    if 'acctId' in jsonObject:
        return jsonObject['acctId']
    else:
        return None
        
def getSummonerNameByAccountId(accountId):
    url = getPublicSummonerDataByAccountIdUrl % accountId
    print "Getting", url
    jsonObject = json.load(urllib2.urlopen(url))
    
    if 'summoner' in jsonObject:
        return jsonObject['summoner']['name']
    else:
        return None
    
def getInProgressGameBySummonerName(summonerName):
    url = retrieveInProgressGameBySummonerNameUrl % summonerName
    print "Getting", url
    jsonData = json.load(urllib2.urlopen(url))
    if 'error' in jsonData:
        return None
    else:
        return jsonData
    
def getRecentGamesBySummonerName(summonerName):
    accountId = self.getAccountIdBySummonerName(summonerName)
    if accountId == None:
        return None
    
    url = getRecentGamesByAccountIdUrl % accountId
    print "Getting", url
    return json.load(urllib2.urlopen(url))
    
def getRecentGamesByAccountId(accountId):
    url = getRecentGamesByAccountIdUrl % accountId
    print "Getting", url
    return json.load(urllib2.urlopen(url))
    
def getChampionNameFromId(championId):
    return championIdToNameMap[championId]

# TODO ignore case for this
def getChampionIdFromName(championName):
    return championNameToIdMap[championName]