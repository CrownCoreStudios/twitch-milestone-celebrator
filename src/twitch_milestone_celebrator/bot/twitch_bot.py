"""Twitch bot for the Twitch Milestone Celebrator."""
import asyncio
import json
import os
import random
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import pygame
from twitchio import Message, User
from twitchio.ext import commands

from twitch_milestone_celebrator.config.settings import TwitchConfig, TTSConfig, SoundConfig, UIConfig
from twitch_milestone_celebrator.ui.window import CelebrationWindow
from twitch_milestone_celebrator.utils.audio import AudioPlayer
from twitch_milestone_celebrator.utils.logging import get_logger

logger = get_logger("bot")


class TwitchMilestoneBot(commands.Bot):
    """Twitch bot that celebrates chat milestones and events."""
    
    def __init__(self):
        """Initialize the Twitch bot."""
        # Initialize the bot with Twitch credentials
        super().__init__(
            token=f"oauth:{TwitchConfig.OAUTH_TOKEN}",
            prefix=TwitchConfig.PREFIX,
            initial_channels=[TwitchConfig.CHANNEL],
            client_id=TwitchConfig.CLIENT_ID
        )
        
        # Chat monitoring settings
        self.keywords = TwitchConfig.get_keywords()
        self.keyword_cooldown: Dict[str, float] = {}
        self.keyword_cooldown_seconds = TwitchConfig.KEYWORD_COOLDOWN
        
        # Keyword tracking and anti-spam
        self.keyword_history: Dict[str, deque] = defaultdict(deque)
        self.keyword_replacements = {
            'poggers': ['pogchamp', 'pog', 'pogU', 'poggers', 'pogchampion'],
            'lets go': ['lets go', 'less go', 'leggo', 'lfg', 'lez go'],
            'gg': ['gg', 'good game', 'well played', 'wp', 'ggwp'],
            'wp': ['wp', 'well played', 'good game', 'gg', 'ggwp'],
            'lol': ['lol', 'lmao', 'lmfao', 'lul', 'haha'],
            'lulw': ['lulw', 'lul', 'kekw', 'lmao', 'lol']
        }
        self.user_cooldown: Dict[str, float] = {}
        self.global_cooldown: float = 0.0
        
        # Audio player
        self.audio_player = AudioPlayer()
        
        # Celebration window
        self.window = CelebrationWindow()
        
        # Track milestones
        self.viewer_milestones = set(TwitchConfig.get_viewer_milestones())
        self.celebrated_milestones: Set[int] = set()
        
        # Track followers and subscribers
        self.recent_followers: deque = deque(maxlen=100)
        self.recent_subscribers: deque = deque(maxlen=100)
        
        # Track viewer count
        self.last_viewer_count: int = 0
        self.viewer_count_last_updated: float = 0.0
        
        # Start the window update loop in a separate thread
        self.running = True
        self.loop.create_task(self._window_update_loop())
        
        logger.info("TwitchMilestoneBot initialized")
    
    async def _window_update_loop(self) -> None:
        """Run the window update loop in the asyncio event loop."""
        logger.info("Starting window update loop")
        
        try:
            while self.running:
                # Update the window
                self.window.update()
                
                # Sleep to avoid high CPU usage
                await asyncio.sleep(1.0 / UIConfig.FPS)
                
        except Exception as e:
            logger.error("Error in window update loop: %s", str(e), exc_info=True)
            self.running = False
    
    async def event_ready(self) -> None:
        """Called when the bot goes online."""
        logger.info(f"Logged in as {self.nick}")
        logger.info(f"User ID: {self.user_id}")
        logger.info(f"Channels: {self.connected_channels}")
        
        # Start background tasks
        self.loop.create_task(self._check_viewer_count())
        
        # Join the configured channel
        channel = self.get_channel(TwitchConfig.CHANNEL)
        if channel:
            await channel.send("Milestone Celebrator is now active! 🎉")
    
    async def event_message(self, message: Message) -> None:
        """Handle incoming messages."""
        # Ignore messages from the bot itself
        if message.author is None or message.author.name.lower() == self.nick.lower():
            return
        
        # Process commands
        await self.handle_commands(message)
        
        # Check for keywords in the message
        await self._check_keywords(message)
    
    async def _check_keywords(self, message: Message) -> None:
        """Check if the message contains any trigger keywords."""
        if not message.content or not hasattr(message, 'author') or not message.author:
            return
        
        content = message.content.lower()
        username = message.author.name.lower()
        current_time = time.time()
        
        # Check global cooldown
        if current_time - self.global_cooldown < 1.0:  # 1 second global cooldown
            return
        
        # Check user cooldown
        if current_time - self.user_cooldown.get(username, 0) < 10.0:  # 10 second user cooldown
            return
        
        # Check for keywords
        for keyword in self.keywords:
            if keyword.lower() in content:
                # Check keyword cooldown
                if current_time - self.keyword_cooldown.get(keyword, 0) < self.keyword_cooldown_seconds:
                    continue
                
                # Get the next variant of the keyword to prevent spam
                variant = self._get_next_keyword_variant(keyword)
                
                # Update cooldowns
                self.keyword_cooldown[keyword] = current_time
                self.user_cooldown[username] = current_time
                self.global_cooldown = current_time
                
                # Log the trigger
                logger.info(f"Keyword triggered: {keyword} by {username}")
                
                # Celebrate!
                await self.celebrate(f"{message.author.name} said {variant}!", "keyword")
                break
    
    def _get_next_keyword_variant(self, keyword: str) -> str:
        """Get the next variant of a keyword to prevent spam."""
        if keyword not in self.keyword_history:
            self.keyword_history[keyword] = deque(maxlen=5)
        
        # Get possible variants
        variants = self.keyword_replacements.get(keyword, [keyword])
        
        # Filter out recently used variants
        available_variants = [v for v in variants if v not in self.keyword_history[keyword]]
        
        # If all variants have been used recently, clear the history
        if not available_variants:
            self.keyword_history[keyword].clear()
            available_variants = variants
        
        # Choose a random variant
        variant = random.choice(available_variants)
        
        # Update history
        self.keyword_history[keyword].append(variant)
        
        return variant
    
    async def _check_viewer_count(self) -> None:
        """Periodically check the viewer count and celebrate milestones."""
        logger.info("Starting viewer count checker")
        
        try:
            while self.running:
                try:
                    # Get the current channel
                    channel = self.get_channel(TwitchConfig.CHANNEL)
                    if not channel:
                        logger.warning(f"Channel {TwitchConfig.CHANNEL} not found")
                        await asyncio.sleep(60)  # Wait a minute before retrying
                        continue
                    
                    # Get viewer count (this is a placeholder - you'll need to implement this)
                    # In a real implementation, you would use the Twitch API to get the current viewer count
                    viewer_count = 0  # Replace with actual viewer count
                    
                    # Check for milestones
                    await self._check_viewer_milestones(viewer_count)
                    
                    # Update last viewer count and timestamp
                    self.last_viewer_count = viewer_count
                    self.viewer_count_last_updated = time.time()
                    
                except Exception as e:
                    logger.error(f"Error checking viewer count: {str(e)}", exc_info=True)
                
                # Wait before checking again
                await asyncio.sleep(60)  # Check every minute
                
        except asyncio.CancelledError:
            logger.info("Viewer count checker cancelled")
            raise
        except Exception as e:
            logger.error(f"Fatal error in viewer count checker: {str(e)}", exc_info=True)
            self.running = False
    
    async def _check_viewer_milestones(self, viewer_count: int) -> None:
        """Check if we've reached any viewer milestones."""
        for milestone in sorted(self.viewer_milestones):
            if (viewer_count >= milestone and 
                milestone not in self.celebrated_milestones and
                viewer_count > self.last_viewer_count):
                
                # Celebrate the milestone
                await self.celebrate(
                    f"🎉 {viewer_count} viewers! 🎉",
                    "viewer_milestone"
                )
                
                # Mark as celebrated
                self.celebrated_milestones.add(milestone)
                logger.info(f"Celebrated {viewer_count} viewer milestone")
    
    async def celebrate(self, message: str, event_type: str = "milestone") -> None:
        """
        Trigger a celebration.
        
        Args:
            message: The message to display
            event_type: Type of event (e.g., 'milestone', 'follower', 'subscriber')
        """
        logger.info(f"Celebrating: {message} ({event_type})")
        
        # Show the celebration in the window
        self.window.show_celebration(message, event_type)
        
        # Play a sound
        self.audio_player.play_sound()
        
        # Optionally, use TTS
        if TTSConfig.ENABLED:
            self.loop.create_task(self._tts_speak(message))
    
    async def _tts_speak(self, text: str) -> None:
        """Speak text using TTS."""
        try:
            await asyncio.to_thread(
                self.audio_player.text_to_speech,
                text,
                TTSConfig.LANGUAGE
            )
        except Exception as e:
            logger.error(f"TTS error: {str(e)}", exc_info=True)
    
    # Command handlers
    @commands.command(name="celebrate")
    async def cmd_celebrate(self, ctx: commands.Context) -> None:
        """Manually trigger a celebration."""
        if not ctx.message or not ctx.author:
            return
        
        # Check for moderator/broadcaster permissions
        if not await self._check_permissions(ctx):
            await ctx.send("You don't have permission to use this command.")
            return
        
        # Get the message to celebrate (everything after the command)
        message = ctx.message.content[len(ctx.prefix + ctx.command.name):].strip()
        if not message:
            message = f"{ctx.author.name} started a celebration! 🎉"
        
        await self.celebrate(message, "manual")
    
    @commands.command(name="addkeyword")
    async def cmd_add_keyword(self, ctx: commands.Context) -> None:
        """Add a keyword to trigger celebrations."""
        if not await self._check_permissions(ctx):
            await ctx.send("You don't have permission to use this command.")
            return
        
        keyword = ctx.message.content[len(ctx.prefix + ctx.command.name):].strip().lower()
        if not keyword:
            await ctx.send("Please specify a keyword to add.")
            return
        
        if keyword in self.keywords:
            await ctx.send(f"Keyword '{keyword}' is already in the list.")
            return
        
        self.keywords.append(keyword)
        await ctx.send(f"Added keyword: {keyword}")
        logger.info(f"Added keyword: {keyword}")
    
    @commands.command(name="listkeywords")
    async def cmd_list_keywords(self, ctx: commands.Context) -> None:
        """List all active keywords."""
        if not self.keywords:
            await ctx.send("No keywords are currently active.")
            return
        
        keywords = ", ".join(f"'{k}'" for k in self.keywords)
        await ctx.send(f"Active keywords: {keywords}")
    
    async def _check_permissions(self, ctx: commands.Context) -> bool:
        """Check if the user has permission to use moderator commands."""
        if not ctx.author:
            return False
        
        # Check if the user is a moderator or the broadcaster
        if hasattr(ctx.author, 'is_mod') and ctx.author.is_mod:
            return True
        
        if hasattr(ctx.author, 'is_broadcaster') and ctx.author.is_broadcaster:
            return True
        
        # Check if the user is the bot owner (from environment variable)
        owner = os.getenv("BOT_OWNER", "").lower()
        if owner and ctx.author.name.lower() == owner:
            return True
        
        return False
    
    async def close(self) -> None:
        """Clean up resources."""
        logger.info("Shutting down Twitch bot...")
        self.running = False
        
        # Clean up the window
        if hasattr(self, 'window'):
            self.window.cleanup()
        
        # Clean up the audio player
        if hasattr(self, 'audio_player'):
            self.audio_player.cleanup()
        
        # Call the parent class's close method
        await super().close()
        logger.info("Twitch bot shutdown complete")


def run_bot() -> None:
    """Run the Twitch bot."""
    # Set up logging
    from twitch_milestone_celebrator.utils.logging import setup_logger
    setup_logger(level="INFO")
    
    bot = None
    
    try:
        # Create and run the bot
        bot = TwitchMilestoneBot()
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
    finally:
        # Clean up
        if bot:
            asyncio.run(bot.close())
        
        # Make sure pygame is properly shut down
        pygame.quit()
        
        logger.info("Bot has been shut down")


if __name__ == "__main__":
    run_bot()
