from dataclasses import dataclass, field
from typing import List

@dataclass
class Member:
    
    id: int 
    
    # For messaging scores
    display_name: str 
    score: int = 0

@dataclass
class Guild:
    
    id: int 

    # For custom commands
    replies: dict = field(default_factory=dict)
    active_keys: List[str] = field(default_factory=list)
    is_enabled: bool = True

    # For messaging scores
    members: List[Member] = field(default_factory=list)
    excluded_channels: List[str] = field(default_factory=list)

    def get_leaderboard(self):
        return sorted(self.members, key=lambda member: member.score)

