# Import all necessary libraries.

import os  # For reading Token.
import discord  # Discord python library.
from discord.ext import commands  # Commands submodule for dealing w commands.
from keep_alive import keep_alive  # To keep the bot alive and not shut down.

# Function that recognizes and returns prefixes when metioned by a user.
def get_prefix(bot, message):
    # All the prefixes recognized by Chitti.
    prefixes = ["do ", "$", "chitti ", "/"]

    if not message.guild:
        return "$"

    return commands.when_mentioned_or(*prefixes)(bot, message)


# All the extenstions or cogs to be loaded into Chitti.
initial_extensions = [
    "misc",
    "rps.main",
    "ttt.main",
    "cc.main",
    "mth.main",
    "help",
    "ranking.ranking",
    "ask.ask",
    "suggestion_react.react",
]

intents = discord.Intents.default()
intents.members = True

# Creating a bot instance.
bot = commands.Bot(
    command_prefix=get_prefix, description="Just Chillin'!", intents=intents
)
bot.remove_command(
    "help"
)  # Removing default help command to implement personalized help command. See /help.py.

# Loads all the extentions from list initial_extensions.
if __name__ == "__main__":
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event  # Checks for an event in the bot. In this case, Checks when the bot is online.
async def on_ready():
    print(
        f"\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n"
    )
    await bot.change_presence(
        activity=discord.Game(name="$help", type=1, url="")
    )  # Sets status for Chitti
    print("Successfully logged in and booted...")

    # All the print statements above are for developer convenience


# Calls keep_alive function to keep the bot alive. Obviously.
keep_alive()

import json
from replit import db
with open('cc.json', 'w') as f:
    data = json.load(f)
    for key in data:
        db[key] = data[key]

# Runs the bot instance
bot.run(
    os.environ[
        "TOKEN"
    ],  # Extracts Bot token stored in replit. (Hosting website is Replit)
    bot=True,
    reconnect=True,
)
