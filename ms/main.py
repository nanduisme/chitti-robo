from dataclasses import asdict

import discord
from replit import db
from discord.ext import commands
from discord.ext.commands.context import Context

from classes import Guild, Member
from embeds import MessagingScoreEmbeds, GeneralEmbeds


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
        return mention

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

    # Add in k and M and all that to the score
    @staticmethod
    def add_suffix(score: int) -> str:
        if score >= 1000 and score < 10000:
            return f"{str(round(score/1000, 1))}k"
        elif score >= 10000 and score < 1000000:
            return f"{str(score//1000)}k"
        elif score >= 1000000:
            return f"{str(round(score/1000000, 1))}M"
        else:
            return str(score)

    # Make score look nice lol
    @staticmethod
    def format_score(score: int) -> str:
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

    # Get guild and member
    @staticmethod
    def get_guild(id: int) -> Guild:
        if str(id) in db:
            return Guild(**db[str(id)])
        else:
            return Guild(id)

    def get_member(self, guild: Guild, id: int, display_name: str) -> Member:
        for member in guild.members:
            if guild.members[member]["id"] == id:
                member = Member(**guild.members[member])
                member.display_name = display_name
                return member

        self.dump(guild, Member(id, display_name))
        return Member(id, display_name)

    # Dump guild and member
    @staticmethod
    def dump(guild: Guild, member: Member = None):
        if member is not None:
            guild.members[str(member.id)] = asdict(member)

        db[str(guild.id)] = asdict(guild)

    # Get member from mention
    def find_member(self, ctx: Context, mention: str):
        member_id = self.decode_mention(mention)
        try:
            member_id = int(member_id)
        except:
            return

        guild = self.get_guild(ctx.guild.id)
        if (
            ctx.guild.get_member(member_id) is None
            or ctx.guild.get_member(member_id).bot
        ):
            return
        else:
            return self.get_member(
                guild, member_id, ctx.guild.get_member(member_id).display_name
            )

    # COMMANDS

    # On message
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Updates Scores on message"""

        if message.author.bot:
            return

        guild = self.get_guild(message.guild.id)
        member = self.get_member(guild, message.author.id, message.author.display_name)

        if message.channel.id in guild.excluded_channels:
            return

        member.score += 1

        self.dump(guild, member)


    # Score
    @commands.command(aliases=["s", "rank"])
    async def score(self, ctx: Context, mention: str = None):
        """Shows score of user if mentioned else shows score of invoker."""

        if mention is None or self.find_member(ctx, mention) is None:
            member = self.get_member(
                self.get_guild(ctx.guild.id), ctx.author.id, ctx.author.display_name
            )
        else:
            member = self.find_member(ctx, mention)

        pfp_url = member.get_avatar_url(self.bot, self.get_guild(ctx.guild.id))

        await ctx.reply(
            embed=MessagingScoreEmbeds.Score.show_score(
                member.display_name,
                pfp_url,
                member.score,
                member.get_rank(self.get_guild(ctx.guild.id)),
            ),
            mention_author=False,
        )

    # Leaderboard
    @commands.command(aliases=["leaderboard", "board", "ranklist", "l"])
    async def lb(self, ctx: Context, page_no: int = None):
        """Shows messaging score leaderboard for the server"""

        if page_no is None:
            page_no = 1

        guild = self.get_guild(ctx.guild.id)
        leaderboard, pages = guild.get_leaderboard(page_no)
        page = [
            f'{self.format_rank(Member(**member).get_rank(guild))} ⫶ {self.format_score(self.add_suffix(member["score"]))} ⫶ {member["display_name"]} {self.get_medal(Member(**member).get_rank(guild))}'
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
    @commands.has_permissions(administrator = True)
    async def exclude(self, ctx: Context, channel= None):
        """Excludes a channel from adding up messaginf scores."""

        guild = self.get_guild(ctx.guild.id)

        if channel is None:
            await ctx.send(f'❌ Mention a channel at the end of the command! Eg: `{ctx.prefix}{ctx.command} #channel-name`')
            return

        if "<#" in channel and ">" in channel:
            channel = ctx.guild.get_channel(int(self.decode_mention(channel)))

        else:
            await ctx.send("❌ Channel not found.")
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
    @commands.command(aliases=['inc'])
    async def include(self, ctx: Context, channel = None):
        """Includes a channel for adding up messaging scores."""

        guild = self.get_guild(ctx.guild.id)

        if channel is None:
            await ctx.send(f'❌ Mention a channel at the end of the command! Eg: `{ctx.prefix}{ctx.command} #channel-name`')

        if "<#" in channel and ">" in channel:
            channel = ctx.guild.get_channel(int(self.decode_channel(channel)))
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
                f'<#{channel}>' + "\n" for channel in guild.excluded_channels
            )

            embed.add_field(name="List:", value=excluded_channels)
        else:
            embed.add_field(name="List:", value="No channels are excluded.")

        await ctx.reply(embed=embed, mention_author=False)
        return

    # Deduct
    @commands.command(aliases=["take"])
    @commands.has_permissions(administrator=True)
    async def deduct(self, ctx: Context, mention = None):
        """Deducts points from a member."""

        guild = self.get_guild(ctx.guild.id)

        if mention is None:
            await ctx.send(f"Mention the member you would like to take points from.")
            mention = await self.bot.wait_for("message")
            mention = mention.content

        if ctx.guild.get_member(self.decode_menion(mention)) is None:
            await ctx.send(f'❌ Member {mention} not found!')
            return

        member = self.get_member(guild, ctx.author.id, ctx.author.display_name)

        while True:
            await ctx.send(
                f"How many points would you like to deduct from {member.mention}?"
            )
            take = await self.bot.wait_for("message")
            try:
                take = int(take.content)
                break
            except:
                await ctx.send("❌ Please enter a valid number.")

        def yn_check(m):
            return m.author == ctx.author and m.content.lower() in ["y", "n"]

        await ctx.send(
            f":interrobang: Are you sure you want to deduce `{take}` points from {member.mention}? (y/n)"
        )
        response = await self.bot.wait_for("message", check=yn_check)

        if response.content.lower() == "n":
            await response.reply("❌ Command cancelled.")
            return        

        take = take if take > 0 else 0 - take

        if member.score - take < 0:
            member.score = 0
        else:
            member.score -= take

        await ctx.send(
            f"✅ {member.mention}'s score is now `{member.score}` after {ctx.author.mention} deduced `{take}` points."
        )

    @deduct.error
    async def deduct_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You do not have the clearance level to use this command.")


def setup(bot):
    bot.add_cog(Cog(bot))
