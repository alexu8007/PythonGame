#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Final Summative: Weapon
# Author: Alex U
# Date: Jan 24 2023
# Description: This is the Weapon file which makes all the weapons sprites in the game
# it also chooses which direction to display the weapon based off of the the player direction
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pygame

#defines the weapon class which will setup weapons
class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        #gets the direction of the player from its path by spliting the value before the _ i.e.(up,down,left,right)
        direction = player.status.split('_')[0]
        #makes its sprite type be a weapons
        self.sprite_type = 'weapon'
        #gets the full path of the weapon
        full_path = f'./graphics/weapons/{player.weapon}/{direction}.png'
        #gets the picture of the weapon
        self.image = pygame.image.load(full_path).convert_alpha()
        #checks what the direction is and will get the rect of that specific image to display its hitbox and interact with other entities
        #example if player direction is 'right' will display the image which is right.png and ge that images rect which would be to the right of the player
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0))
        else:
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-16,0))