import pygame
from settings import TILE_SIZE
from coin import Coin  # Import the Coin class


class Level:
    def __init__(self, level_data, player):
        self.level_data = level_data
        self.player = player
        self.tiles = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.load_level()

    def load_level(self):
        for row_index, row in enumerate(self.level_data):
            for col_index, tile_char in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if tile_char == '#':
                    tile = Tile('assets/images/tiles/ground.png', (x, y))
                    self.tiles.add(tile)
                elif tile_char == 'C':
                    coin = Coin((x + TILE_SIZE // 2, y + TILE_SIZE // 2), 'silver')
                    self.coins.add(coin)
                elif tile_char == 'G':
                    coin = Coin((x + TILE_SIZE // 2, y + TILE_SIZE // 2), 'gold')
                    self.coins.add(coin)
                elif tile_char == 'B':
                    coin = Coin((x + TILE_SIZE // 2, y + TILE_SIZE // 2), 'bronze')
                    self.coins.add(coin)
                elif tile_char == 'H':
                    # TODO: Implement Heart Gift
                    pass
                elif tile_char == 'W':
                    # TODO: Implement Wizard (likely as an Enemy)
                    pass
                elif tile_char == 'P':
                    self.player.rect.topleft = (x, y)  # Set player start position

    def update(self):
        # Update level elements (e.g., moving platforms, enemies)
        self.coins.update()  # If coins have animations

    def draw(self, surface):
        self.tiles.draw(surface)
        self.coins.draw(surface)


class Tile(pygame.sprite.Sprite):
    def __init__(self, image_path, pos):
        super().__init__()
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except FileNotFoundError as e:
            print(f"Error loading tile image: {e}")
            pygame.quit()
            exit()
        self.rect = self.image.get_rect(topleft=pos)
        