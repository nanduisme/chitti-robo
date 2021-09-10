import math
from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class Member:

    id: int

    # For messaging scores
    display_name: str = ""
    score: int = field(default=0, compare=False)
    temp_score: int = 0

    # For Games
    is_playing: bool = False

    @property
    def mention(self):
        return f"<@{self.id}>"


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
    point_cap_on: bool = field(default=False)
    point_cap: int = field(default=10)

    def get_member(self, id: int, display_name: str = None, bot=None) -> Member:
        if (
            not bot  # Bot is not given
            or not (
                member := bot.get_guild(self.id).get_member(id)  # Member does not exist
            )
            or member.bot  # Member is a bot
        ):
            pass

        if str(id) not in self.members:
            member = Member(id, display_name=display_name)
        else:
            member = Member(**self.members[str(id)])

        if display_name is not None:
            member.display_name = display_name

        return member

    def get_leaderboard(self, page: int = None) -> list:
        sorted_members = sorted(
            self.members, key=lambda member: self.members[member]["score"]
        )
        sorted_members.reverse()

        leaderboard = [
            Member(**self.members[member])
            for member in sorted_members
            if self.members[member]["score"] > 0
        ]

        if page is None:
            return leaderboard

        page -= 1
        leaderboard = [member for member in leaderboard if member.score > 0]

        return leaderboard[page * 10 : page * 10 + 10], math.ceil(len(leaderboard) / 10)

    def get_rank(self, member_id: int) -> int:
        lb = self.get_leaderboard()
        member = self.get_member(member_id)
        return lb.index(member) + 1 if member in lb else 0

    def get_avatar_url(self, bot, id: int):
        return bot.get_guild(self.id).get_member(id).avatar_url
