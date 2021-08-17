from discord.ext import commands

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if "suggestions" in message.channel.name and not message.author.bot:
            green = '🟢'
            await message.add_reaction(green)
            red = '🔴'
            await message.add_reaction(red)            

def setup(bot):
    bot.add_cog(Cog(bot))