import pygame

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos, coin_type):
        super().__init__()
        self.coin_type = coin_type
        self.value = 0
        image_path = ""
        if coin_type == 'silver':
            image_path = 'assets/images/coins/silver_coin.png'
            self.value = 1
        elif coin_type == 'gold':
            image_path = 'assets/images/coins/gold_coin.png'
            self.value = 5
        elif coin_type == 'bronze':
            image_path = 'assets/images/coins/bronze_coin.png'
            self.value = 3

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 30)) # Adjust size as needed
        except FileNotFoundError as e:
            print(f"Error loading coin image: {e}")
            pygame.quit()
            exit()
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        # Add any coin animation here if needed
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)