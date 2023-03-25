import requests

api_key = "RGAPI-0a43cac4-6ea4-412b-b6e0-f24def93589d"
api_url = "https://na1.api.riotgames.com"


def get_requests_by_summoner_name(summonerName: str):
    api_key = "RGAPI-0a43cac4-6ea4-412b-b6e0-f24def93589d"
    # api_url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name
    path_param = f"/lol/summoner/v4/summoners/by-name/{summonerName}"
    query = api_url + path_param + '?api_key' + api_key
    # api_url = api_url + '?api_key=' + api_key

    res = requests.get(query)
    player_info = res.json()
    puuid = player_info['puuid']

    return player_info


def get_match_by_puuid(puuid: str):
    path_param = f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
    query = api_url + path_param + '?api_key' + api_key

    res = requests.get(query)
    match_info = res.json()

    return match_info
