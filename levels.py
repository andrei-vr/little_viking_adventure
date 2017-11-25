from constants import *
from functions import *
from game_objects import *
from monsters import *
from hero import *

from pygame import *
import tmxreader
import os
import helperspygame

class Level:
    def __init__(self, tile_map, track_name):
        self.level_over = False

        # Level sprites
        self.entities = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.hero = None

        # Miscellaneous
        self.track_name = track_name
        self.background = Surface((WIN_WIDTH, WIN_HEIGHT)) # create a surface (image)
        self.background.fill(Color(BACKGROUND_COLOR)) # fill the surface with background color

        # Parse a tile map
        path = os.path.join(os.getcwd(), "images", "tiles")
        world_map = tmxreader.TileMapParser().parse_decode('%s/%s.tmx' % (path, tile_map))
        resources = helperspygame.ResourceLoaderPygame()
        resources.load(world_map)
        self.sprite_layers = helperspygame.get_layers_from_map(resources)
        walls_layer   = self.sprite_layers[1]
        goblins_layer = self.sprite_layers[2]
        hero_layer    = self.sprite_layers[3]

        # Create walls
        for row in range(0, walls_layer.num_tiles_x):
            for col in range(0, walls_layer.num_tiles_y):
                if walls_layer.content2D[col][row] is not None:
                   wall = Wall(row * BLOCK_SIZE, col * BLOCK_SIZE)
                   self.walls.add(wall)

        # Create goblins
        for gob in goblins_layer.objects:
            if gob is not None:
                goblin = Goblin(self, gob.x, gob.y)
                self.enemies.add(goblin)

        # Create a hero
        hero = hero_layer.objects[0]
        self.hero = Viking( hero.x, hero.y, self )

        # Assemble entities list (game objects that need to be drawn every cycle)
        self.entities.add(self.enemies)
        self.entities.add(self.hero)

    def level_init(self):
        mixer.music.stop()
        mixer.music.load(os.path.join( GAME_FOLDER, 'music', self.track_name ))
        mixer.music.play()