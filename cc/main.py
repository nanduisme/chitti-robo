import random
from dataclasses import asdict
from typing import Callable

import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from replit import db

from embeds import GeneralEmbeds, CustomCommandEmbeds
from classes import Guild


class Cog(commands.Cog):
    """Custom Commands and Replies!"""

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_guild(id: int):
        if str(id) in db:
            return Guild(**db[str(id)])
        else:
            return Guild(id)

    @staticmethod
    def dump_guild(guild: Guild):
        db[str(guild.id)] = asdict(guild)

    @staticmethod
    def construct_key(key: list):
        return " ".join(map(str, key))

    async def wait_for(
        self,
        check: Callable,
        ctx: Context,
        msg_type: str = "message",
        timeout: int = 60,
    ):
        try:
            response = await self.bot.wait_for(msg_type, timeout=timeout, check=check)
        except Exception:
            await ctx.reply(embed=GeneralEmbeds.timeout(), mention_author=False)
            return
        else:
            return response

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        """Replies to the custom keywords"""

        guild = self.get_guild(message.guild.id)

        if message.author.bot:
            return

        if not guild.is_enabled:
            return

        for keyword in guild.replies:
            if keyword not in guild.active_keys:
                continue

            if " " in keyword and keyword in message.content.lower():
                await message.channel.send(random.choice(guild.replies[keyword]))

            elif keyword in message.content.lower().split():
                await message.channel.send(random.choice(guild.replies[keyword]))

    @commands.group(invoke_without_command=True)
    async def cc(self, ctx: Context):

        """Parent commands for cc command group."""

        await ctx.send("Uh oh! Cant use this command without a subcommand.")

    @cc.command()
    async def enable(self, ctx: Context):

        """Enables custom commands for the whole server."""

        guild = self.get_guild(ctx.guild.id)

        if guild.is_enabled:
            await ctx.send(
                "Custom commands are already enabled for this server, buddy."
            )
        else:
            guild.is_enabled = True
            await ctx.send("Custom commands have been **enabled** for this server")

        self.dump_guild(guild)

    @cc.command()
    async def disable(self, ctx: Context):

        """Disables custom commands for the whole server."""

        guild = self.get_guild(ctx.guild.id)

        if not guild.is_enabled:
            await ctx.send(
                "Custom commands are already disabled for this server, dude."
            )
        else:
            guild.is_enabled = False
            await ctx.send("Custom commands have been **disabled** for this server")

        self.dump_guild(guild)

    @cc.command()
    async def add(self, ctx: Context, *key):

        """Adds a key and a reply to your server."""

        key = self.construct_key(key)
        guild = self.get_guild(ctx.guild.id)

        if len(key) == 0:
            await ctx.send("Enter the keyword for the custom command...")

            key = await self.wait_for(lambda x: x.author == ctx.author, ctx)
            if key is None:
                return

            key = key.content

        if key in guild.replies:
            await ctx.send(embed=CustomCommandEmbeds.Add.key_exists(key))

            response = await self.wait_for(
                lambda m: m.author == ctx.author
                and m.content.lower() in ["yes", "no", "y", "n"],
                ctx,
            )
            if response is None:
                return
            if response.content.lower() in "no":
                await ctx.send(embed=GeneralEmbeds.command_cancelled())
                return

        await ctx.send("What would you like the reply to be?")
        reply = await self.wait_for(lambda m: m.author == ctx.author, ctx)

        if reply is None:
            return

        reply = reply.content

        if key in guild.replies and reply in guild.replies[key]:
            await ctx.send(embed=CustomCommandEmbeds.Add.reply_exists(key, reply))
            return

        await ctx.send(embed=CustomCommandEmbeds.Add.confirm(key, reply))

        confirm = await self.wait_for(
            lambda m: m.author == ctx.author
            and m.content.lower() in ["yes", "no", "y", "n"],
            ctx,
        )

        if confirm is None:
            return

        confirm = confirm.content

        if confirm.lower() in ["no", "n"]:
            await ctx.send(embed=GeneralEmbeds.command_cancelled())
            return

        if key not in guild.replies:
            guild.replies[key] = [reply]
            guild.active_keys.append(key)
        else:
            guild.replies[key].append(reply)

        self.dump_guild(guild)

        await ctx.send(embed=CustomCommandEmbeds.Add.added(key, reply))

    @cc.command()
    async def remove(self, ctx: Context, *key):

        """Removes a reply from a specified key."""

        key = self.construct_key(key)
        guild = self.get_guild(ctx.guild.id)

        if len(key) == 0:
            await ctx.send("Enter the keyword from which you want a reply removed...")

            key = await self.wait_for(lambda m: m.author == ctx.author, ctx)

            if key is None:
                return

            key = key.content

        if key not in guild.replies:
            await ctx.send(embed=CustomCommandEmbeds.Remove.keyword_not_found(key))
            return

        await ctx.send(
            embed=CustomCommandEmbeds.Remove.show_replies(key, guild.replies[key])
        )
        reply_index = await self.wait_for(lambda m: m.author == ctx.author, ctx)

        if reply_index is None:
            return

        reply_index = reply_index.content

        try:
            reply_index = int(reply_index)
            reply_index -= 1
        except Exception:
            await ctx.send(embed=CustomCommandEmbeds.Remove.invalid_index(reply_index))
            return

        if reply_index >= len(guild.replies[key]):
            await ctx.send(embed=CustomCommandEmbeds.Remove.invalid_index(reply_index))
            return

        reply = guild.replies[key][reply_index]
        await ctx.send(embed=CustomCommandEmbeds.Remove.confirm(key, reply))

        response = await self.wait_for(
            lambda m: m.author == ctx.author
            and m.content.lower() in ["yes", "y", "no", "n"],
            ctx,
        )

        if response is None:
            return
        if response.content.lower() in ["n", "no"]:
            await ctx.send(embed=GeneralEmbeds.command_cancelled())
            return

        if len(guild.replies[key]) == 1:
            del guild.replies[key]
        else:
            guild.replies[key].remove(reply)

        self.dump_guild(guild)

        await ctx.send(embed=CustomCommandEmbeds.Remove.removed(key, reply))

    @cc.command()
    async def toggle(self, ctx: Context, *key):

        """Toggles a key and all its replies on or off."""

        key = self.construct_key(key)
        guild = self.get_guild(ctx.guild.id)

        if len(key) == 0:
            await ctx.send("Enter the key you want to toggle on/off.")
            key = await self.wait_for(lambda m: m.author == ctx.author, ctx)

            if key is None:
                return

            key = key.content

        if key not in guild.replies:
            await ctx.send(embed=CustomCommandEmbeds.Toggle.keyword_not_found(key))
            return

        if key in guild.active_keys:
            guild.active_keys.remove(key)
            await ctx.send(embed=CustomCommandEmbeds.Toggle.toggled_off(key))
        else:
            guild.active_keys.append(key)
            await ctx.send(embed=CustomCommandEmbeds.Toggle.toggled_on(key))

    @cc.command(aliases=["list"])
    async def show(self, ctx: Context, *key):

        """Shows list of all the keys and replies."""

        key = self.construct_key(key)
        guild = self.get_guild(ctx.guild.id)

        if len(key) == 0:
            await ctx.send(embed=CustomCommandEmbeds.Show.show_all(guild))

        elif key not in guild.replies:
            await ctx.send(
                embed=CustomCommandEmbeds.Show.key_not_found(key, ctx.prefix)
            )
        else:
            await ctx.send(embed=CustomCommandEmbeds.Show.show_key(key, guild))


def setup(bot):
    bot.add_cog(Cog(bot))
