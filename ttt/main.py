from discord.ext import commands
import discord

PURPLE = 0x510490

class TTT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.moves = [
            ['a1', 'a2', 'a3'],
            ['b1', 'b2', 'b3'],
            ['c1', 'c2', 'c3']
        ]
        self.moveset = ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3']
        self.p1 = None
        self.player = self.p1
        self.check_board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

    def read_board(self, board):
        empty = ':black_square_button:'
        p1 = ':negative_squared_cross_mark:'
        p2 = ':o2:'

        print_str = ''

        for row in board:
            for space in row:
                if space == 0 or space is None:
                    space = empty
                elif space == 1:
                    space = p1
                elif space == 2:
                    space = p2

                print_str += space

            print_str += '\n'

        return print_str

    def check_win(self, player):
        check_board = self.check_board
        p = 1 if player == self.p1 else 2
        for row in range(3):
            for element in range(3):
                check_board[row][element] = None if self.board[row][element] != p else p
        flipped = [
            [check_board[0][2], check_board[1][2], check_board[2][2]],
            [check_board[0][1], check_board[1][1], check_board[2][1]],
            [check_board[0][0], check_board[1][0], check_board[2][0]]
        ]

        if [p, p, p] in check_board or [p, p, p] in flipped:
            return True

        if (
            check_board[0][0] == p
            and check_board[1][1] == p
            and check_board[2][2] == p
        ):
            return True

        if flipped[0][0] == p and flipped[1][1] == p and flipped[2][2] == p:
            return True

        return False

    def get_element(self, coord):
        for row in self.moves:
            for e in row:
                if e == coord:
                    x = row.index(e)
                    y = self.moves.index(row)

                    return x, y

    def get_grid(self):
        pass

    @commands.command(name='ttt', aliases=['tictactoe', 'xo'])
    @commands.guild_only()
    async def ttt(self, ctx, p2=None):  # sourcery no-metrics
        self.p1 = ctx.author
        self.p2 = p2
        guild_id = ctx.guild.id
        guild = self.bot.get_guild(guild_id)

        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        if self.p2 is None:
            await ctx.send('Please mention Player 2. For Eg: `$xo @mark`')
            return

        p2id = self.p2.replace('<', '')
        p2id = p2id.replace('>', '')
        p2id = p2id.replace('@', '')
        p2id = p2id.replace('!', '')

        self.p1 = guild.get_member(self.p1.id)

        try:
            self.p2 = guild.get_member(int(p2id))
        except:
            await ctx.send(f'Member {self.p2} not found on server')
            return

        if self.p2.bot:
            bot_embed = discord.Embed(title='Oopsie!', description='You cant play with a bot man... bots are pretty dumb.', color=PURPLE)
            bot_embed.set_footer(text='LOL lonely ass.')
            await ctx.reply(embed=bot_embed, mention_author=False)
            return

        if self.p2 == self.p1:
            self_embed = discord.Embed(title='Oopsie!', description='You cant play with yourself, silly!', color=PURPLE)
            self_embed.set_footer(text='LOL lonely ass.')
            await ctx.reply(embed=self_embed, mention_author=False)
            return

        p1_turn = True
        self.player = self.p1 if p1_turn else self.p2

            
        def play_check(m):
            return m.content.lower() in (self.moveset + ['help', 'end']) and m.author == self.player

        while True:
            timeout_embed = discord.Embed(title='Aw Man :(', description=f'{self.player.display_name} didnt respond in time :/. GAME OVER.', color=PURPLE)

            self.player = self.p1 if p1_turn else self.p2
            embed = discord.Embed(
                title=f'{self.p1.display_name} VS {self.p2.display_name}', 
                description=f'{self.player.mention}. Its your turn \n\n'+self.read_board(self.board) + f'\n\n`Type in the position you want your marker on, {self.player.display_name}.`', 
                color=PURPLE
                )
            embed.set_footer(text=f'Type in "help" for showing the grid of posistions and "end" to end the game.')

            await ctx.send(embed=embed)

            while True:
                try:
                    play = await self.bot.wait_for('message', check=play_check, timeout=30)
                except:
                    await ctx.send(embed=timeout_embed)
                    return

                if play.content.lower() != 'help':
                    break

                grid = '''```
a1 | a2 | a3
------------
b1 | b2 | b3
------------
c1 | c2 | c3```'''
                help_embed = discord.Embed(title='THE GRID', description=grid, color=PURPLE)
                help_embed.set_footer(text=f'Type in "help" for this message and "end" to end the game.\nType in the position you want your marker on, {self.player.display_name}.')
                await ctx.send(embed=help_embed)
                
            if play.content.lower() == 'end':
                end_embed = discord.Embed(title='Game Ended :/', description=f'{self.player.mention} ended the game! Boohoo', color=PURPLE)
                await ctx.send(embed=end_embed)

                break

            p = 1 if self.player == self.p1 else 2

            posX, posY = self.get_element(play.content)
            pos = self.board[posY][posX]

            while pos != 0:
                error_embed = discord.Embed(title='Uh oh :/', description=f'Uh oh! {play.content} is already taken. Please choose a different position', color=PURPLE)
                await ctx.send(embed=error_embed)

                try:
                    play = await self.bot.wait_for('message', check=play_check, timeout=30)
                except:
                    await ctx.send(embed=timeout_embed)
                    return

                posX, posY = self.get_element(play.content)
                pos = self.board[posY][posX]

            self.board[posY][posX] = p

            if self.check_win(self.player):
                win_embed = discord.Embed(title='YOU WON!', description=f'{self.player.mention} WON THE GAME!! GG!!\n'+self.read_board(self.board), color=PURPLE)
                await ctx.send(embed=win_embed)
                break

            board1d = []

            for row in self.board:
                for e in row:
                    board1d.append(e)

            if 0 not in board1d:
                draw_embed = discord.Embed(title='ITS A DRAW!', description='GG guys! It was a Draw!!\n'+self.read_board(self.board), color=PURPLE)
                await ctx.send(embed=draw_embed)
                break

            p1_turn = not p1_turn


def setup(bot):
    bot.add_cog(TTT(bot))
