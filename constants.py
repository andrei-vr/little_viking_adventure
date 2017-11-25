from pygame import *
import os

# Debug
MUSIC_ON = False

# Global constants
GAME_NAME = "Little Viking Adventure"
WIN_WIDTH  = 1600
WIN_HEIGHT = 1200
BLOCK_SIZE = 128
GAME_FOLDER = os.getcwd()
BACKGROUND_COLOR = "#061ce2"
TP_COLOR = "#b2e206" # Transparent color

# Hero constants
HERO_MOVE_SPEED = 500
HERO_ATTACK_TIME = 1000
HERO_DMG_TIME = 400
HERO_HITBOX_WIDTH = 50
HERO_HITBOX_HEIGHT = 50

# Goblin monster constants
GOB_MS = 250
GOB_RUNNING_MS = 300
GOB_HITBOX_WIDTH = 30
GOB_HITBOX_HEIGHT = 30

# List of custom events
ATTACK_OVER = USEREVENT + 1
ATTACK_DMG  = USEREVENT + 2