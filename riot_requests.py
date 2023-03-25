import requests


def get_requests(summonerName: str):
    api_key = "RGAPI-0a43cac4-6ea4-412b-b6e0-f24def93589d"
    api_url = "https://americas.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName
    api_url = api_url + '?api_key=' + api_key

    res = requests.get(api_url)
    player_info = res.json()

    return player_info
