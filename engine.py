from util import Timer, stack_trace
from scraper import Scraper
from bot import Bot
from repo import Repository
from nft import NFT
from filter import Filter

from typing import List
import threading
import time

class Engine:
	def __init__(self, bot: Bot, repo: Repository) -> None:
		self.bot = bot
		self.repo = repo

	def is_sent(self, nft: NFT):
		return (nft.id, nft.seller_address) in self.repo.sent

	def set_sent(self, nft: NFT):
		self.repo.sent.add((nft.id, nft.seller_address))

	def start(self) -> None:
		lock = threading.RLock()
		buffer:List[NFT] = []
		def scrape():
			while True:
				nfts, err = Scraper.get_nfts()
				if err != None:
					print(err)
					continue
				with lock:
					buffer.extend(nfts)
		t = threading.Thread(name='scraper', target=scrape)
		t.setDaemon(True)
		t.start()
		while True:
			nfts = []
			with lock:
				nfts = buffer
				buffer = []
			for f in self.repo.filters:
				matches = f.match(nfts)
				for n, m in matches:
					if m and not self.is_sent(n):
						self.bot.send_alarm(n, m, f.channel)
						self.set_sent(n)
			# targets = {a: [] for a in self.repo.target_attributes.copy()}
			# for nft in nfts:
			# 	if len(nft.attributes_list) - 5 in self.repo.target_attributecount\
			# 	and not self.is_sent(nft):
			# 		self.bot.send_alarm(nft, channel='aurory-1', trigger=f'attribute count [{len(nft.attributes_list) - 5}]')
			# 		self.set_sent(nft)
			# 	for _, a in enumerate(nft.attributes_list):
			# 		if a == '':
			# 			print(f'this one right here `{nft.attributes}` {nft.name}')
			# 			continue
			# 		if a in self.repo.target_attributes:
			# 			targets[a].append(nft)
			# for a, nfts in targets.items():
			# 	if len(nfts) < 2:
			# 		continue
			# 	nfts = sorted(nfts, key=lambda x: x.price)
			# 	nft = nfts[0]
			# 	if nft.price <= 0.7 * nfts[1].price and not self.is_sent(nft):
			# 		self.bot.send_alarm(nft, channel='aurory-1', next_cheapest=nfts[1], trigger=f'target found [{a}]')
			# 		self.set_sent(nft)