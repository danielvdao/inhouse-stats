import json
import urllib2

getSummonerByNameUrl = "http://legendaryapi.com/api/v1.0/na/summoner/getSummonerByName/%s"
getRecentGamesByAccountIdUrl = "http://legendaryapi.com/api/v1.0/na/summoner/getRecentGames/%s"
retrieveInProgressGameBySummonerNameUrl  = "http://legendaryapi.com/api/v1.0/na/summoner/retrieveInProgressSpectatorGameInfo/%s"
getPublicSummonerDataByAccountIdUrl ="http://legendaryapi.com/api/v1.0/na/summoner/getAllPublicSummonerDataByAccount/%s"

class LegendaryAPI(object):
    """All functions return a JSON dictionary"""
    
    def getAccountIdBySummonerName(self, summonerName):
        url = getSummonerByNameUrl % summonerName
        print "Getting", url
        jsonObject = json.load(urllib2.urlopen(url))
        if 'acctId' in jsonObject:
            return jsonObject['acctId']
        else:
            return None
            
    def getSummonerNameByAccountId(self, accountId):
        url = getPublicSummonerDataByAccountIdUrl % accountId
        print "Getting", url
        jsonObject = json.load(urllib2.urlopen(url))
        
        if 'summoner' in jsonObject:
            return jsonObject['summoner']['name']
        else:
            return None
        
    def getInProgressGameBySummonerName(self, summonerName):
        url = retrieveInProgressGameBySummonerNameUrl % summonerName
        print "Getting", url
        jsonData = json.load(urllib2.urlopen(url))
        if 'error' in jsonData:
            return None
        else:
            return jsonData
        
    def getRecentGamesBySummonerName(self, summonerName):
        accountId = self.getAccountIdBySummonerName(summonerName)
        if accountId == None:
            return None
        
        url = getRecentGamesByAccountIdUrl % accountId
        print "Getting", url
        return json.load(urllib2.urlopen(url))
        
    def getRecentGamesByAccountId(self, accountId):
        url = getRecentGamesByAccountIdUrl % accountId
        print "Getting", url
        return json.load(urllib2.urlopen(url))