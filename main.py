import pygame
import sys
import os
from settings import (
    screen_width, screen_height, tile_size, fps, game_title
)
from player import player
from coin import coin  # Import the Coin class


try:
    from assets.levels.level import level
except ImportError as e:
    print(f"Error importing level module: {e}")
    pygame.quit()


class Game:
    """Main game class to manage the game loop and resources""" 
    def __init__(self):
        """Initialize the game, including pygame, display, and game resources"""
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()
        
        # Set up display
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(game_title)
        self.clock = pygame.time.Clock()
        
        # Game states
        self.running = True
        self.paused = False
        self.current_level = 1
        self.max_levels = 3  # Set the number of available levels
        self.score = 0
        
        # Load assets
        self.load_assets()
        
        # Initialize game objects
        self.player = player(
            (100, screen_height - 2 * tile_size)
        )
        
        # Preload coin images
        coin.preload_images()
        
        # Set up the first level
        self.setup_level(self.current_level)
        
        # UI elements
        self.font = pygame.font.Font(None, 36)
        
    def load_assets(self):
        """Load game assets like images and sounds"""
        self.background_image = pygame.image.load(
            'assets/images/background/clouds1.jpg'
        ).convert()
        try:
            self.background_image = pygame.image.load(
                'assets/images/background/clouds1.jpg'
            ).convert()
            self.background_image = pygame.transform.scale(
                self.background_image, (screen_width, screen_height)
            )
        except FileNotFoundError as e:
            print(f"Error loading background: {e}")
            self.background_image = self.create_fallback_background()
        
            pygame.mixer.music.load(
                'assets/sounds/piano-melody-277609.mp3'
            )
        self.sounds = {}
        try:
            # Load music
            pygame.mixer.music.load('assets/sounds/piano-melody-277609.mp3')
            pygame.mixer.music.set_volume(0.5)  # Set to 50% volume
            self.sounds['coin_collect'] = pygame.mixer.Sound(
                'assets/sounds/coin_collect.wav'
            )
            self.sounds['jump'] = pygame.mixer.Sound(
                'assets/sounds/jump.wav'
            )
            self.sounds['level_complete'] = pygame.mixer.Sound(
                'assets/sounds/level_complete.wav'
            )
            self.sounds['jump'] = pygame.mixer.Sound('assets/sounds/jump.wav')
            self.sounds['level_complete'] = pygame.mixer.Sound(
                'assets/sounds/level_complete.wav'
            )
        except pygame.error as e:
            print(f"Error loading sounds: {e}")
    
    def create_fallback_background(self):
        """Create a simple gradient background if image fails to load"""
        bg = pygame.Surface((screen_width, screen_height))
        for y in range(screen_height):
            # Create a blue to light blue gradient
            color = (100, 100, 255 - int(y * 0.3))
            pygame.draw.line(bg, color, (0, y), (screen_width, y))
        return bg
    
    def setup_level(self, level_number):
        """Load and set up the specified level"""
        # Example of loading different levels
        level_file = f'assets/levels/level{level_number}.txt'
        
        # Check if level file exists, otherwise use hardcoded level data
        if os.path.exists(level_file):
            with open(level_file, 'r') as f:
                level_data = f.read().splitlines()
        else:
            # Fallback level data (can be customized for each level)
            if level_number == 1:
                level_data = [
                    "####################",
                    "#                  #",
                    "#  c g b           #",
                    "# ######   ####    #",
                    "#        c         #",
                    "####################",
                ]
            elif level_number == 2:
                level_data = [
                    "####################",
                    "#       g          #",
                    "#  c    #    b     #",
                    "# #### ### ###     #",
                    "#      c      g    #",
                    "####################",
                ]
            else:
                level_data = [
                    "####################",
                    "#       g g g      #",
                    "# c b c # # # b c  #",
                    "####### # # ###### #",
                    "#           g      #",
                    "####################",
                ]
        
        # Create the level
        self.level = Level(level_data, self.player)
        
        # Reset player position
        self.player.rect.topleft = (100, screen_height - 2 * tile_size)
        self.player.velocity.y = 0
    
    def start_music(self):
        """Start the background music"""
        pygame.mixer.music.play(-1)  # Play on loop
    
    def handle_events(self):
        """Process game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    if self.paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                
                # Debug: Level skip
                elif event.key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.next_level()
        
        # Handle continuous key presses when not paused
        if not self.paused:
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys)
    
    def update(self):
        """Update game state"""
        if self.paused:
            return
            
        # Update game objects
        self.player.update()
        
        # Update level and check for coins collected
        coins_collected = self.level.update()
        if coins_collected:
            self.score += coins_collected
            if 'coin_collect' in self.sounds:
                self.sounds['coin_collect'].play()
        
        # Check for level completion (example: all coins collected)
        if self.level.is_complete():
            self.next_level()
    
    def next_level(self):
        """Advance to the next level or end game if all levels completed"""
        if self.current_level < self.max_levels:
            if 'level_complete' in self.sounds:
                self.sounds['level_complete'].play()
            self.current_level += 1
            self.setup_level(self.current_level)
        else:
            # Game completed - could show victory screen
            print("Game completed! Final score:", self.score)
            # For now, we'll just reset to level 1
            self.current_level = 1
            self.setup_level(self.current_level)
    
    def draw_ui(self):
        """Draw user interface elements"""
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 20))
        
        # Level indicator
        level_text = self.font.render(f"Level: {self.current_level}/{self.max_levels}", True, (255, 255, 255))
        self.screen.blit(level_text, (screen_width - 150, 20))
        
        # Pause indicator
        if self.paused:
            pause_text = self.font.render("PAUSED", True, (255, 0, 0))
            text_rect = pause_text.get_rect(center=(screen_width // 2, screen_height // 2))
            # Draw semi-transparent background
            s = pygame.Surface((pause_text.get_width() + 20, pause_text.get_height() + 20))
            s.set_alpha(150)
            s.fill((0, 0, 0))
            self.screen.blit(s, (text_rect.x - 10, text_rect.y - 10))
            self.screen.blit(pause_text, text_rect)
    
    def draw(self):
        """Draw all game elements"""
        # Background
        self.screen.blit(self.background_image, (0, 0))
        
        # Game elements
        self.level.draw(self.screen)
        self.player.draw(self.screen)
        
        # UI
        self.draw_ui()
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        self.start_music()
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(fps)
        
        self.quit()
    
    def quit(self):
        """Clean up and exit"""
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    # Create and run the game
    game = Game()
    game.run()