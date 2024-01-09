#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Final Summative: Tile
# Author: Alex U
# Date: Jan 24 2023
# Description: This is the Tile file which deals with all the tile generation
# Tile are mainly boundary files and boss arenas
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import pygame
from settings import *

#creates teh tile class which is responsible for creating tiles of objects and boundaries based off of
# inputted values and x y coordinates on teh csv files
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        #initialse the groups
        super().__init__(groups)
        #gets the sprite type of the tile to be made (visible/non-visible,obstacle/non-obstacle)
        self.sprite_type = sprite_type
        #gets the image
        self.image = surface.convert_alpha()
        #gets the rect and the hitbox of the tile, deflates the image by -10 to make game collisions look smoother
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)