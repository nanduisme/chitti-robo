from typing import ValuesView
import discord
from discord.asset import VALID_AVATAR_FORMATS
from discord.ext import commands

PURPLE = 0x510490

class CommandGroup:
    def __init__(self, title, command, name, commands=[]) -> None:
        self.title = title
        self.name = name
        self.command = command
        self.commands = commands


class Command:
    def __init__(self, group, command, discription, usage, name, output=None, aliases=None):
        self.group = group
        self.command = command
        self.discription = discription
        self.usage = usage
        self.output = output
        self.aliases = aliases
        self.name = name

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='help', invoke_without_command=True)
    async def help(self, ctx, group=None, subcommand=None):
        math = CommandGroup('**🤓 Math**',
                    f'`{ctx.prefix}help math`',
                    'math')
        add = Command(math,
                    'Add',
                    'Adds given numbers and returns the sum.',
                    f'`{ctx.prefix}add <[a b c ...]>`',
                    name='add',
                    output='`a + b + c + ... = (sum)`')
        subtract = Command(math,
                        'Subtract',
                        'Subtracts two given numbers and returns the difference.',
                        f'`{ctx.prefix}subtract <x> <y>`',
                        output='`x - y = (difference)`', 
                        name='subtract')
        mult = Command(math,
                    'Multiply',
                    'Mulitplies given numbers and returns the product.',
                    f'`{ctx.prefix}mult <[a b c ...]>`',
                    output='`a * b * c * ... = (product)`', 
                    name='mult')
        div = Command(math,
                    'Divide',
                    'Divides two given numbers and returns the quotient.',
                    f'`{ctx.prefix}div <x> <y>`',
                    output='`x / y = (quotient)`', 
                        name='div')
        mean = Command(math,
                    'Mean',
                    'Gives the arithmetic mean or average of a list of given numbers.',
                    f'`{ctx.prefix}mean <[a b c ...]>`',
                    output='`The arithmetical mean of [a b c ...] is (mean)`',
                    name='mean')
        median = Command(math,
                        'Median',
                        'Gives the median of a list of given numbers.',
                        f'`{ctx.prefix}median <[a b c ...]>`',
                        output='`The median of [a b c ...] is (median)`',
                        name='median')
        mode = Command(math,
                    'Mode',
                    'Gives the arithemetic mode of given list of numbers.',
                    f'`{ctx.prefix}mode <[a b c ...]>`',
                    output='`The mode of [a b c ...] is (mode) occuring at a total of (count) times.`', name='mode')

        listener = CommandGroup('**👂 Listener**',
                                f'`{ctx.prefix}help listener`',
                                'listener')
        list = Command(listener, 'List',
                    'Shows a list of all the keys and replies on this server.', f'`{ctx.prefix}listener list`', name='list')
        ladd = Command(listener, 'Add',
                    'Add a reply to an existing key or create a new key.', f'`{ctx.prefix}listener add |key|`', name='add')
        toggle = Command(listener, 'Toggle Key',
                        'Toggles a key on or off for the server.', f'`{ctx.prefix}listener toggle |key|`', name='toggle')
        enable = Command(listener, 'Enable Listener',
                        'Enables all listeneres for this server.', f'`{ctx.prefix}listener enable`', name='enable')
        disable = Command(listener, 'Disable listener',
                        'Disables all listeners for this server.', f'`{ctx.prefix}listener enable`', name='disable')
        remove = Command(listener, 'Remove Reply',
                        'Removes specific replies from keys.', f'`{ctx.prefix}listener remove |key|`', name='remove')

        fun = CommandGroup('**🎮 Fun**',
                        f'`{ctx.prefix}help fun`',
                        'fun')
        xo = Command(fun, 'TicTacToe', 'Play TicTacToe with another player!',
                    f'`{ctx.prefix}xo <@player 2>`', aliases=['`ttt`', '`tictactoe`'], name='xo')
        rps = Command(fun, 'Rock Paper Scissors',
                    'I play a game of rock paper scissors with you!', f'`{ctx.prefix}rps`', name='rps')

        misc = CommandGroup('**✨ Misc**',
                            f'`{ctx.prefix}help misc`',
                            'misc')
        coolbot = Command(misc, 'Cool Bot 😎',
                        'Find out for yourself. ;)', f'`{ctx.prefix}coolbot`', name='coolbot')

        tier = CommandGroup('**🎖 Messaging Tiers**', f'`{ctx.prefix}help tier`', 'tier')
        deduct = Command(tier, 'Deduct Point', 'Deducts messaging points from a user. (Admins Only)', f'`{ctx.prefix}tier deduct |mention member|`', 'deduct')
        score = Command(tier, 'Messaging Score', 'Shows score and rank of a person or yourself in this server.', f'`{ctx.prefix}tier score |mention member|`', 'score')
        exclude = Command(tier, 'Exclude Channel', 'Excludes said channel from adding up your scores. Useful to nerf spam channels etc.', f'`{ctx.prefix}tier exclude |#channel|`', 'exclude')
        excluded = Command(tier, 'Excluded Channels List', 'Shows list of all the channels excluded from adding scores.', f'`{ctx.prefix}tier excluded`', 'excluded', aliases=['`list`', '`leaderboard`'])   
        include = Command(tier, 'Iclude Channel', 'Includes said channel to add scores.', f'`{ctx.prefix}tier include |#channel|`', 'include')
        leaderboard = Command(tier, 'Leaderboard', 'Shows the leaderboard of messaging scores for this server', f'`{ctx.prefix}leaderboard`', 'leaderboard', aliases=['`lb`', '`leaderboard`'])

        groups = [math, listener, tier, fun, misc]
        group_names = [group.name for group in groups]

        math.commands = [add, subtract, mult, div, mean, median, mode]
        listener.commands = [enable, disable, list, ladd, toggle, remove]
        tier.commands = [leaderboard, score, include, exclude, excluded, deduct]
        fun.commands = [xo, rps]
        misc.commands = [coolbot]

        all_command_names = []
        for g in groups:
            for c in g.commands:
                all_command_names.append(c.name)
        if group == None:
            help = discord.Embed(title='Chitti Robo commands list',
                                 description='Help command for this bot.', color=PURPLE)
            for group in groups:
                help.add_field(name=group.title,
                               value=group.command, inline=True)
            help.set_footer(
                text='Dm Nandu#8677 for suggestions on this bot. :)')
            await ctx.reply(embed=help, mention_author=False)

        elif group in group_names and subcommand == None:
            help = discord.Embed(title=f'{group.capitalize()} commands',
                                 description=f'List of {group} commands for this bot.', color=PURPLE)
            group = groups[group_names.index(group)]
            for c in group.commands:
                help.add_field(name=c.command, value=c.usage, inline=True)
            help.set_footer(
                text=f'Use `{ctx.prefix}help {group.name} <command>` for more info on each command.\nSyntax: <required> [infinite list of numbers...] |optional|')
            await ctx.reply(embed=help, mention_author=False)

        elif group in group_names and subcommand in all_command_names:
            command = None
            for g in groups:
                for c in g.commands:
                    if c.name == subcommand and group == g.name:
                        command = c
                        
            if command == None:
                await ctx.reply(f'Subcommand "{subcommand}" not found in group "{group}".')
                return

            help = discord.Embed(title = command.command, color=PURPLE, description=command.discription)
            help.add_field(name='Usage', value=command.usage)
            if command.aliases != None:
                aliases = ''
                for a in command.aliases:
                    aliases+=(a+'   ')
                help.add_field(name='Aliases', value=aliases)
            if command.output != None:
                help.add_field(name='Output', value=command.output)

            help.set_footer(text='Syntax: <required> [infinite list of numbers...] |optional|')
            await ctx.reply(embed=help)

def setup(bot):
    bot.add_cog(Cog(bot))
