"""Configuration settings for the Twitch Milestone Celebrator."""
import os
from pathlib import Path
from typing import Dict, List, Optional, Union

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent.parent.parent

# Twitch Bot Settings
class TwitchConfig:
    """Twitch bot configuration."""
    
    BOT_USERNAME: str = os.getenv("TWITCH_BOT_USERNAME", "")
    OAUTH_TOKEN: str = os.getenv("TWITCH_OAUTH_TOKEN", "").lstrip("oauth:")
    CHANNEL: str = os.getenv("TWITCH_CHANNEL", "")
    CLIENT_ID: str = os.getenv("TWITCH_CLIENT_ID", "")
    CLIENT_SECRET: str = os.getenv("TWITCH_CLIENT_SECRET", "")
    
    # Chat settings
    PREFIX: str = "!"
    KEYWORD_COOLDOWN: int = 300  # 5 minutes cooldown per keyword (in seconds)
    
    # Default keywords if none provided in .env
    DEFAULT_KEYWORDS = ["poggers", "lets go", "gg", "wp", "lol", "lulw"]
    
    @classmethod
    def get_keywords(cls) -> List[str]:
        """Get the list of chat keywords to monitor."""
        keywords_str = os.getenv("CHAT_KEYWORDS", "")
        if not keywords_str:
            return cls.DEFAULT_KEYWORDS
        return [k.strip().lower() for k in keywords_str.split(",") if k.strip()]
    
    @classmethod
    def get_viewer_milestones(cls) -> List[int]:
        """Get the list of viewer milestones to celebrate."""
        milestones_str = os.getenv("VIEWER_MILESTONES", "1,5,10,25,50,100")
        try:
            return sorted(int(m.strip()) for m in milestones_str.split(",") if m.strip())
        except (ValueError, AttributeError):
            return [1, 5, 10, 25, 50, 100]


# TTS Settings
class TTSConfig:
    """Text-to-Speech configuration."""
    
    ENABLED: bool = os.getenv("TTS_ENABLED", "true").lower() == "true"
    LANGUAGE: str = os.getenv("TTS_LANGUAGE", "en")
    CACHE_DIR: Path = BASE_DIR / "cache" / "tts"
    
    @classmethod
    def ensure_cache_dir_exists(cls) -> None:
        """Ensure the TTS cache directory exists."""
        cls.CACHE_DIR.mkdir(parents=True, exist_ok=True)


# UI Settings
class UIConfig:
    """UI configuration for the celebration window."""
    
    WINDOW_WIDTH: int = 800
    WINDOW_HEIGHT: int = 600
    WINDOW_TITLE: str = "Twitch Milestone Celebrator"
    
    # Animation settings
    ANIMATION_DURATION: float = 8.0  # seconds
    FPS: int = 60
    
    # Colors (RGBA)
    COLORS = [
        (255, 50, 50, 255),    # Red
        (50, 255, 50, 255),    # Green
        (50, 50, 255, 255),    # Blue
        (255, 255, 50, 255),   # Yellow
        (255, 50, 255, 255),   # Magenta
        (50, 255, 255, 255),   # Cyan
    ]
    
    # Font settings
    FONT_NAME: str = "Arial"
    TITLE_FONT_SIZE: int = 72
    SUBTITLE_FONT_SIZE: int = 28
    
    # Window position (None for default/centered)
    WINDOW_X: Optional[int] = None
    WINDOW_Y: Optional[int] = None


# Sound Settings
class SoundConfig:
    """Sound effect configuration."""
    
    ENABLED: bool = True
    SOUNDS_DIR: Path = BASE_DIR / "sounds"
    DEFAULT_SOUND: str = "celebration_sound.mp3"
    
    @classmethod
    def ensure_sounds_dir_exists(cls) -> None:
        """Ensure the sounds directory exists."""
        cls.SOUNDS_DIR.mkdir(parents=True, exist_ok=True)


# Logging configuration
class LoggingConfig:
    """Logging configuration."""
    
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FILE: Path = BASE_DIR / "logs" / "twitch_milestone_celebrator.log"
    MAX_LOG_SIZE: int = 5 * 1024 * 1024  # 5MB
    BACKUP_COUNT: int = 3
    
    @classmethod
    def ensure_log_dir_exists(cls) -> None:
        """Ensure the log directory exists."""
        cls.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


# Initialize required directories
TTSConfig.ensure_cache_dir_exists()
SoundConfig.ensure_sounds_dir_exists()
LoggingConfig.ensure_log_dir_exists()
