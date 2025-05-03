import pygame
from settings import screen_width, screen_height, tile_size, fps
from player import player
from coin import coin
try:
    from assets.levels.level import level
except ImportError as e:
    print(f"Error importing level module: {e}")
    pygame.quit()
    exit()

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pinky's Coins")
clock = pygame.time.Clock()

# Load Background
try:
    background_image = pygame.image.load('assets/images/background/clouds1.jpg').convert()
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
except FileNotFoundError as e:
    print(f"Error loading background: {e}")
    pygame.quit()
    exit()

# Load Music
try:
    pygame.mixer.music.load('assets/sounds/piano-melody-277609.mp3')
    pygame.mixer.music.play(-1)  # Play on loop
except pygame.error as e:
    print(f"Error loading music: {e}")

# Player setup
player = player((100, screen_height - 2 * tile_size))

# Level data (temporary - we'll expand this)
level_data = [
    "####################",
    "#                  #",
    "#  c g b h w       #",
    "# ######   ####    #",
    "#        c         #",
    "####################",
]

# Level setup
level = level(level_data, player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player input
    keys = pygame.key.get_pressed()
    player.handle_input(keys)

    # Update
    player.update()
    level.update()

    # Draw
    screen.blit(background_image, (0, 0))
    level.draw(screen)
    player.draw(screen)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()