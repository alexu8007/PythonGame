#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Final Summative: Magic
# Author: Alex U
# Date: Jan 24 2023
# Description: This is the Magic file where magic animations, damage, sounds,s trength
# and cost reduction are done
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pygame
from settings import *
from random import randint

#defines the Magic player class which is responsible for the execution of magic attacks and their sounds/animations
class MagicPlayer:
    def __init__(self,animation_player):
        #gest the animation player from its paramater
        self.animation_player = animation_player
        #creates sounds attributes for each spells in the game
        self.thundersound = pygame.mixer.Sound('./audio/Explosion4.wav')
        self.thundersound.set_volume(0.04)
        self.sounds = {
            'heal': pygame.mixer.Sound('./audio/heal.wav'),
            'flame': pygame.mixer.Sound('./audio/Fire.wav'),
            'thunder': pygame.mixer.Sound('./audio/Explosion4.wav')
        }
    #defines the heal function which executes the heal spell if called upon
    def heal(self,player,strength,cost,groups):
        #checks if the player has enough mana
        if player.energy >= cost:
            #plays the sound effect
            self.sounds['heal'].set_volume(0.08)
            self.sounds['heal'].play()
            #increases the players health based off of the potency of the spell
            player.health += strength
            player.energy -= cost
            #checks so it doesnt overheal the player
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            #plays an animation from the particles class that will display on the screen when the user uses the spell
            self.animation_player.create_particles('heal',player.rect.center + pygame.math.Vector2(0,-60),groups)
            self.animation_player.create_particles('aura', player.rect.center, groups)
    #defines the oblivion function which executes if the final spell oblivion is usd
    def oblivion(self,player,cost,groups):
        #checks if the player has enough mana and removes it
        if player.energy >= cost:
            player.energy -= cost
            #plays the sound effect
            self.thundersound.play()
            #This for statement is used to make the thunder effect go all around the player
            #different offsets are called upon for each thunder sprite so that they will incircle the player
            for i in range(10):
                offset = (i) * TILESIZE
                offset2 = (-i) * TILESIZE
                offset3 = ((i) * TILESIZE)/2
                offset4 = ((-i) * TILESIZE)/2
                #this will display 8 thunder sprites around the player and will continue displaying 8 more around the player 10 times
                # each time increasing the distance form the player
                #the effect will play through the animation player
                x = player.rect.centerx + offset + randint(-TILESIZE // 3, TILESIZE // 3)
                y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                self.animation_player.create_particles('thunder2', (x, y), groups)
                x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                y = player.rect.centery + offset + randint(-TILESIZE // 3, TILESIZE // 3)
                self.animation_player.create_particles('thunder2', (x, y), groups)
                x = player.rect.centerx + offset2 + randint(-TILESIZE // 3, TILESIZE // 3)
                y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                self.animation_player.create_particles('thunder2', (x, y), groups)
                x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                y = player.rect.centery + offset2 + randint(-TILESIZE // 3, TILESIZE // 3)
                self.animation_player.create_particles('thunder2', (x, y), groups)
                x = player.rect.centerx + offset3 + randint(-TILESIZE // 3, TILESIZE // 3)
                y = player.rect.centery + offset3 + randint(-TILESIZE // 3, TILESIZE // 3)
                self.animation_player.create_particles('thunder2', (x, y), groups)
                x = player.rect.centerx + offset3 + randint(-TILESIZE // 3, TILESIZE // 3)
                y = player.rect.centery + offset4 + randint(-TILESIZE // 3, TILESIZE // 3)
                self.animation_player.create_particles('thunder2', (x, y), groups)
                x = player.rect.centerx + offset4 + randint(-TILESIZE // 3, TILESIZE // 3)
                y = player.rect.centery + offset4 +randint(-TILESIZE // 3, TILESIZE // 3)
                self.animation_player.create_particles('thunder2', (x, y), groups)
                x = player.rect.centerx + offset4+randint(-TILESIZE // 3, TILESIZE // 3)
                y = player.rect.centery + offset3 + randint(-TILESIZE // 3, TILESIZE // 3)
                self.animation_player.create_particles('thunder2', (x, y), groups)
    #defines the flame function which will play when the user uses the flame spell
    def flame(self,player,cost,groups):
        #checks if player has enough mana
        if player.energy >= cost:
            #plays the sound effect
            self.sounds['flame'].set_volume(0.08)
            self.sounds['flame'].play()
            player.energy -= cost
            #gets the direction in which the player is facing in order to display the sprites in that direction
            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1,0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1,0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0,-1)
            else:
                direction = pygame.math.Vector2(0,1)
            #this for statement will create 10 sprites in the direction that the player is facing
            #each sprite is getting furthur away from the player based off of an offset
            for i in range(10):
                if direction.x:
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE//3,TILESIZE//3)
                    y = player.rect.centery + randint(-TILESIZE//3,TILESIZE//3)
                    #will use the animation player to display the effects and make the sprite
                    self.animation_player.create_particles('flame',(x,y),groups)
                else:
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx  + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)