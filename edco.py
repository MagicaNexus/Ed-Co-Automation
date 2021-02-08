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

    #parser.add_argument('--mode', "-M", help='GOD, OG, AG')
    #parser.add_argument('--gameId', "-ID", help='Optionnel - L\'id du match pour le Game Of The Day')
    parser.add_argument('--date', "-D", help='Optionnel - Tu dois remplir la date voulue sur la forme YYYYMMDD (ex : 20210521) - Defaut : today')

    args = parser.parse_args()
    if args.date and len(args.date) == 8:
        global today
        today = args.date

    global scoreboard
    global standings

    standings = requests.get("http://data.nba.net/prod/v1/current/standings_all.json").json()
    scoreboard = requests.get("http://data.nba.net/10s/prod/v1/"+today+"/scoreboard.json").json()

    
    getAllGames()
    getOtherGames()

    #if(args.gameId):
        #getGameOfTheDay(args.gameId)
    #else:
        #parseMode(args.mode)



def getAllGames():
    global scoreboard
    print("Il y a " + str(scoreboard["numGames"]) + " matches : ")
    
    for match in scoreboard["games"]:
        print(match["gameId"] + " " + match["hTeam"]["triCode"] + " vs " + match["vTeam"]["triCode"])
    
    print("")

def getOtherGames():
    ids = input("Entrer les codes des matchs de l'affiche principales et des affiches importantes avec un espace entre chaque code : ")
    codes = ids.split()

    global scoreboard

    for match in scoreboard["games"]:
        if match["gameId"] in codes:
            scoreboard["games"].remove(match)
    
    path = os.path.join(pathlib.Path().absolute(), "templates", "other_games", getPhotoshopFile(len(scoreboard["games"])))
    doPhotoshopStuff(path)

def doPhotoshopStuff(path):
    print("Ouveture de Photoshop")
    psApp = win32com.client.Dispatch("Photoshop.Application")
    psApp.Open(path)
    doc = psApp.Application.ActiveDocument
    print("Photoshop est ouvert")
    print("")

    global scoreboard
    global standings

    teams = standings["league"]["standard"]["teams"]

    for match in scoreboard["games"]:
        index = scoreboard["games"].index(match) + 1
        rank_domicile = doc.ArtLayers["hteam_rank_game_" + str(index)]
        rank_exterieur = doc.ArtLayers["vteam_rank_game_" + str(index)]
        vd_domicile = doc.ArtLayers["hteam_vd_game_" + str(index)]
        vd_exterieur = doc.ArtLayers["vteam_vd_game_" + str(index)]

        for team in teams:
            if str(match["hTeam"]["teamId"]) == str(team["teamId"]):
                vd_domicile_textview = vd_domicile.TextItem
                vd_domicile_textview.contents = str(team["homeWin"] + "-" + team["homeLoss"])
                rank_domicile_textview = rank_domicile.TextItem
                rank_domicile_textview.contents = str(teams.index(team) + 1)
                

            if match["vTeam"]["teamId"] == team["teamId"]:
                vd_exterieur_textview = vd_exterieur.TextItem
                vd_exterieur_textview.contents = str(team["awayWin"] + "-" + team["awayLoss"])
                rank_exterieur_textview = rank_exterieur.TextItem
                rank_exterieur_textview.contents = str(teams.index(team) + 1)
        
        print("Modification OK ! Game " + str(index) + " is " + match["hTeam"]["triCode"] + " vs " + match["vTeam"]["triCode"])

    print("Fin du programme")


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

































def parseMode(mode):
    print("Selected mode : " + mode)
    if mode == "OG":
        getOtherGames()
    if mode == "AG":
        getAllGames()                       

def getTeamStats(teamId):
    for team in standings["league"]["standard"]["teams"]:
        if(team["teamId"] == teamId):
            print(team["confRank"])
            print(team["homeWin"] + "-" + team["homeLoss"])
            print(team["awayWin"] + "-" + team["awayLoss"])
    
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


def updateLogos():
    global standings
    base_path = "nba_logos"
    for team in standings["league"]["standard"]["teams"]:
        print("http://i.cdn.turner.com/nba/nba/.element/img/1.0/teamsites/logos/teamlogos_500x500/"+team["teamSitesOnly"]["teamTricode"]+".png")
        urllib.request.urlretrieve("http://i.cdn.turner.com/nba/nba/.element/img/1.0/teamsites/logos/teamlogos_500x500/"+team["teamSitesOnly"]["teamTricode"].lower()+".png", base_path + team["teamSitesOnly"]["teamTricode"] + ".png")

if __name__ == "__main__":
    main()

