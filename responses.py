import random
import urllib.parse
import riot_requests


def get_response(message: str) -> str:

    p_message = message.lower()

    if p_message == "hello":
        return "Hey there!"

    if p_message == "!help":
        return "`This is a help message that you can modify`"

    if "sn" in p_message:
        summoner_name = p_message.removeprefix('sn:')
        print(summoner_name)
        encoded_summoner_name = urllib.parse.quote(summoner_name)
        print(encoded_summoner_name)
        return riot_requests.get_requests_by_summoner_name(encoded_summoner_name)

    return "I didn't understand what you wrote. Try typing '!help'."
