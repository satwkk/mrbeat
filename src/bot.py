import discord
from discord.ext import commands

CMD_PREFIX = "-"

class Bot():
    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix=CMD_PREFIX, intents=intents)

    def __init__(self):
        pass

mybot = Bot()
