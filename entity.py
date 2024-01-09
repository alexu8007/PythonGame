#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Final Summative: Entity
# Author: Alex U
# Date: Jan 24 2023
# Description: This is the Entity file which the player and the enemies inherit from
# they inherit the movement the collision system and the invulnerability system
# this is because they all share these attributes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#import pygame and the math function
import pygame
from math import *


#creation of the entity class which will be inherited by player and enemy
class Entity(pygame.sprite.Sprite):
    def __init__(self,groups):
        #initalises the groups
        super().__init__(groups)
        #sets the initial common attributes for all entities
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
    #defines the move function which is responsible for the direction and the speed of movement
    def move(self,speed):
        #makes sure that walking diagonally isnt faster then up,down,right,left
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        #moves the hitbox i.e. sprite based off of the direction and speed of entity
        self.hitbox.x += self.direction.x * speed
        #checks the collision of sprites and runs the collision functions
        self.collisions('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collisions('vertical')
        self.rect.center = self.hitbox.center
    #defines the collision function which deals with all entity collisions
    def collisions(self, direction):
        #runs this if the direction is horizontal then will do collisions as such
        if direction == 'horizontal':
            if self.status1 == 'move' or self.status1 == 'attack':
                #if entity is in movement or attacking checks through all obstacles to see if the collide
                for sprite in self.obstacle_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        #if they collide it will push a the sprite in a certain direction to make it look like its hitting a wall
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right
        # runs this if the direction is vertical then will do collisions as such
        if direction == 'vertical':
            if self.status1 == 'move' or self.status1 == 'attack':
                # if entity is in movement or attacking checks through all obstacles to see if the collide
                for sprite in self.obstacle_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        # if they collide it will push a the sprite in a certain direction to make it look like its hitting a wall
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
    #defines the wave value function which will make the entity blink in and out when hit
    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0