import os
from os.path import dirname, join
import dotenv
from src.bot import mybot
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get("TOKEN")

if __name__ == "__main__":
    mybot.bot.run(TOKEN)
