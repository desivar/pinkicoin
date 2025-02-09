import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pinky's Coins")

# Load assets (images and sounds)
try:
    player_image = pygame.image.load(
        'assets/images/pinkygirl.jpg').convert_alpha()
    background_image = pygame.transform.scale(
        pygame.image.load('assets/images/clouds1.jpg').convert(),
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    coin_image = pygame.image.load('assets/images/coin.png').convert_alpha()
    coin_image = pygame.transform.scale(coin_image, (30, 30))
except FileNotFoundError as e:
    print(f"Error loading asset: {e}")
    pygame.quit()
    exit()

pygame.mixer.music.load('assets/sounds/piano-melody-277609.mp3')
coin_sound = pygame.mixer.Sound('assets/sounds/coin_sound.wav')

# Scale images
player_size = 50
player_image = pygame.transform.scale(player_image, (player_size, player_size))

# Player settings
player_pos = [
    SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * player_size
]
player_speed = 5
player_lives = 3

# Coin settings

num_coins = 5
coins = []
for _ in range(num_coins):
    coins.append([
        random.randint(0, SCREEN_WIDTH - 30),
        random.randint(0, SCREEN_HEIGHT - 30)
    ])

# Play background music
pygame.mixer.music.play(-1)

# Clock
clock = pygame.time.Clock()

# Game state
game_over = False
score = 0
font = pygame.font.SysFont("monospace", 35)

# Collision detection


def detect_collision(player_rect, coin_rect):
    return player_rect.colliderect(coin_rect)


# Enemy settings
enemy_size = 25
enemy_pos = [
    random.randint(0, SCREEN_WIDTH - enemy_size),
    random.randint(0, SCREEN_HEIGHT - enemy_size)
]
enemy_speed = 1

# Game loop
game_over = False  # Initialize game_over BEFORE the loop

while not game_over:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True         # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < SCREEN_HEIGHT - player_size:
        player_pos[1] += player_speed

    # Drawing
    screen.blit(background_image, (0, 0))
    player_rect = player_image.get_rect(topleft=player_pos)
    screen.blit(player_image, player_pos)

    # Coins
    coins_to_remove = []
    for i, coin_pos in enumerate(coins):
        coin_rect = coin_image.get_rect(topleft=coin_pos)
        screen.blit(coin_image, coin_pos)

        if detect_collision(player_rect, coin_rect):
            score += 1
            coin_sound.play()
            coins_to_remove.append(i)

    for i in sorted(coins_to_remove, reverse=True):
        del coins[i]
        coins.append([
            random.randint(0, SCREEN_WIDTH - 30),
            random.randint(0, SCREEN_HEIGHT - 30)
        ])

    # Enemy movement (Chase player)
    dx = player_pos[0] - enemy_pos[0]
    dy = player_pos[1] - enemy_pos[1]
    dist = max(1, (dx**2 + dy**2)**0.5)  # Avoid division by zero
    enemy_pos[0] += enemy_speed * dx / dist
    enemy_pos[1] += enemy_speed * dy / dist

    # Keep enemy on screen
    enemy_pos[0] = max(0, min(enemy_pos[0], SCREEN_WIDTH - enemy_size))
    enemy_pos[1] = max(0, min(enemy_pos[1], SCREEN_HEIGHT - enemy_size))

    enemy_rect = pygame.Rect(
        enemy_pos[0], enemy_pos[1], enemy_size, enemy_size
    )
    pygame.draw.rect(screen, (255, 0, 0), enemy_rect)  # Draw the enemy

    # Check for enemy collision (with special effect)
    if detect_collision(player_rect, enemy_rect):
        player_lives -= 1
        # Reset player position
        player_pos = [
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * player_size
        ]
        # Special effect (flash the screen red)
        screen.fill((255, 0, 0), rect=player_rect)  # Flash player red
        pygame.display.update(player_rect)  # Update only the player area
        pygame.time.delay(200)  # Short delay

    # Score and Lives display
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    lives_text = font.render(f"Lives: {player_lives}", True, BLACK)
    screen.blit(lives_text, (10, 50))

    # Check for game over
    if player_lives <= 0:
        game_over = True

    pygame.display.update()  # Update the display (Essential!)
    clock.tick(30)    # Control the frame rate
    # Game Over Screen
game_over_screen = True  # Flag for the game over screen loop
while game_over_screen:  # Use a separate flag for the game over screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Press 'r' to restart
                # Reset all game variables
                score = 0
                player_lives = 3
                player_pos = [
                    SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * player_size
                ]
                coins = []
                for _ in range(num_coins):
                    coins.append([
                        random.randint(0, SCREEN_WIDTH - 30),
                        random.randint(0, SCREEN_HEIGHT - 30)
                    ])
                enemy_pos = [random.randint(0, SCREEN_WIDTH - enemy_size),
                             random.randint(0, SCREEN_HEIGHT - enemy_size)]
                game_over = False  # Reset game_over flag
                game_over_screen = False  # Exit the game over screen loop
                break  # Exit the event loop

    # Draw game over screen
    screen.blit(background_image, (0, 0))
    game_over_text = font.render("Game Over", True, BLACK)
    screen.blit(game_over_text,
                (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
    final_score_text = font.render(f"Final Score: {score}", True, BLACK)
    screen.blit(final_score_text,
                (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50))
    restart_text = font.render("Press 'r' to restart", True, BLACK)
    screen.blit(restart_text,
                (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100))
    pygame.display.update()

pygame.quit()
