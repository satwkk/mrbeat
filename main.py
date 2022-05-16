from src.bot import MrBeat

TOKEN = ""

COGS = [
        "src.greetings",
        "src.stats",
        "src.music",
        "src.errors",
        "src.events"
    ]

if __name__ == "__main__":
    mrbeat = MrBeat()
    for cog in COGS:
        mrbeat.load_extension(cog)
    mrbeat.run(TOKEN)
