import requests
import datetime
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
na1_api_url = "https://na1.api.riotgames.com"
americas_api_url = "https://americas.api.riotgames.com"


def get_requests_by_summoner_name(summoner_name: str) -> str:
    ''' Return puuid given summonerName
    '''
    # api_url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name
    path_param = f"/lol/summoner/v4/summoners/by-name/{summoner_name}"
    query = na1_api_url + path_param + '?api_key=' + api_key
    # api_url = api_url + '?api_key=' + api_key

    res = requests.get(query)
    player_info = res.json()
    puuid = player_info['puuid']

    return puuid


def get_matches_by_puuid(puuid: str) -> List:

    path_param = f"/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=6"
    query = americas_api_url + path_param + '&api_key=' + api_key

    res = requests.get(query)
    matches_info = res.json()

    return matches_info


def get_team_info(match_info) -> Dict:
    ''' Return a dictionary containing teamId, win and participants given match_info.
    get_match_by_matchid helper function
    '''
    teams_info = []
    teams = match_info['info']['teams']

    # Initialize team info
    for team in teams:
        team_dict = {"team_id": team['teamId'],
                     "win": team["win"], "participants": []}
        teams_info.append(team_dict)

    # Add participants
    participants = match_info['info']['participants']
    # print(participants)

    for participant in participants:
        summoner_name = participant['summonerName']
        # print(summoner_name)

        if participant['teamId'] == teams_info[0]['team_id']:
            teams_info[0]["participants"].append(summoner_name)
        else:
            teams_info[1]["participants"].append(summoner_name)

    return teams_info


def get_match_by_matchid(matchId: str) -> Dict:
    ''' Return a dictionary containing game_start, game_end, game_duration and teams info
    '''
    path_param = f"/lol/match/v5/matches/{matchId}"
    query = americas_api_url + path_param + "?api_key=" + api_key

    res = requests.get(query)
    match_info = res.json()

    # Organize the data
    game_start = match_info['info']['gameStartTimestamp']//1000
    game_start = datetime.datetime.fromtimestamp(game_start)

    game_end = match_info['info']['gameEndTimestamp']//1000
    game_end = datetime.datetime.fromtimestamp(game_end)

    game_duration = match_info['info']['gameDuration']
    minutes, seconds = divmod(game_duration/1000, 60)

    # print("game_start: " + str(game_start))
    # print("game_duration: " + str(game_duration))
    # print("game_end: " + str(game_end))

    teams = get_team_info(match_info)

    match = {
        "game_start": game_start.strftime("%m/%d/%Y, %H:%M:%S"),
        "game_end": game_end.strftime("%m/%d/%Y, %H:%M:%S"),
        "game_duration": f"{minutes}:{seconds}",
        "teams": teams
    }

    print(match)

    return match
