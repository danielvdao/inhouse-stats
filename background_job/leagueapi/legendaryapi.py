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

def getAccountIdBySummonerName(summonerName):
    url = getSummonerByNameUrl % summonerName
    jsonObject = json.load(urllib2.urlopen(url))
    if 'acctId' in jsonObject:
        return jsonObject['acctId']
    else:
        return None
        
def getSummonerNameByAccountId(accountId):
    url = getPublicSummonerDataByAccountIdUrl % accountId
    jsonObject = json.load(urllib2.urlopen(url))
    
    if 'summoner' in jsonObject:
        return jsonObject['summoner']['name']
    else:
        return None
    
def getInProgressGameBySummonerName(summonerName):
    url = retrieveInProgressGameBySummonerNameUrl % summonerName
    jsonData = json.load(urllib2.urlopen(url))
    if 'error' in jsonData:
        return None
    else:
        return jsonData
    
def getRecentGamesBySummonerName(summonerName):
    accountId = getAccountIdBySummonerName(summonerName)
    if accountId == None:
        return None
    
    url = getRecentGamesByAccountIdUrl % accountId
    return json.load(urllib2.urlopen(url))
    
def getRecentGamesByAccountId(accountId):
    url = getRecentGamesByAccountIdUrl % accountId
    return json.load(urllib2.urlopen(url))
    
def getChampionNameFromId(championId):
    return championIdToNameMap[championId]

def getChampionIdFromName(championName):
    return championNameToIdMap[_normalizeName(championName)]
    
def getAllChampionNames():
    return championNameToIdMap.keys()
    
def getAllChampionIds():
    return championIdToNameMap.keys()

def _normalizeName(name):
    return "".join(name.split()).lower()
    
# INIT

def init():
    # initialize champion lookup tables
    with open(CHAMPION_MAPPING_FILENAME) as file:
        for line in file:
            lineElements = line.split("=>")
            championId = int(lineElements[0].strip())
            championName = lineElements[1].strip()
            normalizedChampionName = _normalizeName(championName)
            championIdToNameMap[championId] = championName
            championNameToIdMap[normalizedChampionName] = championId
            
init()