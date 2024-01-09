#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Final Summative: Particles
# Author: Alex U
# Date: Jan 24 2023
# Description: This is the particle file where all particle and effects are calculated
# this includes magic, death, attack, and grass
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pygame
from support import import_folder
from random import *

#defines the animation player class which is responsible for the spells animations
#also responsible for hit animations, death animations and grass breaking animations
class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # magic
            'flame': import_folder('./graphics/particles/flame/frames'),
            'aura': import_folder('./graphics/particles/aura'),
            'heal': import_folder('./graphics/particles/heal/frames'),
            'thunder2': import_folder('./graphics/particles/thunder'),

            # attacks
            'claw': import_folder('./graphics/particles/claw'),
            'slash': import_folder('./graphics/particles/slash'),
            'sparkle': import_folder('./graphics/particles/sparkle'),
            'leaf_attack': import_folder('./graphics/particles/leaf_attack'),
            'thunder': import_folder('./graphics/particles/thunder'),

            # monster deaths
            'squid': import_folder('./graphics/particles/smoke_orange'),
            'raccoon': import_folder('./graphics/particles/raccoon'),
            'spirit': import_folder('./graphics/particles/nova'),
            'bamboo': import_folder('./graphics/particles/bamboo'),
            'dragon': import_folder('./graphics/particles/nova'),
            'dragon2': import_folder('./graphics/particles/nova'),
            'beast': import_folder('./graphics/particles/smoke2'),
            'GiantFlame': import_folder('./graphics/particles/nova'),
            'Reptile': import_folder('./graphics/particles/nova'),
            'GiantFlame2': import_folder('./graphics/particles/nova'),
            'Akshar': import_folder('./graphics/particles/nova'),
            'Yatagarasu': import_folder('./graphics/particles/sparkle'),
            'NPC1': import_folder('./graphics/particles/sparkle'),
            'NPC2': import_folder('./graphics/particles/sparkle'),
            'NPC3': import_folder('./graphics/particles/sparkle'),
            'NPC4': import_folder('./graphics/particles/sparkle'),
            'NPC5': import_folder('./graphics/particles/sparkle'),
            'NPC6': import_folder('./graphics/particles/sparkle'),


            # leafs
            'leaf': (
                import_folder('./graphics/particles/leaf1'),
                import_folder('./graphics/particles/leaf2'),
                import_folder('./graphics/particles/leaf3'),
                import_folder('./graphics/particles/leaf4'),
                import_folder('./graphics/particles/leaf5'),
                import_folder('./graphics/particles/leaf6'),
                self.reflect_images(import_folder('./graphics/particles/leaf1')),
                self.reflect_images(import_folder('./graphics/particles/leaf2')),
                self.reflect_images(import_folder('./graphics/particles/leaf3')),
                self.reflect_images(import_folder('./graphics/particles/leaf4')),
                self.reflect_images(import_folder('./graphics/particles/leaf5')),
                self.reflect_images(import_folder('./graphics/particles/leaf6'))
            )
        }
    #defines the reflect images function which will reflect the grass particles therefore increasing the number of
    #grass images that can be displayed when its broken from 6 to 12
    def reflect_images(self, frames):
        new_frames = []
        #will flip the image and add it to a new_frames list
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame,True,False)
            new_frames.append(flipped_frame)
        return new_frames
    #defines the create grass particles function which will create particles when grass is destroyed
    #particles are chosen at random from 12 images
    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)
    #defines the create particles function which is responsible for creating most of the particles
    def create_particles(self, attack_type, pos, groups, speed=0.15):
        animation_frames = self.frames[attack_type]
        ParticleEffect(pos, animation_frames, groups, speed)

    # defines the create weapon function which is responsible for creating particles
    # when the final weapon excalibur hits an enemy
    def create_weapon_particles(self, pos, groups):
        animation_frames = self.frames['thunder']
        ParticleEffect(pos, animation_frames, groups)

#defines the particle effect function which is responsible for display the effects onto the screen
class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups, speed=0.15):
        #initalises groups
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = speed
        #gets which frames it will play from and sets a base image and rect
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
    #defines the animate function which will cycle through the frames based off of the animation speed
    def animate(self):
        #cycling through the frames
        self.frame_index += self.animation_speed
        #if the frame index is longer therefore doesnt exist will kill it
        if self.frame_index >= len(self.frames):
            self.kill()
        #else it will set a new image to display
        else:
            self.image = self.frames[int(self.frame_index)]
    #defines the update function which will constantly display animations when called
    def update(self):
        self.animate()