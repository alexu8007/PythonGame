#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Final Summative: Player
# Author: Alex U
# Date: Jan 24 2023
# Description: This is the player function that deals with player damage, stats, animations,
# interactions cooldowns, and the player hitboxes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pygame
from settings import *
from support import import_folder
from entity import Entity

#defines the player class for which the player will be created
#this class deals with almost everything related to the player
class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_weapon,create_magic):
        #initiales the groups
        super().__init__(groups)
        #gets the player
        self.image = pygame.image.load('./graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-6,-26)
        self.import_player_assets()
        #sets his initial status to be facing up when you spawn
        self.status = 'up'
        self.obstacle_sprites = obstacle_sprites
        self.status1 = 'move'
        #sets attacking variables which are used for cooldowns, invulnerability and moving
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.create_attack = create_attack
        self.destroy_weapon = destroy_weapon
        #sets initial waepon index and gets the list of weapon data from the settings file
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200
        #sets the inital player stats, his max stats, and the upgrade cost for all of his abilities
        self.stats = {'health':100,"energy":60,'attack':10,'magic':4,'speed':7,'stamina':100, 'endurance':1}
        self.max_stats = {'health': 2000, "energy": 400, 'attack': 200, 'magic': 200, 'speed': 12}
        self.upgrade_cost = {'health': 100, "energy": 100, 'attack': 100, 'magic': 100, 'speed': 100}
        #sets initial player attributes
        self.health = self.stats['health']
        self.endurance = self.stats['endurance']
        self.energy = self.stats['energy']
        self.stamina = self.stats['stamina']
        #sets his exp and level
        self.exp = 0
        self.speed = self.stats['speed']
        self.lvl = 0
        #sets the magic_index and the weapons you have in inv as well as magic in inv
        self.magic_index = 0
        self.weaponinv = 0
        self.magicinv = 1
        self.magic = list(magic_data.keys())[self.magic_index]
        self.switch_magic = True
        self.magic_switch_time = None
        self.create_magic = create_magic
        self.dodgecounter = False
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500
        self.xcoor = None
        self.ycoor = None
        self.bossfighting = False
        #sets the attack sound
        self.weapon_attack_sound = pygame.mixer.Sound('./audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.1)
        self.finalorreg = False
    #defines the import player assets function which will import all the animation frames within the player list and
    #assign them to keys in a dictionary
    def import_player_assets(self):
        character_path = './graphics/player/'
        self.animations = {'up': [], 'down':[],'left':[],'right':[],
                           'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
                           'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[],'death':[]}
        #adds the frames to the self.animations folder
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    #defines the function that gets the current weapons damage
    def get_full_weapon_damage(self):
        base = self.stats['attack']
        weapnn = weapon_data[self.weapon]['damage']
        return base + weapnn
    #defines the function that gets the current magic damage/strength
    def get_full_magic_damage(self):
        base = self.stats['magic']
        weapnn = magic_data[self.magic]['strength']
        return base + weapnn
    #return the values of the player stats in list form
    def get_value_by_index(self,index):
        return list(self.stats.values())[index]

    # return the upgrade cost of the player stats in list form
    def get_cost_by_index(self,index):
        return list(self.upgrade_cost.values())[index]
    #defines the energy recovery which makes the players energy increase slowly
    #speed is increased through increasing magic
    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']
    #defines the input function which detects user keyboard inputs and chooses what to do with them
    def input(self):
        running = False
        #gets the keys that are being pressed
        keys = pygame.key.get_pressed()
        #checks if the player is currently running and if he isnt will regen stamina
        if running == False and self.stamina < self.stats['stamina']:
            self.stamina += 0.1
        #check if the player currently is not attacking
        if not self.attacking:
            #checks if the player press up down left or right and if so will move in that direction
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0
            #if you press shift or hold it it will run the sprint function
            if keys[pygame.K_LSHIFT] and not self.attacking:
                self.sprint()
            #if you press space and your currently not attacking it will run the following
            if keys[pygame.K_SPACE] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                #runs the create attack function
                self.create_attack()
                #plays a sound
                self.weapon_attack_sound.play()
            # if you press lctrl and your currently not attacking it will run the following
            if keys[pygame.K_LCTRL] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                #it will get the style of the current magic attack as well as strength and cost
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                #runs the create magic function
                self.create_magic(style,strength,cost)
            #if the player presses q will change their weapon
            if keys[pygame.K_q] and self.switch_weapon:
                #makes sure the player will only switch weapons once per input
                self.switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                self.weapon_index += 1
                #changes the weapon based off of the inv
                if self.weapon_index > self.weaponinv:
                    self.weapon_index = 0
                #sets the new self.weapon value
                self.weapon = list(weapon_data.keys())[self.weapon_index]
            # if the player presses e will change their weapon
            if keys[pygame.K_e] and self.switch_magic:
                self.switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                self.magic_index += 1
                # changes the weapon based off of the inv
                if self.magic_index > self.magicinv:
                    self.magic_index = 0
                # sets the new self.magic value
                self.magic = list(magic_data.keys())[self.magic_index]
    #defines the get_status function
    def get_status(self):
        #if the player is not moving it will set his status to his direction + "_idle"
        #which is needed to display the correct image file
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        #if the player is attacking sets his direction to 0 and 0 so hes not moving
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            #replces the '_idle' at the end of the value with '_attack" so it can display the attack animation
            #if there is no idle it will just add '_attack'
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
        #if hes not attacking removes it from the name to display a non attacking image
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')
    #defines the animate function which will animate the players movement
    def animate(self):
        #gets the animation frames based off of the current status
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        #runs through each animation frame based off of stats
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        #makes the player blink in and out when he is hit
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    #defines the sprint function which will make the player movee faster when it is pressed
    def sprint(self):
        if self.stamina > 0:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
            #gets the direction and moves the player
            self.hitbox.x += self.direction.x * 3
            self.collisions('horizontal')
            self.hitbox.y += self.direction.y * 3
            self.collisions('vertical')
            self.rect.center = self.hitbox.center
            #slowly removes stamina
            self.stamina -= 0.5
    #defines the cooldown function which deals with all the player cooldowns
    def cooldowns(self):
        #gets the current time
        current_time = pygame.time.get_ticks()
        #if the player is currently  will determine the time the weapon sprite will stay active for, it will then destory it
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_weapon()
        #if the player has elected to switch his weapon will start a small cooldown for it
        if not self.switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.switch_weapon = True
        # if the player has elected to switch his magic will start a small cooldwon for it
        if not self.switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.switch_magic = True
        #will make the player invincible for a certain amount of time after hes been hit
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
    #defines the update function which will run all the previous functions
    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        #gets the players x and y coords
        self.xcoor = self.rect.x
        self.ycoor = self.rect.y
        self.move(self.speed)
        self.energy_recovery()