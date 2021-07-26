from discord.ext import commands

class TTT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.moves = [
            ['a1', 'a2', 'a3'],
            ['b1', 'b2', 'b3'], 
            ['c1', 'c2', 'c3']
            ]
        self.moveset = ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3', 'end']
        self.p1 = None
        self.player = self.p1
        self.check_board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
            ]

    def read_board(self, board):
        empty = ':white_circle:'
        p1 = ':x:'
        p2 = ':o:'

        print_str = ''

        for row in board:
            for space in row:
                if space == 0 or space == None:
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
        p = 1 if player==self.p1 else 2
        for row in range(3):
            for element in range(3):
                if self.board[row][element] != p:
                    check_board[row][element] = None
                elif self.board[row][element] == p:
                    check_board[row][element] = p   

        flipped = [
            [check_board[0][2], check_board[1][2], check_board[2][2]],
            [check_board[0][1], check_board[1][1], check_board[2][1]],
            [check_board[0][0], check_board[1][0], check_board[2][0]]
        ]

        if [p, p, p] in check_board or [p, p, p] in flipped:
            return True

        if check_board[0][0] == p:
            if check_board[1][1] == p:
                if check_board[2][2] == p:
                    return True

        if flipped[0][0] == p:
            if flipped[1][1] == p:
                if flipped[2][2] == p:
                    return True

        return False

    def get_element(self, coord):
        for row in self.moves:
            for e in row:
                if e == coord:
                    x = row.index(e)
                    y = self.moves.index(row)

                    return x, y

    @commands.command(name='ttt', aliases=['tictactoe', 'xo'])
    @commands.guild_only()
    async def ttt(self, ctx, p2=None):
        self.p1 = ctx.author
        self.p2 = p2
        guild_id = ctx.guild.id
        guild = self.bot.get_guild(guild_id)

        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
            ]

        if self.p2 == None:
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
            await ctx.send(f'You play with a bot, silly!')
            return
        
        if self.p2 == self.p1:
            await ctx.send('You cant play with yourself!')
            return
        
        await ctx.send(self.read_board(self.board))
        await ctx.send(f'{self.p1.mention} VS {self.p2.mention}')
        
        p1_turn = True
        self.player = self.p1 if p1_turn else self.p2

        def check(m):
            return m.author == self.player and m.content in self.moveset

        while True:
            self.player = self.p1 if p1_turn else self.p2
            await ctx.send(f'{self.player.mention}, your turn! Type in the position you want your marker to be in.')
            await ctx.send('''```
For Eg. your board would look like
a1 | a2 | a3
---+----+---
b1 | b2 | b3
---+----+---
c1 | c2 | c3
            
Type 'end' to end the game.```''')
            play = await self.bot.wait_for('message', check=check)

            if play.content.lower() == 'end':
                await ctx.send(f'{self.player.mention} ended the game! Boohoo')
                break
            
            p = 1 if self.player==self.p1 else 2

            posX, posY = self.get_element(play.content)
            pos = self.board[posY][posX]

            while pos != 0:
                await ctx.send(f'Uh oh! {play.content} is already taken. Please choose a different position')
                
                play = await self.bot.wait_for('message', check=check)
                posX, posY = self.get_element(play.content)
                pos = self.board[posY][posX]

            self.board[posY][posX] = p
            await ctx.send(self.read_board(self.board))

            if self.check_win(self.player):
                await ctx.send(f'{self.player.mention} WON!')
                break

            board1d = []

            for row in self.board:
                for e in row:
                    board1d.append(e)

            if 0 not in board1d:
                await ctx.send(f'Its a DRAW!')
                break  

            p1_turn = not p1_turn

def setup(bot):
    bot.add_cog(TTT(bot))