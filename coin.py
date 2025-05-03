import pygame


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(
            "assets/images/coin.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(center=pos)