"""Visual effects and utilities for the Twitch Milestone Celebrator."""
import math
import random
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import pygame

from twitch_milestone_celebrator.config.settings import UIConfig
from twitch_milestone_celebrator.utils.logging import get_logger

logger = get_logger("visuals")

# Type aliases
Color = Tuple[int, int, int, int]  # RGBA
Position = Tuple[float, float]  # x, y
Velocity = Tuple[float, float]  # vx, vy


@dataclass
class Particle:
    """A single particle for visual effects."""
    
    x: float
    y: float
    vx: float
    vy: float
    color: Color
    size: float
    life: float = 1.0
    decay: float = 0.02
    gravity: float = 0.1
    
    def update(self) -> bool:
        """
        Update the particle's position and life.
        
        Returns:
            bool: True if the particle is still alive, False if it should be removed
        """
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.life -= self.decay
        
        return self.life > 0
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the particle on the given surface."""
        alpha = int(255 * self.life)
        color = (*self.color[:3], alpha)
        
        # Draw a circle for the particle
        pygame.draw.circle(
            surface,
            color,
            (int(self.x), int(self.y)),
            int(self.size * self.life)  # Shrink as life decreases
        )


@dataclass
class EmojiParticle:
    """A particle that displays an emoji character."""
    
    x: float
    y: float
    vx: float
    vy: float
    emoji: str
    font: pygame.font.Font
    color: Color = (255, 255, 255, 255)
    life: float = 1.0
    decay: float = 0.01
    gravity: float = 0.1
    rotation: float = 0.0
    rotation_speed: float = 0.0
    scale: float = 1.0
    
    def __post_init__(self):
        """Initialize the emoji surface."""
        self.text_surface = self.font.render(self.emoji, True, self.color[:3])
        self.original_surface = self.text_surface.copy()
        self.rect = self.text_surface.get_rect(center=(self.x, self.y))
    
    def update(self) -> bool:
        """
        Update the emoji's position, rotation, and life.
        
        Returns:
            bool: True if the emoji is still alive, False if it should be removed
        """
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.life -= self.decay
        self.rotation += self.rotation_speed
        
        # Update alpha based on life
        alpha = int(255 * self.life)
        self.text_surface = self.original_surface.copy()
        self.text_surface.set_alpha(alpha)
        
        # Apply rotation and scale
        if self.rotation != 0 or self.scale != 1.0:
            # Scale first
            if self.scale != 1.0:
                new_width = int(self.original_surface.get_width() * self.scale)
                new_height = int(self.original_surface.get_height() * self.scale)
                self.text_surface = pygame.transform.scale(
                    self.text_surface, 
                    (new_width, new_height)
                )
            
            # Then rotate
            if self.rotation != 0:
                self.text_surface = pygame.transform.rotate(
                    self.text_surface, 
                    self.rotation * 180 / math.pi  # Convert to degrees
                )
        
        # Update the rect for drawing
        self.rect = self.text_surface.get_rect(center=(self.x, self.y))
        
        return self.life > 0
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the emoji on the given surface."""
        surface.blit(self.text_surface, self.rect)


