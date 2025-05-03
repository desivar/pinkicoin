import pygame
from settings import PLAYER_SPEED


class player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        try:
            self.image = pygame.image.load(
                'assets/images/wizard/wizard.jpg'
            ).convert_alpha()    #  Using wizard for now
            self.image = pygame.transform.scale(self.image, (50, 50)) # Adjust size
        except FileNotFoundError as e:
            print(f"Error loading player image: {e}")
            pygame.quit()
            exit()
        self.rect = self.image.get_rect(topleft=pos)
        self.vel = pygame.Vector2(0, 0)

    def handle_input(self, keys):
        self.vel.x = 0
        if keys[pygame.K_LEFT]:
            self.vel.x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.vel.x = PLAYER_SPEED
        if keys[pygame.K_UP]:  # Basic jump (will need more work)
            self.vel.y = -10

    def update(self):
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y  # Basic vertical movement

    def draw(self, surface):
        surface.blit(self.image, self.rect)