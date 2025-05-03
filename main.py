# main.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BG
from player import Player
from coin import Coin
from assets.levels.level import Level

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

# Game objects
player = Player((100, 400))
level = Level(player)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(COLOR_BG)
    level.update(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
