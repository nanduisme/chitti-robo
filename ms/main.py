from dataclasses import asdict

import discord
from replit import db
from discord.ext import commands, tasks
from discord.ext.commands.context import Context

from classes import Guild, Member
from embeds import MessagingScoreEmbeds


class Cog(commands.Cog):

    """Messaging scores"""

    def __init__(self, bot):
        self.bot = bot

    # METHODS

    # Decode mention
    @staticmethod
    def decode_mention(mention: str) -> int:
        mention = mention.replace("<", "")
        mention = mention.replace("@", "")
        mention = mention.replace("#", "")
        mention = mention.replace(">", "")
        mention = mention.replace("!", "")
        return int(mention)

    # Make rank into a 000 format
    @staticmethod
    def format_rank(rank: int) -> str:
        rank = str(rank)
        if len(rank) == 1:
            return f"00{rank}"
        elif len(rank) == 2:
            return f"0{rank}"
        else:
            return rank

    # Make score look nice lol
    @staticmethod
    def format_score(score: int) -> str:
        if score >= 1_000 and score < 10_000:
            score = f"{str(round(score / 1_000, 1))}k"
        elif score >= 10_000 and score < 1_000_000:
            score = f"{str(score // 1_000)}k"
        elif score >= 1_000_000:
            score = f"{str(round(score / 1_000_000, 1))}M"
        else:
            score = str(score)

        return f'{score}{" "*(7-len(score))}'

    # Get medal
    @staticmethod
    def get_medal(rank: int):
        if rank == 1:
            return "🥇"
        elif rank == 2:
            return "🥈"
        elif rank == 3:
            return "🥉"

        return ""

    # Get guild
    @staticmethod
    def get_guild(id: int) -> Guild:
        if str(id) in db:
            return Guild(**db[str(id)])
        else:
            return Guild(id)

    # Dump guild and member
    @staticmethod
    def dump(guild: Guild, member: Member = None):
        if member is not None:
            guild.members[str(member.id)] = asdict(member)

        db[str(guild.id)] = asdict(guild)

    # POINT CAP LOOP
    @tasks.loop(seconds=60)
    async def reset_temp_score(self):
        for guild in db:
            guild = self.get_guild(guild)

            if not guild.point_cap_on:
                continue

            for member in guild.members:
                member = guild.get_member(int(member))

                member.temp_score = 0
                self.dump(guild, member)

    @commands.Cog.listener(name="on_ready")
    async def start_loop(self):
        await self.reset_temp_score.start()

    # COMMANDS

    # On message
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Updates Scores on message"""

        if message.author.bot:
            return

        guild = self.get_guild(message.guild.id)

        if message.channel.id in guild.excluded_channels:
            return

        member = guild.get_member(int(message.author.id), message.author.display_name)

        if member.temp_score >= guild.point_cap and guild.point_cap_on:
            return

        member.score += 1
        member.temp_score += 1 if guild.point_cap_on else 0
        self.dump(guild, member)

    # Score
    @commands.command(aliases=["s", "rank"])
    async def score(self, ctx: Context, member: str = None):
        """Shows score of user if mentioned else shows score of invoker."""

        guild = self.get_guild(ctx.guild.id)

        try:
            rank = int(member)
        except Exception:
            pass
        else:
            lb = guild.get_leaderboard()
            if rank > len(lb):
                await ctx.send(
                    embed=discord.Embed(
                        title="Huh...?", description="❌ Invalid Rank!", color=0xFF0000
                    )
                )
                return

            member = lb[rank - 1]

        if not isinstance(member, Member):
            if (
                member is None
                or guild.get_member(self.decode_mention(member), bot=self.bot) is None
            ):
                member = guild.get_member(ctx.author.id, ctx.author.display_name)

            else:
                member = guild.get_member(self.decode_mention(member))

        pfp_url = guild.get_avatar_url(self.bot, member.id)

        await ctx.reply(
            embed=MessagingScoreEmbeds.Score.show_score(
                member.display_name, pfp_url, member.score, guild.get_rank(member.id)
            ),
            mention_author=False,
        )

    # Leaderboard
    @commands.command(aliases=["leaderboard", "board", "ranklist", "l"])
    async def lb(self, ctx: Context, page_no: int = None):
        """Shows messaging score leaderboard for the server"""

        if not page_no:
            page_no = 1

        guild = self.get_guild(ctx.guild.id)
        leaderboard, pages = guild.get_leaderboard(page_no)
        page = [
            f"{(rank := self.format_rank(guild.get_rank(member.id)))} ⫶ {self.format_score(member.score)} ⫶ {member.display_name} {self.get_medal(rank)}"
            for member in leaderboard
        ]

        if not page:
            await ctx.reply(
                embed=MessagingScoreEmbeds.Lb.page_not_found(), mention_author=False
            )
            return

        embed = discord.Embed(
            title=f"Leaderboard of {ctx.guild.name}",
            description="Messaging scores leaderboard for this server.",
        )
        embed.add_field(
            name=f"RANK ⫶ SCORE ⫶ NAME",
            value="".join("`" + member + "`\n" for member in page),
        )
        embed.set_footer(
            text=f"Currently showing page ({page_no}/{pages}) \n Use {ctx.prefix}{ctx.command} <page no.> to show a specific page."
        )

        await ctx.reply(embed=embed, mention_author=False)
        return

    # Exclude
    @commands.command(aliases=["exc"])
    @commands.has_permissions(administrator=True)
    async def exclude(self, ctx: Context, channel=None):
        """Excludes a channel from adding up messaginf scores."""

        guild = self.get_guild(ctx.guild.id)

        if not channel:
            await ctx.send(f"❌ Mention a channel!", delete_after=20)
            return

        if "<#" in channel and ">" in channel:
            channel = ctx.guild.get_channel(int(self.decode_mention(channel)))

        else:
            await ctx.send("❌ Channel not found.", delete_after=20)
            return

        if channel.id in guild.excluded_channels:
            await ctx.send(
                f"✅ Channel {channel.mention} is already excluded from coutning scores."
            )
            return

        guild.excluded_channels.append(channel.id)

        await ctx.send(
            f"✅ Messages in channel {channel.mention} will no longer add your score."
        )

        self.dump(guild)

    @exclude.error
    async def exclude_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You do not have the clearance level to use this command.")
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("❌ Channel not found.")

    # Include
    @commands.command(aliases=["inc"])
    async def include(self, ctx: Context, channel=None):
        """Includes a channel for adding up messaging scores."""

        guild = self.get_guild(ctx.guild.id)

        if channel is None:
            await ctx.send(f"❌ Mention a channel!", delete_after=20)

        if "<#" in channel and ">" in channel:
            channel = ctx.guild.get_channel(self.decode_mention(channel))
        else:
            await ctx.send("❌ Channel not found.")
            return

        if channel.id not in guild.excluded_channels:
            await ctx.send(
                f"✅ Channel {channel.mention} is already included from counting scores."
            )
            return

        guild.excluded_channels.remove(channel.id)

        await ctx.send(
            f"✅ Messages in channel {channel.mention} will now add your score."
        )

        self.dump(guild)

    @include.error
    async def include_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You do not have the clearance level to use this command.")
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("❌ Channel not found.")

    # Excluded
    @commands.command(aliases=["ec", "channels"])
    async def excluded(self, ctx: Context):
        """Shows channels excluded from messaging scores."""

        guild = self.get_guild(ctx.guild.id)

        embed = discord.Embed(
            title="Excluded Channels",
            description="List of channels excluded from increasing messaging scores.",
            color=0x510490,
        )
        if len(guild.excluded_channels) > 0:
            excluded_channels = "".join(
                f"<#{channel}>" + "\n" for channel in guild.excluded_channels
            )

            embed.add_field(name="List:", value=excluded_channels)
        else:
            embed.add_field(name="List:", value="No channels are excluded.")

        await ctx.reply(embed=embed, mention_author=False)
        return

    # Deduct
    @commands.command(aliases=["points"])
    @commands.has_permissions(administrator=True)
    async def deduct(self, ctx: Context, mention=None, points=None):
        """Deducts points from a member."""

        if not mention or not points:
            await ctx.send(
                embed=discord.Embed(
                    description="❌ Invalid arguments!", color=0xFF0000
                ).set_footer(text=f"Use *{ctx.prefix}help {ctx.command}* for help.")
            )
            return

        try:
            points = int(points)
        except Exception:
            await ctx.send(
                embed=discord.Embed(description=f"❌ Invalid point argument!")
            )
            return

        try:
            mention = self.decode_mention(mention)
        except Exception:
            await ctx.send(embed=discord.Embed(description="❌ Invalid Mention!"))
            return

        guild = self.get_guild(ctx.guild.id)
        member = guild.get_member(mention, bot=self.bot)

        if not member:
            await ctx.send("❌ Member not found!")
            return

        await ctx.send(
            f":interrobang: Are you sure you want to deduce `{points}` points from {member.mention}? (y/n)"
        )

        response = await self.bot.wait_for(
            "message",
            check=lambda m: m.author == ctx.author and m.content.lower() in ["y", "n"],
        )

        if response.content.lower() == "n":
            await response.reply("❌ Command cancelled.")
            return

        points = points if points > 0 else 0 - points

        if member.score - points < 0:
            member.score = 0
        else:
            member.score -= points

        self.dump(guild, member)

        await ctx.send(
            f"✅ {member.mention}'s score is now `{member.score}` after {ctx.author.mention} deduced `{points}` points."
        )

    @deduct.error
    async def deduct_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You do not have the clearance level to use this command.")
        else:
            raise error

    @commands.command(aliases=["pc", "togglecap", "cap"])
    @commands.has_permissions(administrator=True)
    async def pointcap(self, ctx: Context):

        """Toggle point cap for server."""

        guild = self.get_guild(ctx.guild.id)

        guild.point_cap_on = not guild.point_cap_on

        await ctx.send(
            f'✅ Point cap of `{guild.point_cap}` has been toggled {"**ON**" if guild.point_cap_on else "**OFF**"} for this server.'
        )

        self.dump(guild)

    @pointcap.error
    async def pc_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You do not have the clearance level to use this command.")
        else:
            raise error

    @commands.command(aliases=["sc"])
    @commands.has_permissions(administrator=True)
    async def setcap(self, ctx: Context, cap=None):

        """Set point cap"""

        guild = self.get_guild(ctx.guild.id)
        if cap is None:
            await ctx.send(
                f"❌ Invalid argument `{cap}`. Please use `{ctx.prefix}help {ctx.command}` for help."
            )
            return
        try:
            cap = int(cap)
        except Exception:
            await ctx.send(
                f"❌ Invalid argument `{cap}`. Please use `{ctx.prefix}help {ctx.command}` for help."
            )
            return

        if cap < 0:
            cap = -cap
        guild.point_cap = cap
        self.dump(guild)

        await ctx.send(f"✅ Point cap of this server has been set to `{cap}`.")

    @setcap.error
    async def sc_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You do not have the clearance level to use this command.")
        else:
            raise error


def setup(bot):
    bot.add_cog(Cog(bot))
