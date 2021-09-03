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
t = threading.Thread(name='', target=lambda: client.run(os.getenv('DISCORD_TOKEN')))
t.setDaemon(True)
t.start()
while not client.started:
	time.sleep(0.1)

repo = Repository()
Scraper.set_repo(repo)
bot = Bot('-', client, repo)
engine = Engine(bot, repo)

engine.start()
