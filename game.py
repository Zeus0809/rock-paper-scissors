import pygame
import random
import math
import sys
import os
from enum import Enum
from typing import List

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600
FPS = 60
OBJECT_SIZE_RATIO = 1/15  # Objects are 1/15 of screen size
OBJECT_SIZE = int(min(WINDOW_WIDTH, WINDOW_HEIGHT) * OBJECT_SIZE_RATIO)  # Default size
SPAWN_INTERVAL = 0.1  # seconds
SPEED_INCHES_PER_SEC = 2
DPI = 96  # Standard screen DPI
SPEED_PIXELS_PER_FRAME = (SPEED_INCHES_PER_SEC * DPI) / FPS  # Default speed
INITIAL_OBJECT_COUNT = 50

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLUE = (100, 100, 255)

class ObjectType(Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"

class GameObject:
    def __init__(self, obj_type: ObjectType, x: float, y: float, game_instance=None):
        self.type = obj_type
        self.x = x
        self.y = y
        self.game = game_instance
        self.radius = (game_instance.object_size if game_instance else OBJECT_SIZE) // 2
        
        # Random direction for movement
        angle = random.uniform(0, 2 * math.pi)
        speed = (game_instance.speed_pixels_per_frame if game_instance else SPEED_PIXELS_PER_FRAME)
        self.vel_x = math.cos(angle) * speed
        self.vel_y = math.sin(angle) * speed
        
        # Load sprite
        self.sprite = self.load_sprite()
        
    def load_sprite(self):
        object_size = (self.game.object_size if self.game else OBJECT_SIZE)
        sprite_path = f"assets/sprites/{self.type.value}.png"
        if os.path.exists(sprite_path):
            sprite = pygame.image.load(sprite_path)
            return pygame.transform.scale(sprite, (object_size, object_size))
        else:
            # Fallback to colored circles if sprites don't exist
            surface = pygame.Surface((object_size, object_size), pygame.SRCALPHA)
            color = {
                ObjectType.ROCK: (100, 100, 100),
                ObjectType.PAPER: (255, 255, 255),
                ObjectType.SCISSORS: (255, 100, 100)
            }[self.type]
            pygame.draw.circle(surface, color, (self.radius, self.radius), self.radius)
            
            # Add simple text label for clarity
            font = pygame.font.Font(None, 16)
            text = font.render(self.type.value[0].upper(), True, BLACK)
            text_rect = text.get_rect(center=(self.radius, self.radius))
            surface.blit(text, text_rect)
            
            return surface
    
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Get current window dimensions
        window_width = self.game.window_width if self.game else WINDOW_WIDTH
        window_height = self.game.window_height if self.game else WINDOW_HEIGHT
        
        # Bounce off walls
        if self.x - self.radius <= 0 or self.x + self.radius >= window_width:
            self.vel_x = -self.vel_x
            self.x = max(self.radius, min(window_width - self.radius, self.x))
            
        if self.y - self.radius <= 100 or self.y + self.radius >= window_height:  # 100px for UI space
            self.vel_y = -self.vel_y
            self.y = max(100 + self.radius, min(window_height - self.radius, self.y))
    
    def draw(self, screen):
        screen.blit(self.sprite, (self.x - self.radius, self.y - self.radius))
    
    def get_distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def collides_with(self, other):
        return self.get_distance(other) < (self.radius + other.radius)
    
    def convert_to_type(self, new_type: ObjectType):
        """Convert this object to a different type, keeping position and velocity"""
        self.type = new_type
        self.sprite = self.load_sprite()

class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.pressed = False
        
    def draw(self, screen):
        color = GRAY if self.pressed else LIGHT_GRAY
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, DARK_GRAY, self.rect, 2)
        
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False
        return False

