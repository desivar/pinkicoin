"""
Game settings and configuration
This file contains all configurable parameters for the game
"""

# Game setup
game_title = "Pinky's Coins"
screen_width = 800
screen_height = 600
fps = 60
tile_size = 32

# Player physics
PLAYER_SPEED = 5
JUMP_STRENGTH = 10
GRAVITY = 0.5
TERMINAL_VELOCITY = 15  # Maximum falling speed

# UI settings
UI_FONT_SIZE = 36
UI_FONT_COLOR = (255, 255, 255)
UI_SCORE_POS = (20, 20)  # Position for score display
UI_LEVEL_POS = (screen_width - 150, 20)  # Position for level display
UI_HEALTH_POS = (20, 50)  # Position for health display

# Enemy settings
ENEMY_SPEED = 2

# Coin settings
COIN_VALUES = {
    'bronze': 1,
    'silver': 3,
    'gold': 5
}
COIN_ANIMATION_SPEED = 0.1

# Colors
COLOR_BG = (255, 230, 250)        # Light pink background
COLOR_PLAYER = (255, 0, 255)      # Purple for player fallback
COLOR_PLATFORM = (100, 50, 50)    # Brown for platforms
COLOR_COIN_GOLD = (255, 215, 0)   # Gold
COLOR_COIN_SILVER = (192, 192, 192)  # Silver
COLOR_COIN_BRONZE = (205, 127, 50)   # Bronze
COLOR_UI_TEXT = (255, 255, 255)   # White for UI text
COLOR_UI_BG = (0, 0, 0)           # Black for UI backgrounds
COLOR_HEALTH_BAR = (255, 0, 0)    # Red for health bar

# Audio
MUSIC_VOLUME = 0.5                # 50% volume
SFX_VOLUME = 0.7                  # 70% volume

# Paths
PLAYER_IMAGE_PATH = 'assets/images/wizard/wizard.jpg'
BACKGROUND_IMAGE_PATH = 'assets/images/background/clouds1.jpg'
MUSIC_PATH = 'assets/sounds/piano-melody-277609.mp3'
SOUND_COIN = 'assets/sounds/coin_collect.wav'
SOUND_JUMP = 'assets/sounds/jump.wav'
SOUND_LEVEL_COMPLETE = 'assets/sounds/level_complete.wav'

# Levels
MAX_LEVELS = 3
LEVEL_PATHS = [
    'assets/levels/level1.txt',
    'assets/levels/level2.txt',
    'assets/levels/level3.txt',
]

# Debug settings
DEBUG = False  # Set to True to enable debug features
DEBUG_COLLISION_RECTS = False  # Show collision rectangles
DEBUG_SHOW_FPS = True  # Show FPS counter

# Game difficulty
DIFFICULTY_EASY = {
    'player_health': 5,
    'enemy_damage': 1,
    'coin_frequency': 'high'
}

DIFFICULTY_MEDIUM = {
    'player_health': 3,
    'enemy_damage': 2,
    'coin_frequency': 'medium'
}

DIFFICULTY_HARD = {
    'player_health': 2,
    'enemy_damage': 3,
    'coin_frequency': 'low'
}

# Set the current difficulty
current_difficulty = DIFFICULTY_MEDIUM

# Level tile mapping
TILE_MAPPING = {
    '#': 'wall',        # Wall/platform
    ' ': 'empty',       # Empty space
    'c': 'coin_bronze', # Bronze coin
    's': 'coin_silver', # Silver coin
    'g': 'coin_gold',   # Gold coin
    'e': 'enemy',       # Enemy
    'h': 'health',      # Health pickup
    'p': 'player',      # Player start position
    'f': 'finish',      # Level finish
    'w': 'water',       # Water/hazard
    'l': 'lava',        # Lava/hazard
    't': 'trampoline',  # Jump boost
}