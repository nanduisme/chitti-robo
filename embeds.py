"""Embeds For Chitti Boi"""

import discord

PURPLE = 0x510490
RED = 0xFF0000
GREEN = 0x00FF00


class GeneralEmbeds:
    """General Embeds"""

    @staticmethod
    def timeout():
        return discord.Embed(
            title="Oops!", description="You didn't respond in time!", color=RED
        )

    @staticmethod
    def command_cancelled():
        return discord.Embed(
            title="Okey-doke!", description="Alrighty! Command cancelled.", color=RED
        )


class CustomCommandEmbeds:
    """Embeds for custom commands"""

    class Add:
        """cc add"""

        @staticmethod
        def key_exists(keyword):
            return discord.Embed(
                title="Hold on!",
                description=f"Keyword `{keyword}` already exists! Are you sure you want to add a reply to it? (y/n)",
                color=PURPLE,
            )

        @staticmethod
        def reply_exists(keyword, reply):
            return discord.Embed(
                title="Reply Exists.",
                description=f"Reply `{reply}` already exists for keyword `{keyword}`. Command cancelled.",
                color=RED,
            )

        @staticmethod
        def confirm(keyword, reply):
            return discord.Embed(
                title="You sure?",
                description=f"Are you sure you want to add response, `{reply}`, to key `{keyword}` (y/n)",
                color=PURPLE,
            )

        @staticmethod
        def added(keyword, reply):
            return discord.Embed(
                title="Keyword Added!",
                description=f"Reply `{reply}` has been added to keyword `{keyword}`.",
                color=GREEN,
            )

    class Remove:
        """cc remove"""

        @staticmethod
        def keyword_not_found(keyword):
            return discord.Embed(
                title="Keyword not found!".title(),
                description=f"Keyword, `{keyword}` not found! Bummer! Command Cancelled.",
                color=RED,
            )

        @staticmethod
        def show_replies(keyword: str, replies: list):
            embed = discord.Embed(
                title=f'Replies for "{keyword}"',
                description=f"Enter index number of reply to be removed: ",
                color=PURPLE,
            )

            for reply in replies:
                embed.add_field(
                    name=f"{replies.index(reply) + 1}:", value=f"{reply}", inline=False
                )

            return embed

        @staticmethod
        def invalid_index(index: str):
            return discord.Embed(
                title=f"Invalid Index!",
                description=f"Index `{index}` is invalid! Command cancelled.",
                color=RED,
            )

        @staticmethod
        def confirm(keyword: str, reply: str):
            return discord.Embed(
                title="Are you sure?",
                description=f"Are you sure you want to remove response, `{reply}` from keyword, `{keyword}`. (y/n)",
                color=PURPLE,
            )

        @staticmethod
        def removed(keyword: str, reply: str):
            return discord.Embed(
                title=f"Response Removed!",
                description=f"Response `{reply}` has been removed from keyword `{keyword}`.",
                color=GREEN,
            )

    class Toggle:
        """cc toggle"""

        @staticmethod
        def keyword_not_found(keyword):
            return discord.Embed(
                title="Keyword not found!",
                description=f"Keyword `{keyword}` not found! Aw man. Command cancelled.",
                color=RED,
            )

        @staticmethod
        def toggled_off(keyword):
            return discord.Embed(
                title="Toggled Off!",
                description=f"Keyword `{keyword}` has been toggled **OFF** for this server.",
                color=GREEN,
            )

        @staticmethod
        def toggled_on(keyword):
            return discord.Embed(
                title="Toggled On!",
                description=f"Keyword `{keyword}` has been toggled **ON** for this server.",
                color=GREEN,
            )

    class Show:
        """cc show/list"""

        @staticmethod
        def show_all(guild):
            embed = discord.Embed(
                title="All the custom commands and responses", color=PURPLE
            )

            for command in guild.replies:
                replies = "".join(
                    f"{guild.replies[command].index(reply) + 1} : `{reply}` \n"
                    for reply in guild.replies[command]
                )

                embed.add_field(
                    name=f'{command} - [{"ON" if command in guild.active_keys else "OFF"}]',
                    value=replies,
                )

            return embed

        @staticmethod
        def key_not_found(key, prefix):
            return discord.Embed(
                title="Huh?",
                description=f"I cant seem to find the key, `{key}` you're talking about :/",
            ).set_footer(text="Use `{prefix}cc show` to make sure it actually exists.")

        @staticmethod
        def show_key(key, guild):
            return discord.Embed(
                title=f"All replies for key `{key}`",
                description="".join(
                    f"{guild.replies[key].index(reply) + 1} : `{reply}` \n"
                    for reply in guild.replies[key]
                ),
                color=PURPLE,
            )


class MessagingScoreEmbeds:
    """Embeds for messaging score cog"""

    class Score:
        """ms score"""

        @staticmethod
        def invalid_mention(mention):
            return discord.Embed(
                title="Bruh",
                description=f"`{mention}` is not a valid mention!",
                color=RED,
            )

        @staticmethod
        def member_not_found(mention):
            return discord.Embed(
                title="Who?",
                description=f"I cant find a `{mention}` on this server. :/",
            )

        @staticmethod
        def show_score(name: str, avatar: str, score: int, rank: int):
            embed = discord.Embed(title=name)
            embed.set_thumbnail(url=avatar)
            embed.add_field(
                name="Messaging Score",
                value=f"Your messaging score is `{score}`.",
            )
            embed.add_field(
                name="Rank",
                value=f"Your rank in this server is `{rank}`",
            )
            return embed

    class Lb:
        """ms lb"""

        @staticmethod
        def page_not_found():
            return discord.Embed(
                title="Where is that...?", description="Page not found!", color=RED
            )
