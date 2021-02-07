import argparse
import requests
from datetime import date
import win32com.client
import os
import pathlib
import urllib

today = date.today().strftime("%Y%m%d")
scoreboard = ""
standings = ""
path = ""

def main():
    parser = argparse.ArgumentParser(description="Pour utiliser l'outil, tu dois remplir les arguments ci dessous : ")

    parser.add_argument('--mode', "-M", help='GOD, OG, AG')
    parser.add_argument('--gameId', "-ID", help='Optionnel - L\'id du match pour le Game Of The Day')
    parser.add_argument('--date', "-D", help='Optionnel - Tu dois remplir la date voulue sur la forme YYYYMMDD (ex : 20210521) - Defaut : today')

    args = parser.parse_args()
    if args.date and len(args.date) == 8:
        global today
        today = args.date

    global scoreboard
    global standings
    standings = requests.get("http://data.nba.net/prod/v1/current/standings_all.json").json()
    scoreboard = requests.get("http://data.nba.net/10s/prod/v1/"+today+"/scoreboard.json").json()

    for team in standings["league"]["standard"]["teams"]:
        print("http://i.cdn.turner.com/nba/nba/.element/img/1.0/teamsites/logos/teamlogos_500x500/"+team["teamSitesOnly"]["teamTricode"]+".png")
        urllib.request.urlretrieve("http://i.cdn.turner.com/nba/nba/.element/img/1.0/teamsites/logos/teamlogos_500x500/"+team["teamSitesOnly"]["teamTricode"].lower()+".png", team["teamSitesOnly"]["teamTricode"] + ".png")
    getAllGames()

    if(args.gameId):
        getGameOfTheDay(args.gameId)
    else:
        parseMode(args.mode)

def parseMode(mode):
    print("Selected mode : " + mode)
    if mode == "OG":
        getOtherGames()
    if mode == "AG":
        getAllGames()

def getAllGames():
    
    #print("Il y a " + scoreboard["numGames"].text + " matches")
    global scoreboard
    for match in scoreboard["games"]:
        print(match["gameId"] + " " + match["hTeam"]["triCode"] + " vs " + match["vTeam"]["triCode"])


def getTeamStats(teamId):
    for team in standings["league"]["standard"]["teams"]:
        if(team["teamId"] == teamId):
            print(team["confRank"])
            print(team["homeWin"] + "-" + team["homeLoss"])
            print(team["awayWin"] + "-" + team["awayLoss"])

def getOtherGames():
    ids = input("Entrer les codes des matchs de l'affiche principales et des affiches importantes :")
    codes = ids.split()

    global scoreboard
    for match in scoreboard["games"]:
        if match["gameId"] in codes:
            scoreboard["games"].remove(match)
    
    #path = os.path.join(pathlib.Path().absolute(), "templates", "other_games", getPhotoshopFile(len(scoreboard["games"])))
    path = os.path.join(pathlib.Path().absolute(), "templates", "other_games", getPhotoshopFile(1))
    doPhotoshopStuff(path)

def doPhotoshopStuff(path):
    psApp = win32com.client.Dispatch("Photoshop.Application")
    psApp.Open(path)
    doc = psApp.Application.ActiveDocument
    layer = doc.ArtLayers["hteam_rank_game_1"]
    text_of_layer = layer.TextItem
    text_of_layer.contents = "120"
    


def getPhotoshopFile(teamsNumber):
    if teamsNumber == 1 :
        return "one_game.psd"
    if teamsNumber == 2 :
        return "two_games.psd"
    if teamsNumber == 3 :
        return "three_games.psd"
    if teamsNumber == 4 :
        return "four_games.psd"
    if teamsNumber == 5 :
        return "five_games.psd"
    if teamsNumber == 6 :
        return "six_games.psd"
    if teamsNumber == 7 :
        return "seven_games.psd"


    

                
                


    
def getGameOfTheDay(gameId):
    global scoreboard
    global standings

    hTeamId = ""
    vTeamId = ""

    #getTeamsId
    for game in scoreboard["games"]:
        if(game["gameId"] == gameId):
            hTeamId = game["hTeam"]["teamId"]
            vTeamId = game["vTeam"]["teamId"]

    #get hTeam stats
    getTeamStats(hTeamId)
    getTeamStats(vTeamId)
    print("Done")

if __name__ == "__main__":
    main()

