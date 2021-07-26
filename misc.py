from discord.ext import commands

class MiscCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='coolbot')
    async def coolbot(self, ctx):
        await ctx.send('This bot is cool. :)')

    @commands.command(name='help')
    async def help(self, ctx):
        await ctx.send('''List of all the commands I know: ```
- $help
    -Displays this message.

- $coolbot
    -Find out for yourself. ;)

- $rps
    -I play a game of rock paper scissors with you!
    
- $xo |mention player 2|
    -Plays a game of tictactoe with mentioned player 2.
    
- $math
    -A parent command for a few simple Math command. Use command for more info.
    
- $listener 
    -A parent command for some commands which listens to specified keywords in messages and responds with designated replies. Use command for more info.
    
Dm Nandu#8677 if you have any suggestions. :)```''')

def setup(bot):
    bot.add_cog(MiscCommands(bot))