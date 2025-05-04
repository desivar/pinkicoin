import pygame
import os
from settings import tile_size, TILE_MAPPING, COLOR_PLATFORM, COIN_VALUES, DEBUG
from coin import coin


class Level:
    """
    Level class that handles level generation, collision detection,
    and managing all game objects within a level.
    """
    
    def __init__(self, level_data, player):
        """
        Initialize the level with data and player reference
        
        Args:
            level_data: List of strings representing the level layout
            player: Player object reference for collision handling
        """
        # Store references
        self.level_data = level_data
        self.player = player
        
        # Create sprite groups
        self.tiles = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.trampolines = pygame.sprite.Group()
        self.finish_points = pygame.sprite.Group()
        
        # Level state
        self.collected_coins = 0
        self.total_coins = 0
        self.level_complete = False
        
        # Load the level from data
        self.load_level()
    
    def load_level(self):
        """Parse level data and create game objects"""
        for row_index, row in enumerate(self.level_data):
            for col_index, tile_char in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                
                # Process different tile types based on character
                if tile_char == '#':
                    # Wall/platform tile
                    tile = Tile((x, y))
                    self.tiles.add(tile)
                
                elif tile_char in ['c', 's', 'g', 'b']:  # Different coin types
                    # Map tile characters to coin types
                    coin_type = {
                        'c': 'bronze',
                        's': 'silver',
                        'g': 'gold',
                        'b': 'bronze'  # Backward compatibility with 'B'
                    }.get(tile_char.lower(), 'silver')
                    
                    # Create coin at center of tile
                    coin_pos = (x + tile_size // 2, y + tile_size // 2)
                    coin = coin(coin_pos, coin_type)
                    self.coins.add(coin)
                    self.total_coins += 1
                
                elif tile_char == 'h':
                    # Health powerup
                    from powerup import HealthPowerup
                    health = HealthPowerup((x + tile_size // 2, y + tile_size // 2))
                    self.powerups.add(health)
                
                elif tile_char == 'w':
                    # Water hazard
                    from hazard import WaterHazard
                    water = WaterHazard((x, y))
                    self.hazards.add(water)
                
                elif tile_char == 't':
                    # Trampoline
                    from special_tile import Trampoline
                    trampoline = Trampoline((x, y))
                    self.trampolines.add(trampoline)
                
                elif tile_char == 'e':
                    # Enemy
                    from enemy import Enemy
                    enemy = Enemy((x, y), self.tiles)
                    self.enemies.add(enemy)
                
                elif tile_char == 'f':
                    # Level finish point
                    from special_tile import FinishPoint
                    finish = FinishPoint((x, y))
                    self.finish_points.add(finish)
                
                elif tile_char == 'p':
                    # Player start position
                    self.player.rect.topleft = (x, y)
                    self.player.velocity.y = 0
    
    def check_coin_collisions(self):
        """Check for collisions between player and coins"""
        collected_value = 0
        current_time = pygame.time.get_ticks()
        
        # Check each coin for collision with player
        for coin in self.coins:
            if not coin.is_collected and coin.rect.colliderect(self.player.rect):
                # Collect the coin and get its value
                value = coin.collect(current_time)
                collected_value += value
                self.collected_coins += 1
        
        return collected_value
    
    def check_player_collisions(self):
        """Handle all player collisions with level objects"""
        self._check_horizontal_collisions()
        self._check_vertical_collisions()
        
        # Check special tile interactions
        self._check_trampoline_collisions()
        self._check_hazard_collisions()
        self._check_powerup_collisions()
        self._check_finish_point_collisions()
    
    def _check_horizontal_collisions(self):
        """Handle horizontal collisions with tiles"""
        player = self.player
        player.collision_rect.x += player.velocity.x
        
        # Check collisions with tiles
        for tile in self.tiles:
            if tile.rect.colliderect(player.collision_rect):
                # Handle collision based on direction
                if player.velocity.x > 0:  # Moving right
                    player.collision_rect.right = tile.rect.left
                elif player.velocity.x < 0:  # Moving left
                    player.collision_rect.left = tile.rect.right
                
                # Stop horizontal movement
                player.velocity.x = 0
        
        # Update player rect to match collision rect
        player.rect.centerx = player.collision_rect.centerx
    
    def _check_vertical_collisions(self):
        """Handle vertical collisions with tiles"""
        player = self.player
        # Apply gravity first
        player.velocity.y += player.acceleration.y
        
        # Apply vertical velocity
        player.collision_rect.y += player.velocity.y
        
        # Reset ground state
        player.on_ground = False
        
        # Check collisions with tiles
        for tile in self.tiles:
            if tile.rect.colliderect(player.collision_rect):
                # Handle collision based on direction
                if player.velocity.y > 0:  # Falling
                    player.collision_rect.bottom = tile.rect.top
                    player.velocity.y = 0
                    player.on_ground = True  # Mark as on ground when landing
                    player.jumping = False
                elif player.velocity.y < 0:  # Jumping/moving up
                    player.collision_rect.top = tile.rect.bottom
                    player.velocity.y = 0  # Stop upward movement
        
        # Update player rect to match collision rect
        player.rect.bottom = player.collision_rect.bottom
    
    def _check_trampoline_collisions(self):
        """Check for collisions with trampolines"""
        for trampoline in self.trampolines:
            if self.player.collision_rect.colliderect(trampoline.rect) and self.player.velocity.y > 0:
                # Bounce the player
                self.player.velocity.y = -20  # Strong upward force
                trampoline.activate()  # Trigger trampoline animation
    
    def _check_hazard_collisions(self):
        """Check for collisions with hazards"""
        for hazard in self.hazards:
            if self.player.collision_rect.colliderect(hazard.rect):
                # Apply damage to player
                hazard.apply_effect(self.player)
    
    def _check_powerup_collisions(self):
        """Check for collisions with powerups"""
        for powerup in self.powerups:
            if self.player.collision_rect.colliderect(powerup.rect) and not powerup.collected:
                # Apply powerup effect
                powerup.apply(self.player)
    
    def _check_finish_point_collisions(self):
        """Check if player has reached the finish point"""
        for finish in self.finish_points:
            if self.player.collision_rect.colliderect(finish.rect):
                self.level_complete = True
    
    def is_complete(self):
        """Check if the level is completed"""
        # Level can be completed by reaching finish point or collecting all coins
        all_coins_collected = self.collected_coins >= self.total_coins and self.total_coins > 0
        return self.level_complete or all_coins_collected
    
    def update(self):
        """Update all level elements and check collisions"""
        # Update all sprite groups
        self.coins.update(pygame.time.get_ticks())
        self.enemies.update()
        self.powerups.update()
        self.hazards.update()
        self.trampolines.update()
        
        # Check collisions
        self.check_player_collisions()
        collected_value = self.check_coin_collisions()
        
        # Return coin value for score updating in main game
        return collected_value
    
    def draw(self, surface):
        """Draw all level elements to the screen"""
        # Draw all sprite groups
        self.tiles.draw(surface)
        
        # Draw special tiles
        self.trampolines.draw(surface)
        self.hazards.draw(surface)
        self.finish_points.draw(surface)
        
        # Draw enemies and powerups
        self.enemies.draw(surface)
        self.powerups.draw(surface)
        
        # Draw coins last (on top)
        for coin in self.coins:
            coin.draw(surface)
        
        # Debug drawing
        if DEBUG:
            self._draw_debug(surface)
    
    def _draw_debug(self, surface):
        """Draw debug information"""
        for tile in self.tiles:
            pygame.draw.rect(surface, (255, 0, 0), tile.rect, 1)


class Tile(pygame.sprite.Sprite):
    """Class representing a solid tile in the level"""
    
    def __init__(self, pos):
        """
        Initialize a tile
        
        Args:
            pos (tuple): Position (x, y) for the tile
        """
        super().__init__()
        
        # Try to load the tile image
        image_path = 'assets/images/tiles/ground.png'
        try:
            if os.path.exists(image_path):
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
            else:
                # Create fallback tile if image not found
                self.image = self._create_fallback_tile()
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading tile image: {e}")
            self.image = self._create_fallback_tile()
        
        # Set up the tile's rectangle
        self.rect = self.image.get_rect(topleft=pos)
    
    def _create_fallback_tile(self):
        """Create a simple colored square as fallback"""
        surface = pygame.Surface((tile_size, tile_size))
        surface.fill(COLOR_PLATFORM)
        
        # Add a border
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, tile_size, tile_size), 1)
        return surface


# These are placeholder classes that would be implemented in separate files
# I'm including them to show how they'd integrate with the level class

class HealthPowerup(pygame.sprite.Sprite):
    """Placeholder for a health powerup"""
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))  # Green for health
        self.rect = self.image.get_rect(center=pos)
        self.collected = False
    
    def apply(self, player):
        if not self.collected:
            player.health = min(player.health + 25, 100)
            self.collected = True
            self.kill()
    
    def update(self):
        pass


