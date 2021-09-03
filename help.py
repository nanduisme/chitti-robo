import json

import discord
from discord.ext import commands
from discord.ext.commands.context import Context


class Cog(commands.Cog):

    '''Help Cog for chitti'''

    def __init__(self, bot):
        self.bot = bot
        with open("help.json", "r") as file:
            self.data = json.load(file)

    @commands.command(aliases=['h'])
    async def help(self, ctx: Context, command: str = None):
        if command is None or command not in self.data["commands"]:
            embed = discord.Embed(
                title = 'Help command for chitti'.title(),
                description = f'Enter `{ctx.prefix}help <command>` (without "<>") for more info on the command.',
                color=0xB26EfA
            )
            for group in self.data["groups"]:
                embed.add_field(
                    name = group,
                    value= ''.join(f"`{c}` " for c in self.data["groups"][group]),
                    inline = False
                )

        else:
            embed = discord.Embed(
                title = f'Help: {command}',
                colour =0xB26EfA
            )
            embed.add_field(
                name = 'Syntax',
                value=f'`{ctx.prefix}{command} {self.data["commands"][command]["syntax"]}`',
                inline = False
            )
            embed.add_field(
                name="Description",
                value=self.data['commands'][command]['help'],
                inline = False
            )
            if self.data['commands'][command]['aliases'] != []:
                embed.add_field(
                    name = 'Aliases',
                    value=''.join(f'`{alias}`, ' for alias in self.data['commands'][command]['aliases']),
                    inline = False
                )

            embed.set_footer(
                text='DO NOT use `<>`, `[]` or `...` when using the command.\n<> = required, [] = optional, ... = infinitly continues'
            )

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Cog(bot))