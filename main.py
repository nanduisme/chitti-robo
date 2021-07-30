import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

def get_prefix(bot, message):
	prefixes = ['do ', '$', 'chitti ']

	if not message.guild:
		return '$'

	return commands.when_mentioned_or(*prefixes)(bot, message)

initial_extensions = ['misc', 'rps.main', 'ttt.main', 'listener.listener', 'mth.math', 'help', 'ranking.ranking']

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=get_prefix, description="Just Chillin'!", intents=intents)
bot.remove_command('help')

if __name__ == "__main__":
	for extension in initial_extensions:
		bot.load_extension(extension)

@bot.event
async def on_ready():
	print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

	await bot.change_presence(activity=discord.Game(name='$help', type=1, url=''))
	print('Successfully logged in and booted...')

keep_alive()

bot.run(os.environ['TOKEN'], bot=True, reconnect=True)
