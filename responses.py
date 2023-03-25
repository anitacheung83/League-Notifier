import random
import riot_requests


def get_response(message: str) -> str:

    sommoner_name = "sn"
    p_message = message.lower()

    if p_message == "hello":
        return "Hey there!"

    if message == "roll":
        return str(random.randint(1, 6))

    if p_message == "!help":
        return "`This is a help message that you can modify`"

    if "sn" in p_message:
        return p_message.removeprefix('sn:')

    return "I didn't understand what you wrote. Try typing '!help'."
