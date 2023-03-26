from typing import List, Dict
import random
import urllib.parse
import riot_requests


def parse_matches(matches: List, summoner_name: str) -> str:
    matches_str = f"{summoner_name}: \n\n"
    i = 1
    for match in matches:
        # print(match)
        match_info = riot_requests.get_match_by_matchid(match)
        matches_str += match_data_to_str(match_info, i)
        i += 1

    return matches_str


def match_data_to_str(match_info: Dict, game_id: int) -> str:
    game_id = f"Game: {game_id}:\n"
    start_time = f"Start Time: {match_info['game_start']} \n"
    end_time = f"End Time: {match_info['game_end']}\n"
    duration = f"Duration: {match_info['game_duration']}\n"
    team0 = f"Team {match_info['teams'][0]['team_id']}: {match_info['teams'][0]['participants']}, Win: {match_info['teams'][0]['win']}\n"
    team1 = f"Team {match_info['teams'][1]['team_id']}: {match_info['teams'][1]['participants']}, Win: {match_info['teams'][1]['win']}\n\n"
    print(game_id + start_time + end_time + duration + team0 + team1)

    return game_id + start_time + end_time + duration + team0 + team1


def get_response(message: str) -> str:

    p_message = message.lower()

    if p_message == "hello":
        return "Hey there!"

    if p_message == "!help":
        return "`This is a help message that you can modify`"

    if "sn" in p_message:
        summoner_name = p_message.removeprefix('sn:')  # Remove prefix 'sn'
        encoded_summoner_name = urllib.parse.quote(
            summoner_name)  # url encode summoner_name
        puuid = riot_requests.get_requests_by_summoner_name(
            encoded_summoner_name)  # Get puuid
        matches = riot_requests.get_matches_by_puuid(
            puuid)  # Return a lists of the last 20 games

        matches_info = parse_matches(matches, summoner_name)
        return matches_info

    return "I didn't understand what you wrote. Try typing '!help'."
