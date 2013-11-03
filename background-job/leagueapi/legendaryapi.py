import json
import urllib2

getSummonerByNameUrl = "http://legendaryapi.com/api/v1.0/na/summoner/getSummonerByName/%s"
getRecentGamesByAccountIdUrl = "http://legendaryapi.com/api/v1.0/na/summoner/getRecentGames/%s"
retrieveInProgressGameBySummonerNameUrl  = "http://legendaryapi.com/api/v1.0/na/summoner/retrieveInProgressSpectatorGameInfo/%s"

class LegendaryAPI(object):
    """All functions return a JSON dictionary"""
    
    def getAccountIdBySummonerName(self, summonerName):
        jsonObject = json.load(urllib2.urlopen(getSummonerByNameUrl % summonerName))
        return jsonObject['acctId']
        
    def getInProgressGameBySummonerName(self, summonerName):
        accountId = self.getAccountIdBySummonerName(summonerName)
        return json.load(urllib2.urlopen(retrieveInProgressGameBySummonerNameUrl % accountId))
        
    def getRecentGamesBySummonerName(self, summonerName):
        accountId = self.getAccountIdBySummonerName(summonerName)
        return json.load(urllib2.urlopen(getRecentGamesByAccountIdUrl % accountId))