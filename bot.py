import os
import discord
import asyncio
from discord import Intents, app_commands
from discord.ext import commands
import responses
from dotenv import load_dotenv

load_dotenv()


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)

        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = os.getenv('TOKEN')
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix="!", intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        try:
            synced = await client.tree.sync()
        except Exception as e:
            print(e)

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    @client.tree.command(name="yellow")
    async def yellow(interaction: discord.Interaction):
        await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command", ephemeral=True)

    @client.tree.command(name="say")
    @app_commands.describe(arg="What should I say?")
    async def say(interaction: discord.Interaction, arg: str):
        await interaction.response.send_message(f"{interaction.user.name} said: `{arg}`")

    @client.tree.command(name="curr")
    @app_commands.describe(summoner_name="Summoner Name")
    async def curr(interaction: discord.Interaction, summoner_name: str):
        curr_game = responses.curr(summoner_name)
        await interaction.response.send_message(curr_game)

    @client.tree.command(name="past")
    @app_commands.describe(summoner_name="Summoner Name")
    async def past(interaction: discord.Interaction, summoner_name: str):
        await interaction.response.defer()
        past_games = responses.past(summoner_name)
        await asyncio.sleep(10)
        await interaction.followup.send(past_games)
        # await interaction.response.send_message(past_games)

    client.run(TOKEN)
