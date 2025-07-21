"""Audio utilities for the Twitch Milestone Celebrator."""
import os
import tempfile
import time
from pathlib import Path
from typing import Dict, Optional, Union

import pygame
from gtts import gTTS

from twitch_milestone_celebrator.config.settings import SoundConfig, TTSConfig
from twitch_milestone_celebrator.utils.logging import get_logger

logger = get_logger("audio")


class AudioPlayer:
    """Handles audio playback for the Twitch Milestone Celebrator."""
    
    def __init__(self):
        """Initialize the audio player."""
        self.sounds: Dict[str, Optional[pygame.mixer.Sound]] = {}
        self._initialized = False
        self._initialize()
    
    def _initialize(self) -> None:
        """Initialize the audio mixer and load sounds."""
        if not SoundConfig.ENABLED:
            logger.info("Sound is disabled in settings")
            return
            
        try:
            # Initialize the mixer with reasonable defaults
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
            self._initialized = True
            logger.info("Audio mixer initialized successfully")
            
            # Load the default sound
            self._load_sound("default", SoundConfig.DEFAULT_SOUND)
            
        except Exception as e:
            logger.error("Failed to initialize audio: %s", str(e), exc_info=True)
            self._initialized = False
    
    def _load_sound(self, name: str, sound_file: Union[str, Path]) -> bool:
        """
        Load a sound file into memory.
        
        Args:
            name: Name to reference the sound by
            sound_file: Path to the sound file
            
        Returns:
            bool: True if the sound was loaded successfully, False otherwise
        """
        if not self._initialized:
            return False
            
        try:
            # Convert string paths to Path objects
            if isinstance(sound_file, str):
                sound_file = Path(sound_file)
            
            # If path is not absolute, look in the sounds directory
            if not sound_file.is_absolute():
                sound_file = SoundConfig.SOUNDS_DIR / sound_file
            
            # Check if file exists
            if not sound_file.exists():
                logger.warning("Sound file not found: %s", sound_file)
                self.sounds[name] = None
                return False
            
            # Load the sound
            sound = pygame.mixer.Sound(str(sound_file))
            self.sounds[name] = sound
            logger.debug("Loaded sound: %s from %s", name, sound_file)
            return True
            
        except Exception as e:
            logger.error("Failed to load sound %s: %s", sound_file, str(e), exc_info=True)
            self.sounds[name] = None
            return False
    
    def play_sound(self, name: str = "default") -> bool:
        """
        Play a loaded sound.
        
        Args:
            name: Name of the sound to play
            
        Returns:
            bool: True if the sound was played successfully, False otherwise
        """
        if not self._initialized or not SoundConfig.ENABLED:
            return False
            
        sound = self.sounds.get(name)
        if sound is None:
            # Try to load the sound if it's not loaded
            if name == "default":
                sound_file = SoundConfig.DEFAULT_SOUND
            else:
                sound_file = name
                
            if not self._load_sound(name, sound_file):
                return False
                
            sound = self.sounds.get(name)
            if sound is None:
                return False
        
        try:
            sound.play()
            logger.debug("Playing sound: %s", name)
            return True
            
        except Exception as e:
            logger.error("Failed to play sound %s: %s", name, str(e), exc_info=True)
            return False
    
    def text_to_speech(self, text: str, language: str = None) -> bool:
        """
        Convert text to speech and play it.
        
        Args:
            text: Text to convert to speech
            language: Language code (e.g., 'en', 'es'). Uses TTS_LANGUAGE from settings if None.
            
        Returns:
            bool: True if the TTS was played successfully, False otherwise
        """
        if not TTSConfig.ENABLED or not self._initialized:
            return False
            
        if not text.strip():
            logger.warning("Empty text for TTS")
            return False
            
        language = language or TTSConfig.LANGUAGE
        
        try:
            # Create cache directory if it doesn't exist
            TTSConfig.ensure_cache_dir_exists()
            
            # Generate a cache key based on the text and language
            import hashlib
            cache_key = hashlib.md5(f"{text}_{language}".encode('utf-8')).hexdigest()
            cache_file = TTSConfig.CACHE_DIR / f"{cache_key}.mp3"
            
            # Generate TTS if not in cache
            if not cache_file.exists():
                tts = gTTS(text=text, lang=language, slow=False)
                tts.save(str(cache_file))
                logger.debug("Generated TTS and saved to cache: %s", cache_file)
            
            # Play the sound
            return self.play_sound(str(cache_file))
            
        except Exception as e:
            logger.error("TTS failed: %s", str(e), exc_info=True)
            return False
    
    def stop_all_sounds(self) -> None:
        """Stop all currently playing sounds."""
        if self._initialized:
            pygame.mixer.stop()
    
    def cleanup(self) -> None:
        """Clean up resources."""
        if self._initialized:
            self.stop_all_sounds()
            pygame.mixer.quit()
            self._initialized = False