class VisualEffects:
    """Manages visual effects for the Twitch Milestone Celebrator."""
    
    def __init__(self):
        """Initialize the visual effects manager."""
        self.particles: List[Particle] = []
        self.emoji_particles: List[EmojiParticle] = []
        self.effects: List[dict] = []
        self.screen: Optional[pygame.Surface] = None
        self.clock = pygame.time.Clock()
        self.running = False
        self.last_update = pygame.time.get_ticks()
        
        # Load fonts
        try:
            self.title_font = pygame.font.SysFont(
                UIConfig.FONT_NAME, 
                UIConfig.TITLE_FONT_SIZE, 
                bold=True
            )
            self.subtitle_font = pygame.font.SysFont(
                UIConfig.FONT_NAME, 
                UIConfig.SUBTITLE_FONT_SIZE
            )
            self.emoji_font = pygame.font.SysFont("segoe ui emoji", 36)
        except Exception as e:
            logger.error("Failed to load fonts: %s", str(e))
            # Fallback to default fonts
            self.title_font = pygame.font.SysFont(None, 72, bold=True)
            self.subtitle_font = pygame.font.SysFont(None, 28)
            self.emoji_font = pygame.font.SysFont(None, 36)
    
    def create_explosion(self, x: float, y: float, color: Optional[Color] = None, 
                        count: int = 50, size: float = 5.0) -> None:
        """
        Create an explosion effect at the given position.
        
        Args:
            x: X coordinate of the explosion
            y: Y coordinate of the explosion
            color: Color of the particles (random if None)
            count: Number of particles to create
            size: Base size of the particles
        """
        color = color or random.choice(UIConfig.COLORS)
        
        for _ in range(count):
            # Random angle and speed
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            
            # Create particle with random velocity
            self.particles.append(Particle(
                x=x,
                y=y,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                color=color,
                size=random.uniform(size * 0.5, size * 1.5),
                decay=random.uniform(0.01, 0.05),
                gravity=random.uniform(0.05, 0.2)
            ))
    
    def create_emoji_explosion(self, x: float, y: float, emoji: str = "🎉", 
                             count: int = 10) -> None:
        """
        Create an explosion of emoji characters.
        
        Args:
            x: X coordinate of the explosion
            y: Y coordinate of the explosion
            emoji: Emoji character to use
            count: Number of emojis to create
        """
        for _ in range(count):
            # Random angle and speed
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 5)
            
            # Create emoji particle with random velocity
            self.emoji_particles.append(EmojiParticle(
                x=x,
                y=y,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                emoji=emoji,
                font=self.emoji_font,
                color=random.choice(UIConfig.COLORS),
                decay=random.uniform(0.005, 0.02),
                gravity=random.uniform(0.05, 0.2),
                rotation_speed=random.uniform(-0.1, 0.1),
                scale=random.uniform(0.5, 1.5)
            ))
    
    def create_text_effect(self, text: str, x: float, y: float, 
                         color: Optional[Color] = None, duration: float = 3.0) -> None:
        """
        Create a text effect at the given position.
        
        Args:
            text: Text to display
            x: X coordinate of the text
            y: Y coordinate of the text
            color: Color of the text (random if None)
            duration: How long the effect should last in seconds
        """
        color = color or random.choice(UIConfig.COLORS)
        text_surface = self.title_font.render(text, True, color[:3])
        
        self.effects.append({
            'type': 'text',
            'surface': text_surface,
            'rect': text_surface.get_rect(center=(x, y)),
            'created_at': pygame.time.get_ticks(),
            'duration': duration * 1000,  # Convert to milliseconds
            'alpha': 255
        })
    
    def update(self) -> None:
        """Update all visual effects."""
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_update) / 1000.0  # Convert to seconds
        self.last_update = current_time
        
        # Update particles
        self.particles = [p for p in self.particles if p.update()]
        
        # Update emoji particles
        self.emoji_particles = [e for e in self.emoji_particles if e.update()]
        
        # Update effects
        current_time = pygame.time.get_ticks()
        for effect in self.effects[:]:
            age = current_time - effect['created_at']
            
            # Remove old effects
            if age > effect['duration']:
                self.effects.remove(effect)
                continue
            
            # Update effect properties (e.g., fade out)
            if 'alpha' in effect:
                # Fade out based on remaining life
                life_remaining = 1.0 - (age / effect['duration'])
                effect['alpha'] = int(255 * life_remaining)
                
                # Apply alpha to surface
                if 'surface' in effect:
                    effect['surface'].set_alpha(effect['alpha'])
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw all visual effects on the given surface.
        
        Args:
            surface: The surface to draw on
        """
        # Draw particles
        for particle in self.particles:
            particle.draw(surface)
        
        # Draw emoji particles
        for emoji in self.emoji_particles:
            emoji.draw(surface)
        
        # Draw effects
        for effect in self.effects:
            if 'surface' in effect and 'rect' in effect:
                surface.blit(effect['surface'], effect['rect'])
    
    def clear(self) -> None:
        """Clear all visual effects."""
        self.particles.clear()
        self.emoji_particles.clear()
        self.effects.clear()
    
    def cleanup(self) -> None:
        """Clean up resources."""
        self.clear()
        if self.screen is not None:
            pygame.display.quit()
            self.screen = None
