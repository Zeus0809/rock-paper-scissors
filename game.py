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
FPS = 60
OBJECT_SIZE_RATIO = 1/15  # Objects are 1/15 of screen size
OBJECT_SIZE = int(min(WINDOW_WIDTH, WINDOW_HEIGHT) * OBJECT_SIZE_RATIO)
SPAWN_INTERVAL = 0.1  # seconds
SPEED_INCHES_PER_SEC = 2
DPI = 96  # Standard screen DPI
SPEED_PIXELS_PER_FRAME = (SPEED_INCHES_PER_SEC * DPI) / FPS
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
    def __init__(self, obj_type: ObjectType, x: float, y: float):
        self.type = obj_type
        self.x = x
        self.y = y
        self.radius = OBJECT_SIZE // 2
        
        # Random direction for movement
        angle = random.uniform(0, 2 * math.pi)
        self.vel_x = math.cos(angle) * SPEED_PIXELS_PER_FRAME
        self.vel_y = math.sin(angle) * SPEED_PIXELS_PER_FRAME
        
        # Load sprite
        self.sprite = self.load_sprite()
        
    def load_sprite(self):
        sprite_path = f"assets/sprites/{self.type.value}.png"
        if os.path.exists(sprite_path):
            sprite = pygame.image.load(sprite_path)
            return pygame.transform.scale(sprite, (OBJECT_SIZE, OBJECT_SIZE))
        else:
            # Fallback to colored circles if sprites don't exist
            surface = pygame.Surface((OBJECT_SIZE, OBJECT_SIZE), pygame.SRCALPHA)
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
        
        # Bounce off walls
        if self.x - self.radius <= 0 or self.x + self.radius >= WINDOW_WIDTH:
            self.vel_x = -self.vel_x
            self.x = max(self.radius, min(WINDOW_WIDTH - self.radius, self.x))
            
        if self.y - self.radius <= 100 or self.y + self.radius >= WINDOW_HEIGHT:  # 100px for UI space
            self.vel_y = -self.vel_y
            self.y = max(100 + self.radius, min(WINDOW_HEIGHT - self.radius, self.y))
    
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

class NumberControl:
    def __init__(self, x, y, label, initial_value, min_val, max_val, font):
        self.x = x
        self.y = y
        self.label = label
        self.value = initial_value
        self.min_val = min_val
        self.max_val = max_val
        self.font = font
        
        button_size = 20
        self.up_button = Button(x + 160, y, button_size, button_size, "▲", font)
        self.down_button = Button(x + 160, y + button_size + 2, button_size, button_size, "▼", font)
    
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
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Rock Paper Scissors Battle")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 64)
        
        # Game state
        self.objects: List[GameObject] = []
        self.game_running = False
        self.winner = None
        self.spawn_timer = 0
        self.objects_to_spawn = []
        
        # UI Controls
        self.object_count_control = NumberControl(10, 10, "Objects per type", INITIAL_OBJECT_COUNT, 1, 200, self.font)
        self.new_game_button = Button(10, 50, 100, 30, "New Game", self.font)
    
    def start_new_game(self):
        self.objects.clear()
        self.objects_to_spawn.clear()
        self.game_running = True
        self.winner = None
        self.spawn_timer = 0
        
        count = self.object_count_control.value
        
        # Create spawn queue - spawn from different corners
        spawn_positions = [
            (ObjectType.SCISSORS, 50, WINDOW_HEIGHT - 50),  # Bottom left
            (ObjectType.PAPER, WINDOW_WIDTH - 50, WINDOW_HEIGHT - 50),  # Bottom right
            (ObjectType.ROCK, WINDOW_WIDTH - 50, 150),  # Top right
        ]
        
        for obj_type, base_x, base_y in spawn_positions:
            for i in range(count):
                # Add small random offset to prevent overlap
                x = base_x + random.randint(-30, 30)
                y = base_y + random.randint(-30, 30)
                # Ensure objects stay within bounds
                x = max(OBJECT_SIZE, min(WINDOW_WIDTH - OBJECT_SIZE, x))
                y = max(120, min(WINDOW_HEIGHT - OBJECT_SIZE, y))
                self.objects_to_spawn.append((obj_type, x, y))
        
        # Shuffle to randomize spawn order
        random.shuffle(self.objects_to_spawn)
    
    def update(self, dt):
        if not self.game_running:
            return
        
        # Spawn objects
        if self.objects_to_spawn:
            self.spawn_timer += dt
            if self.spawn_timer >= SPAWN_INTERVAL:
                obj_type, x, y = self.objects_to_spawn.pop(0)
                self.objects.append(GameObject(obj_type, x, y))
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
        
        # Draw UI
        self.object_count_control.draw(self.screen)
        self.new_game_button.draw(self.screen)
        
        # Draw object counts
        counts = self.get_counts()
        count_y = 10
        count_x = 250
        for obj_type in [ObjectType.ROCK, ObjectType.PAPER, ObjectType.SCISSORS]:
            count_text = f"{obj_type.value.capitalize()}: {counts[obj_type]}"
            count_surf = self.font.render(count_text, True, WHITE)
            self.screen.blit(count_surf, (count_x, count_y))
            count_x += 120
        
        # Draw game area border
        pygame.draw.line(self.screen, WHITE, (0, 100), (WINDOW_WIDTH, 100), 2)
        
        # Draw objects
        for obj in self.objects:
            obj.draw(self.screen)
        
        # Draw winner message
        if self.winner:
            winner_text = f"{self.winner.value.capitalize()} Wins!"
            winner_surf = self.big_font.render(winner_text, True, WHITE)
            winner_rect = winner_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            
            # Draw background for text
            bg_rect = winner_rect.inflate(40, 20)
            pygame.draw.rect(self.screen, BLACK, bg_rect)
            pygame.draw.rect(self.screen, WHITE, bg_rect, 3)
            
            self.screen.blit(winner_surf, winner_rect)
        
        pygame.display.flip()
    
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
        
        # Handle UI events
        if self.object_count_control.handle_event(event):
            pass  # Value updated in the control
        
        if self.new_game_button.handle_event(event):
            self.start_new_game()
        
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
