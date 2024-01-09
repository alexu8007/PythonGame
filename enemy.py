#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Final Summative: Enemy
# Author: Alex U
# Date: Jan 24 2023
# Description: This is the Enemy file which deals with all enemy generation, its decision-making
# (attack, move, idle) the boss fight generations, damage done to player,NPC interactions and animations.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pygame
from settings import *
from support import *
from entity import Entity
from tile import Tile
from support import *

#defines the Enemy class where all the enemies, bosses, NPC will be created in inherits from Entity
#this class will deal with everything enemy related. Animations, boss arenas, dialog, damage, particles, death animations, sounds etc...
class Enemy(Entity):
    def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles,add_exp,difficulty,dialog1='',dialog2='',dialog3=''):
        #initiales groups
        super().__init__(groups)
        #initialises attributes for the enemy
        self.health_bar_rect = pygame.Rect(340,640,600,50)
        self.display_surface = pygame.display.get_surface()
        self.sprite_type = 'enemy'
        self.status = 'idle'
        self.status1 = 'idle'
        #imports the graphics for the given enemy
        self.import_graphics(monster_name)
        self.image  = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites
        self.monster_name = monster_name
        #gets the enemy info from the settings file
        monster_info = monster_data[self.monster_name]
        #sets all the enemies current stats
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']
        #sets more attributes for late calculations
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300
        #gets functions from level file
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp
        #loads the boss arena csv
        self.layout = {'boundary': import_csv_layout('./map/mapidea_bossarena.csv')}
        self.ranonce = True
        #initializises the sounds used
        self.death_sound = pygame.mixer.Sound('./audio/death.wav')
        self.hit_sound = pygame.mixer.Sound('./audio/hit.wav')
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.dialogsound =pygame.mixer.Sound('./audio/Voice3.wav')
        self.death_sound.set_volume(0.05)
        self.hit_sound.set_volume(0.05)
        self.attack_sound.set_volume(0.05)
        self.dialogsound.set_volume(0.1)
        self.notice_radiuss = 1000
        self.healthbardisplay = False
        #gets dialog and the difficulty setting
        self.difficulty = difficulty
        self.dialog1 = dialog1
        self.dialog2 = dialog2
        self.dialog3 = dialog3
    #defines the import graphics function which will import all the enemy graphics into a attribute
    def import_graphics(self,name):
        self.animations = {'idle':[],'move':[],'attack':[]}
        main_path = f'./graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)
    #defines the player distance function which will get the distance of the player to the current enemy
    def get_player_distance(self,player):
        #gets enemy rect center coords
        enemy_vec = pygame.math.Vector2(self.rect.center)
        # gets player rect center coords
        player_vec = pygame.math.Vector2(player.rect.center)
        #calculates distance
        distance = (player_vec - enemy_vec).magnitude()
        #gets direction based off of the distance
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance, direction)
    #defines the get status function which gets the current status to assign to the enemy
    def get_status(self,player):
        #gets the distance from the enemy to the player
        distance = self.get_player_distance(player)[0]
        #if the distance is within attack radius will set the status to attack
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
            self.status1 = 'attack'
        #if the distance is rather in the notice radius will set the status to move
        elif distance <= self.notice_radius:
            self.status = 'move'
            self.status1 = 'move'
        #if none of these are true the enemy is idle
        else:
            self.status = 'idle'
            self.status1 = 'idle'
    #defines the action function which determines what to do based off of the status
    def actions(self,player):
        #if status is attack will play a attack sound and run the damage player function
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.attack_sound.play()
            self.damage_player(self.attack_damage,self.attack_type)
        #if the status is move it will move the enemy towards the player
        elif self.status == 'move':
            self.direction = self.get_player_distance(player)[1]
        else:
            self.direction = pygame.math.Vector2()
    #defines the animation function which deals with all enemy animations
    def animate(self):
        #gets the enemies animation based off of status
        animation = self.animations[self.status]
        #if your fighting the final boss it will set his attack animation to the direction hes attacking in
        if self.monster_name == 'Yatagarasu':
            if self.status == 'attack':
                if abs(self.direction[1]) > abs(self.direction[0]):
                    if self.direction[1] >= 0:
                        animation = [self.animations[self.status][0]]
                    elif self.direction[1] <= 0:
                        animation = [self.animations[self.status][3]]
                else:
                    if self.direction[0] >= 0:
                        animation = [self.animations[self.status][2]]
                    elif self.direction[0] <= 0:
                        animation = [self.animations[self.status][1]]
        #adds the animation speed to the frame index so it can loop through the animation frames
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        #sets the image based off of the current animation image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        #will blink the enemy in and out if he is hit
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    #defines the cooldown function which will deal with all enemy cooldowns
    def cooldown(self):
        #gets the current time
        current_time = pygame.time.get_ticks()
        #makes it so the enemies attacks dont hit hundreds of times in a second and rather 1 attack every 1 sec hde is in attack_radius
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        #sets a enemy invulnerability timer and sets the vulnerability back to true at the end
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True
    #defines the get damage function which will get the damage the enemy takes from the player
    def get_damage(self,player,attack_type):
        #checks if hes been hit
        if self.vulnerable:
            #plays the hit sound
            self.hit_sound.play()
            self.direction = self.get_player_distance(player)[1]
            #checks if the player attack with a weapon or magic then get its value and substracts it from health
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            #makes it so he cant get hit until the timer is over
            self.vulnerable = False
    #defines the check death function which will check if the enemy has died
    def check_death(self,player):
        #if self.health is less then 0 then the enemy is dead
        if self.health <= 0:
            #plays the death sound
            self.death_sound.play()
            #removes the boss arena boundary when the boss dies
            for sprite in self.obstacle_sprites:
                if sprite.sprite_type == 'Boss_arena':
                    player.bossfighting = False
                    sprite.kill()
            #kills the sprite
            self.kill()
            #triggers the death animation to play
            self.trigger_death_particles(self.rect.center,self.monster_name)
            #adds a certain amount of exp to the player
            self.add_exp(self.exp)
            #if the monster you killed was 'Akshar" it will play a cutscene and give you a strong weapon
            #that you can use to kill the final boss with
            if self.monster_name == 'Akshar':
                player.weaponinv = 5
                #plays dialog sound and displays all the text on screen
                self.dialogsound.play(loops=10)
                font = pygame.font.Font(UI_FONT, 24)
                text_surf = font.render('!EXCALIBUR AQUIRED!', False, TEXT_COLOR)
                x = 640
                y = 300
                text_rect = text_surf.get_rect(center=(x, y))
                pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
                self.display_surface.blit(text_surf, text_rect)
                pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
                pygame.display.update()
                pygame.time.delay(2000)
                font = pygame.font.Font(UI_FONT, 24)
                text_surf = font.render('Did... you think... that was it?...', False, TEXT_COLOR)
                x = 640
                y = 400
                text_rect = text_surf.get_rect(center=(x, y))
                pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
                self.display_surface.blit(text_surf, text_rect)
                pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
                pygame.display.update()
                pygame.time.delay(4000)
                #teleports the player
                player.hitbox.y = 8064
                player.hitbox.x = 15872
    #defintes the hit reaction function which will make it so on normal mode bosses aren't knocked back
    def hit_reaction(self):
        if not self.vulnerable:
            self.direction  *= -self.resistance
    #defines the draw dialog function which will draw the dialog box for NPC's
    def drawdialog(self):
        #plays the dialgo sound
        #draws dialog boxes one after another
        self.dialogsound.play(loops=10)
        font = pygame.font.Font(UI_FONT, 24)
        text_surf = font.render(self.dialog1, False, TEXT_COLOR)
        x = 640
        y = 300
        text_rect = text_surf.get_rect(center=(x, y))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
        pygame.display.update()
        pygame.time.delay(4000)
        self.dialogsound.play(loops=10)
        font = pygame.font.Font(UI_FONT, 24)
        text_surf = font.render(self.dialog2, False, TEXT_COLOR)
        x = 640
        y = 400
        text_rect = text_surf.get_rect(center=(x, y))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
        pygame.display.update()
        pygame.time.delay(4000)
        self.dialogsound.play(loops=10)
        text_surf = font.render(self.dialog3, False, TEXT_COLOR)
        x = 640
        y = 500
        text_rect = text_surf.get_rect(center=(x, y))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
        pygame.display.update()
        pygame.time.delay(4000)
        #stops the sound
        self.dialogsound.stop()
    #defines the boss arena function which deals with boss health bar, the arena, and music
    def Bossarena(self,player,layout):
        #gets the player distance and the arena csv layout, creates a bosses list to use later
        distance = self.get_player_distance(player)[0]
        layouts = layout
        bosses = ['raccoon','GiantFlame','Cyclopse','Akshar','Reptile','GiantFlame2','Yatagarasu']
        #checks if the current enemy is a boss
        if self.monster_name in bosses and distance < self.notice_radius and self.ranonce:
            #spawns in the boss arena tiles
            for style, layout in layouts.items():
                for row_index, row in enumerate(layout):
                    for column_index, column in enumerate(row):
                        if column != '-1':
                            x = column_index * TILESIZE
                            y = row_index * TILESIZE
                            Tile((x,y),[self.obstacle_sprites],'Boss_arena')
            #sets the boss notice radius to the size of the arena
            self.notice_radius = 5000
            #if your fighting the final boss it plays different music otherwise it plays the regular boss music
            if self.monster_name == 'Yatagarasu':
                player.finalorreg = True
                player.bossfighting = True
            else:
                player.finalorreg = False
                player.bossfighting = True
            self.ranonce = False
            self.healthbardisplay = True
        #checks if the current enemy is a boss and if so displays their health bar and their name at the bottom
        if self.monster_name in bosses and distance < self.notice_radiuss and self.healthbardisplay:
            #displays the boss health bar at the bottom
            max_amount = (monster_data[self.monster_name])['health']
            current = self.health
            color = HEALTH_COLOR
            bg_rect = pygame.Rect(340, 640, 600, 50)
            pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
            ratio = current / max_amount
            current_width = bg_rect.width * ratio
            current_rect = bg_rect.copy()
            current_rect.width = current_width
            font = pygame.font.Font(UI_FONT, 14)
            text = font.render(str(int(current)) + '/' + str(int(max_amount)), True, 'white')
            textRect = text.get_rect(center=self.health_bar_rect.center)
            pygame.draw.rect(self.display_surface, color, current_rect)
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
            self.display_surface.blit(text, textRect)
            #displays the boss name
            font = pygame.font.Font(UI_FONT, 14)
            mnstrname = self.monster_name
            if self.monster_name == 'Yatagarasu':
                mnstrname = 'Yatagarasu The Dark Lord'
                self.health += 0.25
            text_surf = font.render(mnstrname, False, 'gold')
            x = 340
            y = 620
            text_rect = text_surf.get_rect(topleft=(x, y))
            self.display_surface.blit(text_surf, text_rect)
    #defines the NPC interaction function which deals with npc interactions
    def NPC_interact(self,player):
        #makes a NPC list and get the distance from the player
        distance = self.get_player_distance(player)[0]
        NPCS = ['NPC1','NPC2','NPC3','NPC4','NPC5','NPC6']
        #checks if the current enemy is an NPC and if the player is close to him will display the
        #press F to interact box
        if self.monster_name in NPCS and distance < self.notice_radius:
            font = pygame.font.Font(UI_FONT, 20)
            text_surf = font.render('Press F to interact',False, TEXT_COLOR)
            x = 640
            y = 600
            text_rect = text_surf.get_rect(center=(x, y))
            pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
            self.display_surface.blit(text_surf, text_rect)
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
            #if the player presses F next to a npc will display their dialog
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.drawdialog()
    #defines the update function which will run all the previous functions
    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldown()
    #defines the enemy update functions which will run enemy specific functions
    def enemy_update(self,player):
        bosses = ['raccoon','GiantFlame','Cyclopse','Akshar','Reptile','GiantFlame2','Yatagarasu']
        self.get_status(player)
        self.actions(player)
        self.Bossarena(player,self.layout)
        self.NPC_interact(player)
        self.check_death(player)
        if self.monster_name in bosses:
            if self.difficulty:
                self.hit_reaction()