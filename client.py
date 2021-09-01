from typing import Any, Callable
import discord

class Client(discord.Client):
	hooks: list[Callable[[discord.Message], Any]] = []
	def __init__(self, startup_message, channel_name='bot'):
		super().__init__()
		self.initialized_guilds = 0
		self.started = False
		self.startup_message = startup_message
		self.channel_name = channel_name

	async def on_ready(self):
		print('Logged on as {0}!'.format(self.user))
		self.send_message(self.startup_message)

	async def on_message(self, message: discord.Message):
		# print('Message from {0.author}: {0.content}'.format(message))
		# print(message.author == self.user, message.content == self.startup_message)
		# print(self.guilds)
		if message.author == self.user and message.content == self.startup_message:
			self.initialized_guilds += 1
			
			if self.initialized_guilds == len(self.guilds):
				self.started = True
			
		for f in Client.hooks:
			f(message)
		
	def send_message(self, message, log=False, channel_name=None):
		if channel_name is None:
			channel_name = self.channel_name
		if log:
			print(f"sending message '{message[:100]}'")
		if len(message) > 2000:
			print(f"sending message '{message}'")
			message = message[:2000]
		for server in self.guilds:
			for channel in server.channels:
				if str(channel.type) == 'text' and channel.name == (channel_name):
					self.loop.create_task(channel.send(message))
					break
	def log(self, message):
		self.send_message(message, True, 'log')
