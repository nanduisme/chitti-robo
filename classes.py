import math
from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class Guild:

    id: int

    # For custom commands
    replies: dict = field(default_factory=dict)
    active_keys: List[str] = field(default_factory=list)
    is_enabled: bool = True

    # For messaging scores
    members: dict = field(default_factory=dict)
    excluded_channels: List[str] = field(default_factory=list)

    def get_leaderboard(self, page: int = None) -> list:
        sorted_members = sorted(
            self.members, key=lambda member: self.members[member]["score"]
        )
        sorted_members.reverse()

        leaderboard = [{**self.members[member]} for member in sorted_members]

        if page is None:
            return leaderboard
        page -= 1
        leaderboard = [{**member} for member in leaderboard if member["score"] > 0]
        return leaderboard[page * 10 : page * 10 + 10], math.ceil(len(leaderboard) / 10)


@dataclass
class Member:

    id: int

    # For messaging scores
    display_name: str
    score: int = field(default=0, compare=False)

    @property
    def mention(self):
        return f'<@{self.id}>'

    def get_avatar_url(self, bot, guild):
        return bot.get_guild(guild.id).get_member(self.id).avatar_url

    def get_rank(self, guild: Guild):
        self = asdict(self)
        leaderboard = guild.get_leaderboard()
        return (leaderboard.index(self) + 1) if self in guild.get_leaderboard() else 0
