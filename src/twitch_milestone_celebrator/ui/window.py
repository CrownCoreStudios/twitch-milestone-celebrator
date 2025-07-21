"""Main window for the Twitch Milestone Celebrator."""
import ctypes
import os
import sys
from typing import Optional, Tuple

import pygame

from twitch_milestone_celebrator.config.settings import UIConfig
from twitch_milestone_celebrator.utils.logging import get_logger
from twitch_milestone_celebrator.utils.visuals import VisualEffects

logger = get_logger("ui.window")


class CelebrationWindow:
    """Main window for displaying celebration effects."""
    
    def __init__(self):
        """Initialize the celebration window."""
        self.width = UIConfig.WINDOW_WIDTH
        self.height = UIConfig.WINDOW_HEIGHT
        self.running = False
        self.clock = pygame.time.Clock()
        self.effects = VisualEffects()
        self.screen = None
        self.window_x = UIConfig.WINDOW_X
        self.window_y = UIConfig.WINDOW_Y
        
        # Set up the window
        self._setup_window()
        
        # Load any additional resources
        self._load_resources()
    
    def _setup_window(self) -> None:
        """Set up the Pygame window with the correct properties."""
        try:
            # Initialize pygame
            pygame.init()
            
            # Set window position if not specified
            if self.window_x is None or self.window_y is None:
                try:
                    user32 = ctypes.windll.user32
                    screen_width = user32.GetSystemMetrics(0)
                    self.window_x = screen_width - self.width - 10  # 10px from right edge
                    self.window_y = 10  # 10px from top
                except Exception as e:
                    logger.warning("Could not get screen size: %s", str(e))
                    self.window_x = 0
                    self.window_y = 0
            
            # Set window position
            os.environ['SDL_VIDEO_WINDOW_POS'] = f"{self.window_x},{self.window_y}"
            
            # Create a transparent window with per-pixel alpha
            self.screen = pygame.display.set_mode(
                (self.width, self.height),
                pygame.NOFRAME | pygame.SRCALPHA | pygame.HWSURFACE | pygame.DOUBLEBUF
            )
            
            # Set window properties
            pygame.display.set_caption(UIConfig.WINDOW_TITLE)
            
            # Make window click-through and transparent on Windows
            self._make_window_click_through()
            
            logger.info("Celebration window initialized")
            
        except Exception as e:
            logger.error("Failed to initialize window: %s", str(e), exc_info=True)
            raise
    
    def _make_window_click_through(self) -> None:
        """Make the window click-through on Windows."""
        if sys.platform != 'win32':
            return
            
        try:
            import ctypes
            from ctypes import wintypes
            
            # Constants for Windows API
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x00080000
            WS_EX_TRANSPARENT = 0x00000020
            LWA_ALPHA = 0x00000002
            
            # Get window handle
            hwnd = pygame.display.get_wm_info()['window']
            
            # Get current extended style
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            
            # Set new style with layered and transparent flags
            ctypes.windll.user32.SetWindowLongW(
                hwnd,
                GWL_EXSTYLE,
                style | WS_EX_LAYERED | WS_EX_TRANSPARENT
            )
            
            # Set window transparency (0 = fully transparent, 255 = fully opaque)
            ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 255, LWA_ALPHA)
            
            logger.debug("Set window to be click-through")
            
        except Exception as e:
            logger.warning("Could not set window to be click-through: %s", str(e))
    
    def _load_resources(self) -> None:
        """Load any additional resources needed by the window."""
        # This can be expanded to load images, sounds, etc.
        pass
    
    def show_celebration(self, message: str, message_type: str = "milestone") -> None:
        """
        Show a celebration with the given message.
        
        Args:
            message: The message to display
            message_type: Type of celebration (e.g., 'milestone', 'follower', 'subscriber')
        """
        if not self.screen:
            logger.error("Cannot show celebration: window not initialized")
            return
        
        logger.info("Showing celebration: %s (%s)", message, message_type)
        
        # Clear any existing effects
        self.effects.clear()
        
        # Create effects based on message type
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Add a text effect
        self.effects.create_text_effect(
            message,
            center_x,
            center_y - 50,
            duration=UIConfig.ANIMATION_DURATION * 0.8
        )
        
        # Add some particles
        for _ in range(5):
            x = random.randint(100, self.width - 100)
            y = random.randint(100, self.height - 100)
            self.effects.create_explosion(x, y, count=30)
        
        # Add some emoji particles
        emojis = ["🎉", "🎊", "✨", "🌟", "💫", "🎈", "🎆", "🎇"]
        for _ in range(3):
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)
            self.effects.create_emoji_explosion(
                x, y, 
                emoji=random.choice(emojis),
                count=5
            )
    
    def update(self) -> None:
        """Update the window and all effects."""
        if not self.screen:
            return
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        
        # Clear the screen with transparent background
        self.screen.fill((0, 0, 0, 0))
        
        # Update effects
        self.effects.update()
        
        # Draw effects
        self.effects.draw(self.screen)
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        self.clock.tick(UIConfig.FPS)
    
    def run(self) -> None:
        """Run the main window loop."""
        if not self.screen:
            logger.error("Cannot run: window not initialized")
            return
        
        self.running = True
        logger.info("Starting celebration window loop")
        
        try:
            while self.running:
                self.update()
        except KeyboardInterrupt:
            logger.info("Window loop interrupted by user")
        except Exception as e:
            logger.error("Error in window loop: %s", str(e), exc_info=True)
        finally:
            self.cleanup()
    
    def cleanup(self) -> None:
        """Clean up resources."""
        logger.info("Cleaning up celebration window")
        
        # Clean up effects
        if hasattr(self, 'effects'):
            self.effects.cleanup()
        
        # Quit pygame
        pygame.quit()
        self.screen = None
        self.running = False


def main():
    """Run a test of the celebration window."""
    import time
    
    # Set up logging
    from twitch_milestone_celebrator.utils.logging import setup_logger
    setup_logger(level="DEBUG")
    
    # Create and show the window
    window = CelebrationWindow()
    
    # Show a test celebration
    window.show_celebration("Test Celebration!", "test")
    
    # Run for 10 seconds
    start_time = time.time()
    while time.time() - start_time < 10:
        window.update()
    
    # Clean up
    window.cleanup()


if __name__ == "__main__":
    main()
