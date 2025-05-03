# player.py
import pygame
from settings import GRAVITY, PLAYER_SPEED, JUMP_POWER


class player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(
            "assets/images/pinkygirl.jpg"
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel.x = 0
        if keys[pygame.K_LEFT]:
            self.vel.x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.vel.x = PLAYER_SPEED
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel.y = -JUMP_POWER

    def apply_gravity(self):
        self.vel.y += GRAVITY
        self.rect.y += self.vel.y

    def update(self):
        self.handle_input()
        self.rect.x += self.vel.x
        self.apply_gravity()
