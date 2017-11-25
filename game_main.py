from constants import *
from functions import *
from levels import *
from hero import *
from game_objects import *

from pygame import *
import pygame
import helperspygame


# ======================================================================================================================
# Game class
# ======================================================================================================================
class Game:

    def __init__(self):
        pygame.init()                                                             # init pygame
        pygame.mixer.init()                                                       # init pygame module that plays sounds
        icon = pygame.image.load(os.path.join(GAME_FOLDER, 'images', 'icon.png')) # load window icon
        pygame.display.set_icon(icon)                                             # set window icon
        self.screen = display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE) # create a window
        display.set_caption(GAME_NAME)                          # set a window caption
        self.timer = pygame.time.Clock()                        # create main game timer
        self.renderer = helperspygame.RendererPygame()          # create level renderer
        self.ui = UserInput()                                   # create user input struct
        self.current_level = None

        # Set up game levels
        self.level_0 = Level( "level_0", "Vodka.mp3" )

    def get_user_input(self, event):

        # Defaults
        self.ui.mouse_motion = False
        self.ui.attack = False
        self.ui.attack_over = False
        self.ui.attack_dmg = False

        # Handle exit event
        if event.type == QUIT:
            raise SystemExit

        #  Handle keyboard events
        elif event.type == KEYDOWN and event.key == K_a:
            self.ui.left = True
        elif event.type == KEYUP and event.key == K_a:
            self.ui.left = False
        elif event.type == KEYDOWN and event.key == K_d:
            self.ui.right = True
        elif event.type == KEYUP and event.key == K_d:
            self.ui.right = False
        elif event.type == KEYDOWN and event.key == K_w:
            self.ui.up = True
        elif event.type == KEYUP and event.key == K_w:
            self.ui.up = False
        elif event.type == KEYDOWN and event.key == K_s:
            self.ui.down = True
        elif event.type == KEYUP and event.key == K_s:
            self.ui.down = False

        # Handle mouse events
        elif event.type == MOUSEMOTION:
            self.ui.mouse_motion = True
            self.ui.mouse_x      = event.pos[0]
            self.ui.mouse_y      = event.pos[1]
            #print((self.ui.mouse_x, self.ui.mouse_y))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.ui.attack = True

        # Handle custom events
        elif event.type == ATTACK_OVER:
            self.ui.attack_over = True
        elif event.type == ATTACK_DMG:
            self.ui.attack_dmg = True

    def start_next_level(self):
        if self.current_level is None:
            self.current_level = self.level_0
            self.current_level.level_init()

    def update_state(self, dt):
        self.current_level.hero.update(self.ui, dt)
        self.current_level.enemies.update(self.current_level.hero, self.ui, dt)

    def update_screen(self):
        self.screen.blit(self.current_level.background, (0, 0)) # Draw background

        for sprite_layer in self.current_level.sprite_layers:   # Draw not moving map layers
            if not sprite_layer.is_object_group:
                self.renderer.render_layer(self.screen, sprite_layer)

        self.current_level.entities.draw(self.screen)                                       # Draw moving objects
        self.renderer.set_camera_position_and_size(0, 0, WIN_WIDTH, WIN_HEIGHT, "topleft" ) # Set camera position
        pygame.display.update()                                                             # Update display



# ======================================================================================================================
# User Input class
# ======================================================================================================================
class UserInput:
    def __init__(self):
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.attack = False
        self.attack_dmg = False
        self.attack_over = False
        self.throw = False
        self.mouse_motion = False
        self.mouse_x = 0
        self.mouse_y = 0


# ======================================================================================================================
# Game Main Loop
# ======================================================================================================================
game = Game()
while 1:
    if (game.current_level is None) or game.current_level.level_over:
        game.start_next_level()
    dt = game.timer.tick(60)/1000           # Restrict frame rate to 60 FPS and get time (in sec) passed from prev frame
    event = pygame.event.poll()             # Get event from event queue
    game.get_user_input(event)              # Handle user input
    game.update_state(dt)                   # Determine all changes in game state
    game.update_screen()                    # Draw everything
    if not MUSIC_ON: pygame.mixer.stop()
    if not MUSIC_ON: pygame.mixer.music.stop()
    # TODO Make it logging info
    #print(game.timer.get_fps())
    #print(pygame.event.event_name(event.type))
