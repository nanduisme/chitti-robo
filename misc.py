from discord.ext import commands


class MiscCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="coolbot")
    async def coolbot(self, ctx):
        await ctx.send("This bot is cool. :)")

    @commands.command()
    async def feedback(self, ctx: commands.context.Context, *feedback):

        """Get feedback from the users"""

        if len(feedback) == 0:
            await ctx.send(
                "❌ Oops! I think you forgot to give your feedback!", delete_after=5
            )
            return

        dev = self.bot.get_user(591078175778537512)
        feedback = "".join(f"{word} " for word in feedback)

        await dev.send(f"{ctx.author.mention} says: " + feedback)
        await ctx.reply(
            "Team Chitti thanks you for your valuable feedback! 😄", delete_after=30
        )


def setup(bot):
    bot.add_cog(MiscCommands(bot))
