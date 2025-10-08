import os
from dotenv import load_dotenv
import threading

from app.discord.bot import discord_bot
from app.web.webserver import run_flask



if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("discord_bot_token")
    threading.Thread(target=run_flask).start()
    discord_bot.run(token)