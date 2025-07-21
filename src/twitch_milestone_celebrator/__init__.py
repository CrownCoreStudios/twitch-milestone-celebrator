"""Twitch Milestone Celebrator - Celebrate Twitch chat events with style!"""

__version__ = "0.1.0"
__author__ = "CrownCore Studios <crowncorestudios@gmail.com>"
__license__ = "MIT"

# Import key components for easier access
from twitch_milestone_celebrator.bot.twitch_bot import TwitchMilestoneBot
from twitch_milestone_celebrator.ui.window import CelebrationWindow

__all__ = [
    'TwitchMilestoneBot',
    'CelebrationWindow',
]
