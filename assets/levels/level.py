# level.py
import pygame
from coin import coin


class level:
    def __init__(self, player):
        self.player = player
        self.player_group = pygame.sprite.GroupSingle(player)

        # Example coin
        self.coins = pygame.sprite.Group()
        self.coins.add(coin((400, 300)))

    def update(self, screen):
        self.coins.draw(screen)
        self.player_group.update()
        self.player_group.draw(screen)

        # Check coin collisions
        pygame.sprite.groupcollide(self.player_group, self.coins, False, True)
