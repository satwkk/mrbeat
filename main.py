import os
from bot import mybot
TOKEN = os.environ['TOKEN']

COGS = [
        "greetings",
        "stats",
        "music",
        "errors"
    ]

if __name__ == "__main__":
    for cog in COGS:
        mybot.bot.load_extension(cog)
    mybot.bot.run(TOKEN)

