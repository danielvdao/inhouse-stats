from flask import Flask
from flask import request
import stats_pp

app = Flask(__name__)

@app.route("/")
def index():
    returnString = "Example usages:<br>"
    returnString += _surroundLink("http://garsh0p.no-ip.biz:5000/summoners")
    returnString += _surroundLink("http://garsh0p.no-ip.biz:5000/summoners?minGames=5")
    returnString += _surroundLink("http://garsh0p.no-ip.biz:5000/summoners/gar")
    returnString += _surroundLink("http://garsh0p.no-ip.biz:5000/champions")
    returnString += _surroundLink("http://garsh0p.no-ip.biz:5000/champions?minGames=5")
    returnString += _surroundLink("http://garsh0p.no-ip.biz:5000/champions/nasus")
    returnString += _surroundLink("http://garsh0p.no-ip.biz:5000/championContest")
    return returnString
    
@app.route("/summoners/")
def summonerWinRates():
    minGames = 1
    if request.args.get("minGames") is not None:
        minGames = int(request.args.get("minGames"))
    returnString = _getCommonHtmlString()
    returnString += stats_pp.getAllSummonerWinRates(minGames=minGames)
    return returnString
    
@app.route("/summoners/<name>")
def summonerStats(name):
    returnString = _getCommonHtmlString()
    returnString += stats_pp.getSummonerStats(name)
    return returnString
    
@app.route("/champions/", methods=['GET'])
def championWinRates():
    minGames = 1
    if request.args.get("minGames") is not None:
        minGames = int(request.args.get("minGames"))
    returnString = _getCommonHtmlString()
    returnString += stats_pp.getAllChampionWinRates(minGames=minGames)
    return returnString
    
@app.route("/champions/<name>")
def championStats(name):
    returnString = _getCommonHtmlString()
    returnString += stats_pp.getChampionStats(name)
    return returnString
    
@app.route("/championContest/", methods=['GET'])
def championContestRates():
    minGames = 1
    if request.args.get("minGames") is not None:
        minGames = int(request.args.get("minGames"))
    returnString = _getCommonHtmlString()
    returnString += stats_pp.getAllChampionContestRates(minGames=minGames)
    return returnString    
    
def _getCommonHtmlString():
    returnString = ""
    returnString += "<pre>"
    return returnString

def _surroundLink(link):
    return '<a href="%s">%s</a><br>' % (link, link)
    
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