class WaterHazard(pygame.sprite.Sprite):
    """Placeholder for a water hazard"""
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((tile_size, tile_size//2))
        self.image.fill((0, 0, 255, 128))  # Semi-transparent blue
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1] + tile_size//2))
    
    def apply_effect(self, player):
        # Slow down the player in water
        player.velocity.x *= 0.9
    
    def update(self):
        pass


class Enemy(pygame.sprite.Sprite):
    """Placeholder for an enemy"""
    def __init__(self, pos, obstacles):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))  # Red for enemy
        self.rect = self.image.get_rect(topleft=pos)
        self.velocity = pygame.Vector2(2, 0)  # Basic horizontal movement
        self.obstacles = obstacles
        self.direction = 1  # 1 for right, -1 for left
    
    def update(self):
        # Simple left-right movement
        self.rect.x += self.velocity.x * self.direction
        
        # Check for collisions with obstacles
        for obstacle in self.obstacles:
            if self.rect.colliderect(obstacle.rect):
                self.direction *= -1  # Reverse direction
                break
        
        # Check for edges
        if self.rect.left < 0 or self.rect.right > pygame.display.get_surface().get_width():
            self.direction *= -1


class Trampoline(pygame.sprite.Sprite):
    """Placeholder for a trampoline"""
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((tile_size, tile_size//2))
        self.image.fill((255, 165, 0))  # Orange for trampoline
        self.rect = self.image.get_rect(topleft=pos)
        self.active = False
        self.activation_time = 0
    
    def activate(self):
        self.active = True
        self.activation_time = pygame.time.get_ticks()
        # In a full implementation, you would trigger animation here
    
    def update(self):
        # Reset after animation
        if self.active and pygame.time.get_ticks() - self.activation_time > 500:
            self.active = False


class FinishPoint(pygame.sprite.Sprite):
    """Placeholder for level finish point"""
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill((255, 215, 0))  # Gold for finish
        self.rect = self.image.get_rect(topleft=pos)