class ArrowButton:
    def __init__(self, x, y, width, height, direction, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.direction = direction  # "up" or "down"
        self.font = font
        self.pressed = False
        self.hovered = False
        
    def draw(self, screen):
        # Determine colors based on state
        if self.pressed:
            bg_color = (150, 150, 150)
            border_color = (80, 80, 80)
            arrow_color = BLACK
        elif self.hovered:
            bg_color = (220, 220, 220)
            border_color = (100, 100, 100)
            arrow_color = BLACK
        else:
            bg_color = LIGHT_GRAY
            border_color = DARK_GRAY
            arrow_color = BLACK
        
        # Draw button background
        pygame.draw.rect(screen, bg_color, self.rect)
        pygame.draw.rect(screen, border_color, self.rect, 1)
        
        # Draw arrow using triangles
        center_x = self.rect.centerx
        center_y = self.rect.centery
        arrow_size = min(self.rect.width, self.rect.height) // 3
        
        if self.direction == "up":
            # Up arrow triangle
            points = [
                (center_x, center_y - arrow_size),  # Top point
                (center_x - arrow_size, center_y + arrow_size // 2),  # Bottom left
                (center_x + arrow_size, center_y + arrow_size // 2)   # Bottom right
            ]
        else:  # down
            # Down arrow triangle
            points = [
                (center_x, center_y + arrow_size),  # Bottom point
                (center_x - arrow_size, center_y - arrow_size // 2),  # Top left
                (center_x + arrow_size, center_y - arrow_size // 2)   # Top right
            ]
        
        pygame.draw.polygon(screen, arrow_color, points)
    
    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False
        return False

class NumberControl:
    def __init__(self, x, y, label, initial_value, min_val, max_val, font):
        self.x = x
        self.y = y
        self.label = label
        self.value = initial_value
        self.min_val = min_val
        self.max_val = max_val
        self.font = font
        
        button_size = 22
        self.up_button = ArrowButton(x + 160, y, button_size, button_size, "up", font)
        self.down_button = ArrowButton(x + 160, y + button_size + 2, button_size, button_size, "down", font)
    
    def draw(self, screen):
        label_surf = self.font.render(f"{self.label}: {self.value}", True, WHITE)
        screen.blit(label_surf, (self.x, self.y + 8))
        
        self.up_button.draw(screen)
        self.down_button.draw(screen)
    
    def handle_event(self, event):
        if self.up_button.handle_event(event):
            self.value = min(self.max_val, self.value + 1)
            return True
        elif self.down_button.handle_event(event):
            self.value = max(self.min_val, self.value - 1)
            return True
        return False

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Rock Paper Scissors Battle")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 64)
        
        # Current window dimensions (will be updated on resize)
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        self.is_fullscreen = False
        
        # Game state (initialize before calling update_window_dependent_values)
        self.objects: List[GameObject] = []
        self.game_running = False
        self.game_paused = False
        self.winner = None
        self.spawn_timer = 0
        self.objects_to_spawn = []
        
        # Recalculate dynamic values (after objects list is initialized)
        self.update_window_dependent_values()
        
        # UI Controls - repositioned for better layout
        self.object_count_control = NumberControl(20, 20, "Objects per type", INITIAL_OBJECT_COUNT, 1, 200, self.font)
        
        # Buttons positioned on the right side in a column
        button_width = 100
        button_height = 35
        button_margin = 10
        self.new_game_button = Button(self.window_width - button_width - 20, 15, button_width, button_height, "New Game", self.font)
        self.pause_button = Button(self.window_width - button_width - 20, 15 + button_height + button_margin, button_width, button_height, "Pause", self.font)
    
    def update_window_dependent_values(self):
        """Update values that depend on window size"""
        self.object_size = int(min(self.window_width, self.window_height) * OBJECT_SIZE_RATIO)
        self.speed_pixels_per_frame = (SPEED_INCHES_PER_SEC * DPI) / FPS
        
        # Update button positions for new window size
        self.update_ui_positions()
        
        # Update all existing objects' sprites to new size
        for obj in self.objects:
            obj.radius = self.object_size // 2
            obj.sprite = obj.load_sprite()
    
    def update_ui_positions(self):
        """Update UI element positions based on current window size"""
        # Only update button positions if they exist
        if hasattr(self, 'new_game_button') and hasattr(self, 'pause_button'):
            button_width = 100
            button_height = 35
            button_margin = 10
            
            # Reposition buttons on the right side
            self.new_game_button.rect.x = self.window_width - button_width - 20
            self.new_game_button.rect.y = 15
            
            self.pause_button.rect.x = self.window_width - button_width - 20
            self.pause_button.rect.y = 15 + button_height + button_margin
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        
        # Update window dimensions
        self.window_width, self.window_height = self.screen.get_size()
        self.update_window_dependent_values()
    
    def handle_resize(self, new_width, new_height):
        """Handle window resize event"""
        # Enforce minimum window size
        new_width = max(MIN_WINDOW_WIDTH, new_width)
        new_height = max(MIN_WINDOW_HEIGHT, new_height)
        
        self.window_width = new_width
        self.window_height = new_height
        self.update_window_dependent_values()
        
        # Keep objects within new bounds
        for obj in self.objects:
            obj.x = max(obj.radius, min(self.window_width - obj.radius, obj.x))
            obj.y = max(100 + obj.radius, min(self.window_height - obj.radius, obj.y))
    
    def start_new_game(self):
        self.objects.clear()
        self.objects_to_spawn.clear()
        self.game_running = True
        self.game_paused = False
        self.winner = None
        self.spawn_timer = 0
        
        # Update pause button text
        self.pause_button.text = "Pause"
        
        count = self.object_count_control.value
        
        # Create spawn queue - spawn from different corners using current window size
        spawn_positions = [
            (ObjectType.SCISSORS, 50, self.window_height - 50),  # Bottom left
            (ObjectType.PAPER, self.window_width - 50, self.window_height - 50),  # Bottom right
            (ObjectType.ROCK, self.window_width - 50, 130),  # Top right (below header)
        ]
        
        # Create spawn batches - each batch contains one of each type
        for i in range(count):
            batch = []
            for obj_type, base_x, base_y in spawn_positions:
                # Add small random offset to prevent overlap
                x = base_x + random.randint(-30, 30)
                y = base_y + random.randint(-30, 30)
                # Ensure objects stay within bounds using current window size
                x = max(self.object_size, min(self.window_width - self.object_size, x))
                y = max(120, min(self.window_height - self.object_size, y))
                batch.append((obj_type, x, y))
            
            # Shuffle the order within each batch for visual variety
            random.shuffle(batch)
            self.objects_to_spawn.append(batch)
    
    def update(self, dt):
        if not self.game_running or self.game_paused:
            return
        
        # Spawn objects
        if self.objects_to_spawn:
            self.spawn_timer += dt
            if self.spawn_timer >= SPAWN_INTERVAL:
                # Spawn an entire batch (one of each type) simultaneously
                batch = self.objects_to_spawn.pop(0)
                for obj_type, x, y in batch:
                    self.objects.append(GameObject(obj_type, x, y, self))
                self.spawn_timer = 0
        
        # Update objects
        for obj in self.objects:
            obj.update()
        
        # Check collisions
        converted_objects = []
        for i, obj1 in enumerate(self.objects):
            for j, obj2 in enumerate(self.objects[i+1:], i+1):
                if obj1.collides_with(obj2):
                    winner_obj, loser_idx = self.determine_winner(obj1, obj2, i, j)
                    if loser_idx is not None:
                        # Convert the loser to the winner's type
                        loser_obj = self.objects[loser_idx]
                        converted_objects.append((loser_idx, winner_obj.type))
        
        # Apply conversions
        for loser_idx, winner_type in converted_objects:
            if loser_idx < len(self.objects):
                self.objects[loser_idx].convert_to_type(winner_type)
        
        # Check win condition
        if self.objects and not self.objects_to_spawn:
            remaining_types = set(obj.type for obj in self.objects)
            if len(remaining_types) == 1:
                self.winner = list(remaining_types)[0]
                self.game_running = False
    
    def determine_winner(self, obj1, obj2, idx1, idx2):
        # Rock beats Scissors, Scissors beats Paper, Paper beats Rock
        if obj1.type == obj2.type:
            return obj1, None  # Same type, no winner
        
        rules = {
            (ObjectType.ROCK, ObjectType.SCISSORS): (obj1, idx2),
            (ObjectType.SCISSORS, ObjectType.PAPER): (obj1, idx2),
            (ObjectType.PAPER, ObjectType.ROCK): (obj1, idx2),
            (ObjectType.SCISSORS, ObjectType.ROCK): (obj2, idx1),
            (ObjectType.PAPER, ObjectType.SCISSORS): (obj2, idx1),
            (ObjectType.ROCK, ObjectType.PAPER): (obj2, idx1),
        }
        
        return rules.get((obj1.type, obj2.type), (obj1, None))
    
    def get_counts(self):
        counts = {ObjectType.ROCK: 0, ObjectType.PAPER: 0, ObjectType.SCISSORS: 0}
        for obj in self.objects:
            counts[obj.type] += 1
        return counts
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw UI elements
        self.object_count_control.draw(self.screen)
        self.new_game_button.draw(self.screen)
        self.pause_button.draw(self.screen)
        
        # Draw centered object counts with larger text
        counts = self.get_counts()
        stats_font = pygame.font.Font(None, 32)  # Larger font for stats
        stats_y = 25
        
        # Calculate total width needed for all stats
        stat_texts = []
        stat_widths = []
        for obj_type in [ObjectType.ROCK, ObjectType.PAPER, ObjectType.SCISSORS]:
            text = f"{obj_type.value.capitalize()}: {counts[obj_type]}"
            stat_texts.append(text)
            text_surf = stats_font.render(text, True, WHITE)
            stat_widths.append(text_surf.get_width())
        
        total_stats_width = sum(stat_widths) + 60  # 30px spacing between each stat
        start_x = (self.window_width - total_stats_width) // 2
        
        # Draw each stat centered
        current_x = start_x
        for i, (text, width) in enumerate(zip(stat_texts, stat_widths)):
            text_surf = stats_font.render(text, True, WHITE)
            self.screen.blit(text_surf, (current_x, stats_y))
            current_x += width + 30  # Move to next position with spacing
        
        # Draw game area border (higher to accommodate larger header with stacked buttons)
        border_y = 100
        pygame.draw.line(self.screen, WHITE, (0, border_y), (self.window_width, border_y), 2)
        
        # Draw objects
        for obj in self.objects:
            obj.draw(self.screen)
        
        # Draw winner message
        if self.winner:
            winner_text = f"{self.winner.value.capitalize()} Wins!"
            winner_surf = self.big_font.render(winner_text, True, WHITE)
            winner_rect = winner_surf.get_rect(center=(self.window_width // 2, self.window_height // 2))
            
            # Draw background for text
            bg_rect = winner_rect.inflate(40, 20)
            pygame.draw.rect(self.screen, BLACK, bg_rect)
            pygame.draw.rect(self.screen, WHITE, bg_rect, 3)
            
            self.screen.blit(winner_surf, winner_rect)
        
        # Draw pause message
        elif self.game_paused:
            pause_text = "PAUSED"
            pause_surf = self.big_font.render(pause_text, True, WHITE)
            pause_rect = pause_surf.get_rect(center=(self.window_width // 2, self.window_height // 2))
            
            # Draw background for text
            bg_rect = pause_rect.inflate(40, 20)
            pygame.draw.rect(self.screen, BLACK, bg_rect)
            pygame.draw.rect(self.screen, WHITE, bg_rect, 3)
            
            self.screen.blit(pause_surf, pause_rect)
        
        pygame.display.flip()
    
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
        
        # Handle window resize
        elif event.type == pygame.VIDEORESIZE:
            self.handle_resize(event.w, event.h)
        
        # Handle fullscreen toggle (F11 or Alt+Enter)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11 or (event.key == pygame.K_RETURN and event.mod & pygame.KMOD_ALT):
                self.toggle_fullscreen()
        
        # Handle UI events
        if self.object_count_control.handle_event(event):
            pass  # Value updated in the control
        
        if self.new_game_button.handle_event(event):
            self.start_new_game()
        
        if self.pause_button.handle_event(event):
            if self.game_running and not self.winner:
                self.game_paused = not self.game_paused
                self.pause_button.text = "Resume" if self.game_paused else "Pause"
        
        return True
    
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            # Handle events
            for event in pygame.event.get():
                if not self.handle_event(event):
                    running = False
            
            # Update game
            self.update(dt)
            
            # Draw everything
            self.draw()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
