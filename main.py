from src.bot import mybot

TOKEN = os.environ['TOKEN']

COGS = [
        "src.greetings",
        "src.stats",
        "src.music",
        "src.errors",
        "src.events"
    ]

if __name__ == "__main__":
    for cog in COGS:
        mybot.bot.load_extension(cog)
    mybot.bot.run(TOKEN)
