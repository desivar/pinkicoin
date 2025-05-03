import pygame


class coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(
            "assets/images/pinkygirl.jpj"
        ).convert_alpha()
        self.rect = self.image.get_rect(center=pos)