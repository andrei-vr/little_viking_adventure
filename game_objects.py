from constants import *
from functions import *

from pygame import *

class Wall(sprite.Sprite):

    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.rect = Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
