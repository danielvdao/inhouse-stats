import json
import urllib2
import os
import unirest

getSummonerByNameUrl = "https://community-league-of-legends.p.mashape.com/api/v1.0/NA/summoner/getSummonerByName/%s"
getRecentGamesByAccountIdUrl = "https://community-league-of-legends.p.mashape.com/api/v1.0/NA/summoner/getRecentGames/%s"
retrieveInProgressGameBySummonerNameUrl  = "https://community-league-of-legends.p.mashape.com/api/v1.0/NA/summoner/retrieveInProgressSpectatorGameInfo/%s"
getPublicSummonerDataByAccountIdUrl ="https://community-league-of-legends.p.mashape.com/api/v1.0/NA/summoner/getAllPublicSummonerDataByAccount/%s"

CHAMPION_MAPPING_FILENAME = os.path.join(os.path.dirname(__file__), "champion_mapping.raw")

championIdToNameMap = {}
championNameToIdMap = {}

def getAccountIdBySummonerName(summonerName):
    url = getSummonerByNameUrl % summonerName
    response = unirest.get(url,
        headers={
            "X-Mashape-Authorization": "4YBi2VGcGJ0ClhZqk5l2sQsyEwOaBtzc"
        }
    )
    body = response.body
    if 'acctId' in body:
        return body['acctId']
    else:
        return None
        
def getSummonerNameByAccountId(accountId):
    url = getPublicSummonerDataByAccountIdUrl % accountId
    response = unirest.get(url,
        headers={
            "X-Mashape-Authorization": "4YBi2VGcGJ0ClhZqk5l2sQsyEwOaBtzc"
        }
    )
    body = response.body
    if 'summoner' in body:
        return body['summoner']['name']
    else:
        return None
    
def getInProgressGameBySummonerName(summonerName):
    url = retrieveInProgressGameBySummonerNameUrl % summonerName
    response = unirest.get(url,
        headers={
            "X-Mashape-Authorization": "4YBi2VGcGJ0ClhZqk5l2sQsyEwOaBtzc"
        }
    )
    body = response.body
    if 'error' in body:
        return None
    else:
        return body
    
def getRecentGamesBySummonerName(summonerName):
    accountId = getAccountIdBySummonerName(summonerName)
    if accountId == None:
        return None
    
    url = getRecentGamesByAccountIdUrl % accountId
    response = unirest.get(url,
        headers={
            "X-Mashape-Authorization": "4YBi2VGcGJ0ClhZqk5l2sQsyEwOaBtzc"
        }
    )
    return response.body
    
def getRecentGamesByAccountId(accountId):
    url = getRecentGamesByAccountIdUrl % accountId
    response = unirest.get(url,
        headers={
            "X-Mashape-Authorization": "4YBi2VGcGJ0ClhZqk5l2sQsyEwOaBtzc"
        }
    )
    return response.body
    
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