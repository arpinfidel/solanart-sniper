from scraper import Scraper
from client import Client
from nft import NFT
from repo import Repository
from filter import Filter

import os

class Bot:
	def __init__(self, prefix: str, client: Client, repo: Repository):
		self.client = client
		self.prefix = prefix
		self.repo = repo

		self.client.hooks.append(lambda m: self.handle_addattribute(m.content, str(m.channel)))
		self.client.hooks.append(lambda m: self.handle_addattributecount(m.content, str(m.channel)))
		self.client.hooks.append(lambda m: self.handle_list(m.content, str(m.channel)))
		self.client.hooks.append(lambda m: self.handle_removeattribute(m.content, str(m.channel)))
		self.client.hooks.append(lambda m: self.handle_setcollection(m.content, str(m.channel)))

	def send_alarm(self, nft: NFT, channel='bot', next_cheapest: NFT=None, trigger=None):
		self.client.send_message(
			'@everyone\n'+
			f'https://solanart.io/search/?token={nft.token_add}\n'+
			'```'
			f'{nft.name}\n'+
			f'price  : {nft.price} sol\n'+
			f'{f"next: {next_cheapest.price}" if next_cheapest is not None else ""}\n'+
			f'{f"trigger: {trigger}" if trigger is not None else ""}\n'+
			f'attr : {[a for a in nft.attributes_list]}\n'+
			f'count: {len(nft.attributes_list) - 5}\n'+
			f'\n'+
			'```'
		, log=True, channel_name=channel)
	# def send_alarm(self, nft:NFT, match:Filter.Match, channel:str = 'bot'):
	# 	self.client.send_message(
	# 		'@testing\n'+
	# 		f'https://solanart.io/search/?token={nft.token_add}\n'+
	# 		'```'
	# 		f'{nft.name}\n'+
	# 		f'price  : {nft.price} sol\n'+
	# 		f'{f"next: {nft.price/match.price_threshold[1]}" if match.price_threshold is not None else ""}\n'+
	# 		f'trigger: {match.as_dict()}\n'+
	# 		f'attr : {[a for a in nft.attributes_list]}\n'+
	# 		f'count: {len(nft.attributes_list) - 5}\n'+
	# 		f'\n'+
	# 		'```'
	# 	, log=True, channel_name=channel)

	def handle_addattribute(self, message: str, channel: str):
		message = message.split('|')
		if message[0] != self.prefix+'addattribute':
			return
		if len(message) < 2:
			self.client.send_message('invalid command syntax', channel_name=channel)
			return
		for m in message[1:]:
			self.repo.target_attributes.add(m)
		self.client.send_message(f'successfully added `{message[1:]}`', channel_name=channel)

	def handle_addattributecount(self, message: str, channel: str):
		message = message.split('|')
		if message[0] != self.prefix+'addattributecount':
			return
		if len(message) != 2:
			self.client.send_message('invalid command syntax', channel_name=channel)
			return
		try:
			message[1] = int(message[1])
		except:
			self.client.send_message('invalid command syntax', channel_name=channel)
			return
		self.repo.target_attributecount.add(message[1])
		self.client.send_message(f'successfully added `{message[1]}`', channel_name=channel)

	def handle_removeattribute(self, message: str, channel: str):
		message = message.split('|')
		if message[0] != self.prefix+'removeattribute':
			return
		if len(message) != 2:
			self.client.send_message('invalid command syntax', channel_name=channel)
			return
		try:
			self.repo.target_attributes.remove(message[1])
		except KeyError:
			self.client.send_message('attribute not found')
			return
		self.client.send_message(f'successfully removed `{message[1]}`', channel_name=channel)
		
	def handle_list(self, message: str, channel: str):
		message = message.split('|')
		if message[0] != self.prefix+'list':
			return
		if len(message) > 1:
			self.client.send_message('invalid command syntax', channel_name=channel)
			return
		
		attributes = sorted(list(self.repo.target_attributes.copy()))
		header = \
			f'instance-{os.getenv("ID")}\n'+\
			f'collection: {self.repo.get_collection()}\n'+\
			f'\n'+\
			f'attr count alarm: {sorted(list(self.repo.target_attributecount.copy()))}\n'+\
			f'\n'+\
			f'total attributes: {len(attributes)}\n'+\
			''
		
		if len(attributes) == 0:
			self.client.send_message(f'```\n{header}```', channel_name=channel)
			return

		for i in range(0, len(attributes), 20):
			message = '```\n'
			if i == 0:
				message += f'{header}'
			for j, a in enumerate(attributes[i:i+20]):
				message += f'{i+j+1:2}. {a}\n'
			message += '```'
			self.client.send_message(message, channel_name=channel)
		
	def handle_setcollection(self, message: str, channel: str):
		message = message.split('|')
		if message[0] != self.prefix+'setcollection':
			return
		if len(message) != 2:
			self.client.send_message('invalid command syntax', channel_name=channel)
			return
		old_coll = self.repo.get_collection()
		self.repo.set_collection(message[1])
		for i in range(3):
			_, err = Scraper.get_nfts()
			if err is None:
				break
			else:
				print(err)
		else:
			self.client.send_message('set collection failed. reverted to previous collection')
			self.repo.set_collection(old_coll)
			return
		self.client.send_message('successfully set collection to '+message[1], channel_name=channel)
