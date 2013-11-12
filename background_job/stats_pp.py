import stats
from pandas import DataFrame

def getAllChampionContestRates(minGames=1):
    contestRates = stats.getAllChampionContestRates(minGames=minGames)
    dataFrame = DataFrame(contestRates, columns=(["champion", "picked", "banned", "contested", "contestRate"]))
    dataFrame = dataFrame.set_index("champion")
    return dataFrame.to_string()
    
def getAllChampionWinRates(minGames=1):
    winRates = stats.getAllChampionWinRates(minGames=minGames)
    dataFrame = DataFrame(winRates, columns=["champion", "won", "lost", "winrate"])
    dataFrame = dataFrame.set_index("champion")
    return dataFrame.to_string()
    
def getCompleteGameInfo(gameId):
    return stats.getCompleteGameInfo(gameId)