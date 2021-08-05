import discord
from discord.ext import commands


class RPScog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='rps')
    async def rps(self, ctx):
        p1 = ctx.author
        channel = ctx.channel

        await ctx.send('reply `a` if you would like to play alone')

        def check(m):
            return m.content == 'a' and m.channel == channel and m.author == ctx.author

        await self.bot.wait_for('message', check=check)

        await ctx.send(f'So, it is {p1.mention} vs ME! Let the Game Begin!')

        p1_score = 0
        ai_score = 0

        def play_check(m):
            return m.content in ['rock', 'paper', 'scissors'] and m.channel == channel and m.author == p1

        import rps.WinLogic as wl

        while True:
            await ctx.send(f'{p1.mention} type your choice! rock, paper or scissors.')

            pchoice = await self.bot.wait_for('message', check=play_check)
            randchoice = wl.ai_choice()
            outcome = wl.win_logic(randchoice, pchoice.content.lower())[0]

            if outcome == 'w':
                p1_score += 1
                await ctx.send(f'{pchoice.content.upper()}({p1.mention}) **VS** {randchoice.upper()}(BOT)')
                await ctx.send('YOU SCORED! ')
                await ctx.send(f'''`SCORE: {p1_score}(YOU) - {ai_score}(BOT)`''')

            elif outcome == 'l':
                ai_score += 1
                await ctx.send(f'{pchoice.content.upper()}({p1.mention}) **VS** {randchoice.upper()}(BOT))')
                await ctx.send('BOT SCORED! ')
                await ctx.send(f'''`SCORE: {p1_score}(YOU) - {ai_score}(BOT)`''')

            else:
                await ctx.send(f'{pchoice.content.upper()}({p1.mention}) **VS** {randchoice.upper()}(BOT))')
                await ctx.send('IT WAS A DRAW! ')
                await ctx.send(f'''`SCORE: {p1_score}(YOU) - {ai_score}(BOT)`''')

            if ai_score == 5 or p1_score == 5:
                winner = None
                if ai_score > p1_score:
                    winner = 'Bot'
                else:
                    winner = 'You'
                await ctx.send(f'GAME OVER! {winner} won! Final scores: {p1_score} - {ai_score}')
                break


def setup(bot):
    bot.add_cog(RPScog(bot))
