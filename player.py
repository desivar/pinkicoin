import pygame
import os
from settings import PLAYER_SPEED, GRAVITY, JUMP_STRENGTH, screen_height, tile_size

class player(pygame.sprite.Sprite):
    """
    Player class representing the main character in the game.
    Handles player movement, physics, animations, and states.
    """
    
    def __init__(self, pos):
        """
        Initialize the player with position and default states
        
        Args:
            pos (tuple): Initial position (x, y)
        """
        super().__init__()
        
        # Player states
        self.facing_right = True
        self.on_ground = False
        self.jumping = False
        self.health = 100
        
        # Animation variables
        self.current_frame = 0
        self.animation_speed = 0.15
        self.animation_time = 0
        
        # Load player images
        self.animations = self.load_animations()
        
        # Set initial image from animations or create a fallback
        if self.animations['idle_right']:
            self.image = self.animations['idle_right'][0]
        else:
            self.image = self.create_fallback_image()
            
        # Set up physics and positioning
        self.rect = self.image.get_rect(topleft=pos)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, GRAVITY)
        
        # Collision detection helpers
        self.collision_rect = pygame.Rect(0, 0, self.rect.width - 10, self.rect.height)
        self.collision_rect.midbottom = self.rect.midbottom
        
        # Sound effects
        self.jump_sound = None
        try:
            self.jump_sound = pygame.mixer.Sound('assets/sounds/jump.wav')
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading jump sound: {e}")
    
    def load_animations(self):
        """Load all animation frames for the player"""
        animations = {
            'idle_right': [],
            'idle_left': [],
            'run_right': [],
            'run_left': [],
            'jump_right': [],
            'jump_left': []
        }
        
        # Try to load the wizard sprite for now
        try:
            # For single image (will be expanded for animations)
            wizard_img = pygame.image.load('assets/images/wizard/wizard.jpg').convert_alpha()
            wizard_img = pygame.transform.scale(wizard_img, (50, 50))
            
            # Store the base image for animations
            animations['idle_right'] = [wizard_img]
            
            # Create flipped version for left-facing animations
            animations['idle_left'] = [pygame.transform.flip(wizard_img, True, False)]
            
            # Temporarily use the same image for all states
            animations['run_right'] = [wizard_img]
            animations['run_left'] = [pygame.transform.flip(wizard_img, True, False)]
            animations['jump_right'] = [wizard_img]
            animations['jump_left'] = [pygame.transform.flip(wizard_img, True, False)]
            
        except FileNotFoundError as e:
            print(f"Error loading player images: {e}")
            # Don't exit - we'll use a fallback image
        
        return animations
    
    def create_fallback_image(self):
        """Create a simple shape as fallback if image loading fails"""
        surface = pygame.Surface((50, 50), pygame.SRCALPHA)
        
        # Draw a simple character shape
        pygame.draw.rect(surface, (255, 0, 255), (10, 10, 30, 40))  # Purple body
        pygame.draw.circle(surface, (255, 0, 255), (25, 10), 10)    # Purple head
        
        return surface
    
    def handle_input(self, keys):
        """
        Process keyboard input for player movement
        
        Args:
            keys: pygame key states from pygame.key.get_pressed()
        """
        # Horizontal movement
        self.velocity.x = 0
        
        if keys[pygame.K_LEFT]:
            self.velocity.x = -PLAYER_SPEED
            self.facing_right = False
        
        if keys[pygame.K_RIGHT]:
            self.velocity.x = PLAYER_SPEED
            self.facing_right = True
        
        # Jump - only if on ground
        if keys[pygame.K_UP] and self.on_ground:
            self.jump()
    
    def jump(self):
        """Initiate a jump if the player is on ground"""
        if self.on_ground:
            self.velocity.y = -JUMP_STRENGTH
            self.on_ground = False
            self.jumping = True
            
            # Play jump sound
            if self.jump_sound:
                self.jump_sound.play()
    
    def apply_gravity(self):
        """Apply gravity to the player's vertical movement"""
        self.velocity.y += self.acceleration.y
        
        # Terminal velocity to prevent excessive falling speed
        if self.velocity.y > 15:
            self.velocity.y = 15
    
    def update_animation(self):
        """Update the player's animation based on current state"""
        # Determine animation state
        if not self.on_ground:
            if self.facing_right:
                animation = self.animations['jump_right']
            else:
                animation = self.animations['jump_left']
        elif self.velocity.x != 0:
            if self.facing_right:
                animation = self.animations['run_right']
            else:
                animation = self.animations['run_left']
        else:
            if self.facing_right:
                animation = self.animations['idle_right']
            else:
                animation = self.animations['idle_left']
        
        # Update animation frame
        if animation:
            self.animation_time += self.animation_speed
            if self.animation_time >= len(animation):
                self.animation_time = 0
            
            self.current_frame = int(self.animation_time)
            self.image = animation[min(self.current_frame, len(animation) - 1)]
    
    def check_boundaries(self):
        """Prevent player from moving off screen edges"""
        # Left boundary
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity.x = 0
        
        # Right boundary (assuming screen_width is defined in settings)
        if hasattr(pygame, 'display') and pygame.display.get_surface():
            screen_width = pygame.display.get_surface().get_width()
            if self.rect.right > screen_width:
                self.rect.right = screen_width
                self.velocity.x = 0
        
        # Bottom boundary (for falling)
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.velocity.y = 0
            self.on_ground = True
    
    def update_collision_rect(self):
        """Update the collision rectangle to match player position"""
        self.collision_rect.midbottom = self.rect.midbottom
    
    def update(self):
        """Update player state, position, and animations"""
        # Apply physics
        self.apply_gravity()
        
        # Move horizontally
        self.rect.x += self.velocity.x
        self.update_collision_rect()
        
        # Move vertically
        self.rect.y += self.velocity.y
        self.update_collision_rect()
        
        # Check boundaries
        self.check_boundaries()
        
        # Update animation
        self.update_animation()
    
    def draw(self, surface):
        """Draw the player on the given surface"""
        surface.blit(self.image, self.rect)
        
        # Debug: Draw collision rect (comment out in production)
        # pygame.draw.rect(surface, (255, 0, 0), self.collision_rect, 2)


# Example usage (if this file is run directly)
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Player Test")
    clock = pygame.time.Clock()
    
    # Settings for testing
    GRAVITY = 0.5
    JUMP_STRENGTH = 12
    
    player = player((100, 300))
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        
        player.update()
        
        # Draw
        screen.fill((100, 100, 255))
        player.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()