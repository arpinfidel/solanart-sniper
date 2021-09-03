from scraper import Scraper
from engine import Engine
from repo import Repository
from client import Client
from bot import Bot

import threading
import time
import os

from dotenv import load_dotenv
load_dotenv()

client = Client('starting...', channel_name='aurory-1')

repo = Repository()
Scraper.set_repo(repo)
bot = Bot('-', client, repo)
engine = Engine(bot, repo)

t = threading.Thread(name='', target=lambda: engine.start())
t.setDaemon(True)
t.start()

client.run(os.getenv('DISCORD_TOKEN'))