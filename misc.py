from discord.ext import commands


class MiscCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="coolbot")
    async def coolbot(self, ctx):
        await ctx.send("This bot is cool. :)")


def setup(bot):
    bot.add_cog(MiscCommands(bot))
