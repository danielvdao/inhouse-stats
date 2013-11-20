import stats
from pandas import DataFrame

def getAllChampionContestRates(minGames=1):
    contestRateString = ""
    contestRateString += "Total Games: %d\n\n" % stats.getTotalGames()
    
    contestRates = stats.getAllChampionContestRates(minGames=minGames)
    dataFrame = DataFrame(contestRates, columns=(["champion", "picked", "banned", "contested", "contestRate"]))
    dataFrame = dataFrame.set_index("champion")
    contestRateString += dataFrame.to_string()
    
    return contestRateString
    
def getAllChampionWinRates(minGames=1):
    winRates = stats.getAllChampionWinRates(minGames=minGames)
    dataFrame = DataFrame(winRates, columns=["champion", "won", "lost", "winrate"])
    dataFrame = dataFrame.set_index("champion")
    return dataFrame.to_string()
    
def getCompleteGameInfo(gameId):
    # TODO
    return stats.getCompleteGameInfo(gameId)
    
def getAllSummonerWinRates(minGames=1):
    winRates = stats.getAllSummonerWinRates(minGames=minGames)
    dataFrame = DataFrame(winRates, columns=["Summoner", "Wins", "Losses", "Winrate"])
    dataFrame = dataFrame.set_index("Summoner")
    return dataFrame.to_string()
    
def getSummonerStats(summonerName):
    statsString = ""

    summonerStats = stats.getSummonerStats(summonerName)
    
    statsString += "Summoner: %s\n" % summonerStats['Summoner']
    statsString += "Total Games: %d\n" % summonerStats['Total Games']
    statsString += "Record: %d-%d\n" % (summonerStats['Wins'], summonerStats['Losses'])
    statsString += "Average KDA: %s/%s/%s\n" % (str(summonerStats['Average Kills']), str(summonerStats['Average Deaths']), str(summonerStats['Average Assists']))
    
    championStats = summonerStats['Champion stats']
    dataFrame = DataFrame(championStats, columns=[
        "Champion", "Wins", "Losses", "Kills", "Deaths", "Assists", "CS",
        "Jungle CS", "Damage Dealt", "Damage Taken", "Wards Placed"
    ])
    dataFrame = dataFrame.set_index("Champion")
    statsString += dataFrame.to_string()
    
    return statsString
    
def getChampionStats(championName):
    statsString = ""
    
    championStats = stats.getChampionStats(championName)
    
    statsString += "Champion: %s\n" % championStats['Champion']
    statsString += "Picked: %s\n" % championStats['Picks']
    statsString += "Banned: %s\n" % championStats['Bans']
    statsString += "Contested: %s\n" % championStats['Contested']
    statsString += "Record: %d-%d\n" % (championStats['Wins'], championStats['Losses'])
    
    summonerStats = championStats['Summoner stats']
    dataFrame = DataFrame(summonerStats, columns=[
        "Summoner", "Wins", "Losses", "Kills", "Deaths", "Assists", "CS",
        "Jungle CS", "Damage Dealt", "Damage Taken", "Wards Placed"
    ])
    dataFrame = dataFrame.set_index("Summoner")
    statsString += dataFrame.to_string()
    
    return statsString