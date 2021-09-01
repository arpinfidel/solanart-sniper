from scraper import Scraper
from engine import Engine
from repo import Repository
from client import Client
from bot import Bot

import threading
import time

client = Client('starting...', channel_name='aurory-1')
t = threading.Thread(name='', target=lambda: client.run('ODcyMzkzNzE0NzY3NjM4NTQ4.YQpN9Q.udlF_beZtMsxBQTrWMFotGUxEz0'))
t.setDaemon(True)
t.start()
while not client.started:
	time.sleep(0.1)

repo = Repository()
Scraper.set_repo(repo)
bot = Bot('-', client, repo)
engine = Engine(bot, repo)

engine.start()
