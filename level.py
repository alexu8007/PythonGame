#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Final Summative: Level
# Author: Alex U
# Date: Jan 24 2023
# Description: This is the level file which is the main game running file where the game runs
# this deals with map generations, camera mouvement, boundaries, music, saving and loadin, generating
# sprites(weapon, player, enemies, boss, npcs), Minimap, menu toggle, weapon and magic association
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#imports all the needed libraries
import sys
import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade

#defines the Level class which deals with all the level actions
class Level:
    def __init__(self,playerload,zz,difficulty):
        #get the display surface and sets initial values for font and difficulty
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        self.minimap = False
        self.font = pygame.font.Font(UI_FONT,30)
        self.font2 = pygame.font.Font(UI_FONT,4)
        self.difficulty = difficulty
        #setsup the sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.current_attack = None
        self.playerload = playerload
        #sets up the map based off of the create map function
        self.create_map()
        #create the player UI based off of the UI functino
        self.ui = UI()
        #sets the animation player attribute up
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)
        self.upgrade = Upgrade(self.player)
        #sets up all the music that will play in the game, it sets their volume as well so its not too loud
        self.main_sound = pygame.mixer.Sound('./audio/main.wav')
        self.main_sound.set_volume(0.04)
        self.bossmusic = pygame.mixer.Sound('./audio/bossfight.wav')
        self.bossmusic.set_volume(0.04)
        self.finalbossmusic = pygame.mixer.Sound('./audio/final.wav')
        self.finalbossmusic.set_volume(0.04)
        #plays main music and sets some variables up
        self.switchh = True
        self.main_sound.play(loops=-1)
        self.menusent = False
    #defines the create_map function which will create the map, the boundaries and all the entities
    def create_map(self):
        #sets up the layouts dictionary for use in the map creation
        layouts = {
            'boundary': import_csv_layout('./map/mapidea_boundary.csv'),
            'grass': import_csv_layout('./map/mapidea_grass.csv'),
            'object': import_csv_layout('./map/map_LargeObjects.csv'),
            'entities': import_csv_layout('./map/mapidea_Entities.csv')
        }
        # sets up the graphics dictionary for use in the map creation
        graphics = {
            'grass':import_folder('./graphics/Grass'),
            'objects': import_folder('./graphics/objects')
        }
        #gets the style and the layout from the layouts dic
        for style,layout in layouts.items():
            #gets the rows of the csv
            for row_index, row in enumerate(layout):
                #gets the column in the row of the csv
                for column_index, column in enumerate(row):
                    #if column is not equal -1 i.e. something is there will execute the following functions
                    if column != '-1':
                        x = column_index*TILESIZE
                        y = row_index*TILESIZE
                        #if the player chose to load the game it will set self.playerload to true and execute the load function
                        if self.playerload and column == '394':
                            loadinfile = open("Savefile.txt", "r")
                            loadeddata = (loadinfile.read().splitlines())
                            x = int(loadeddata[15])
                            y = int(loadeddata[16])
                        #if the style is boundary which means it a border it will set up the tile as obstacle sprite but not visible
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible')
                        #if the style is grass will set it up as grass picture and make it attackable while being an object so that
                        #the player can break it
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites,self.obstacle_sprites,self.attackable_sprites], 'grass',random_grass_image)
                        #if the style is entities it will spawn in the entites based off of the csv valeu in the file
                        #different enemies have diffirent csv values so we can ensure each entity is generated properly
                        if style == 'entities':
                            if column == '394':
                                self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites,self.create_attack,self.destroy_weapon,self.create_magic)
                            else:
                                dialog1 = ''
                                dialog2 = ''
                                dialog3 = ''
                                if column == '390': monster_name = 'bamboo'
                                elif column == '382': monster_name = 'dragon'
                                elif column == '381': monster_name = 'dragon2'
                                elif column == '380': monster_name = 'beast'
                                elif column == '379': monster_name = 'GiantFlame'
                                elif column == '378': monster_name = 'Reptile'
                                elif column == '377':
                                    monster_name = 'GiantFlame2'
                                elif column == '376':
                                    monster_name = 'Akshar'
                                elif column == '362':
                                    monster_name = 'NPC1'
                                    dialog1 = 'The Dark Lord has taken over...'
                                    dialog2 = 'All living creatures have fallen under his control...'
                                    dialog3 = 'I dont know how much longer i have...'
                                elif column == '361':
                                    monster_name = 'NPC2'
                                    dialog1 = 'The Raccoon lies ahead...'
                                    dialog2 = 'He is quite the formidable foe'
                                    dialog3 = 'Make sure your well prepared before you fight him...'
                                elif column == '360':
                                    monster_name = 'NPC3'
                                    dialog1 = 'Whoaa!'
                                    dialog2 = 'Watch out theres a lot of dragons up ahead!'
                                    dialog3 = 'I heard one of the Dark Lords Great Warriors is among them...'
                                elif column == '359':
                                    monster_name = 'NPC4'
                                    dialog1 = 'These lands are ruined...'
                                    dialog2 = 'The Great Spirit is blocking access to the holy lands'
                                    dialog3 = 'Be careful he is no ordinary foe...'
                                elif column == '358':
                                    monster_name = 'NPC5'
                                    dialog1 = 'Soilders... Civilians... all gone...'
                                    dialog2 = 'Im all thats left...'
                                    dialog3 = 'Please great warrior save this tarnished land'
                                elif column == '357':
                                    monster_name = 'NPC6'
                                    dialog1 = 'The Dark Lord awaits ahead'
                                    dialog2 = 'Many have tried before you, ive kept count...'
                                    dialog3 = 'youre number.... 3708, Good luck Warrior'
                                elif column == '405':
                                    monster_name = 'Yatagarasu'
                                elif column == '391': monster_name = 'spirit'
                                elif column == '392': monster_name = 'raccoon'
                                elif column == '395': monster_name = 'cyclopse'
                                else: monster_name = 'squid'
                                #once it gets the monster name it will set up the enemy by getting the info from the settings file based off of the name of the given enemy in the csv value
                                Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.damage_player,self.trigger_death_particles,self.add_xp,self.difficulty,dialog1,dialog2,dialog3)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # remenants of a rendering system that can be put in place
    # def create_map2(self):
    #     layouts = {
    #         'boundary': import_csv_layout('./map/mapidea_boundary.csv'),
    #         'grass': import_csv_layout('./map/mapidea_grass.csv'),
    #         'object': import_csv_layout('./map/map_LargeObjects.csv'),
    #         'entities': import_csv_layout('./map/mapidea_Entities.csv')
    #     }
    #     graphics = {
    #         'grass': import_folder('./graphics/Grass'),
    #         'objects': import_folder('./graphics/objects')
    #     }
    #     for style, layout in layouts.items():
    #         for row_index, row in enumerate(layout):
    #             for column_index, column in enumerate(row):
    #                 if column != '-1':
    #                     x = column_index * TILESIZE
    #                     y = row_index * TILESIZE
    #                     if self.playerload and column == '394':
    #                         loadinfile = open("Savefile.txt", "r")
    #                         loadeddata = (loadinfile.read().splitlines())
    #                         x = int(loadeddata[15])
    #                         y = int(loadeddata[16])
    #                     if style == 'boundary':
    #                         Tile((x, y), [self.obstacle_sprites], 'invisible')
    #                     if style == 'grass':
    #                         random_grass_image = choice(graphics['grass'])
    #                         Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
    #                              'grass', random_grass_image)
    #                     if style == 'object':
    #                         surf = graphics['objects'][int(column)]
    #                         Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)
    #                     if style == 'entities':
    #                         if column == '394':
    #                             self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites,
    #                                                  self.create_attack, self.destroy_weapon, self.create_magic)
    #                         else:
    #                             if column == '390':
    #                                 monster_name = 'bamboo'
    #                             elif column == '382':
    #                                 monster_name = 'dragon'
    #                             elif column == '381':
    #                                 monster_name = 'dragon2'
    #                             elif column == '380':
    #                                 monster_name = 'beast'
    #                             elif column == '391':
    #                                 monster_name = 'spirit'
    #                             elif column == '392':
    #                                 monster_name = 'raccoon'
    #                             elif column == '395':
    #                                 monster_name = 'cyclopse'
    #                             else:
    #                                 monster_name = 'squid'
    #                             Enemy(monster_name, (x, y), [self.visible_sprites, self.attackable_sprites],
    #                                   self.obstacle_sprites, self.damage_player, self.trigger_death_particles,
    #                                   self.add_xp)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #defines the create attack function which will create a weapon from the settings file based on current selected weapon
    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])
    #defines the create magic functino which will create magic spells based off of a weapons style,strength and its cost
    #it will also play that magic in game
    def create_magic(self,style,strength,cost):
        if style == 'heal':
            self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])
        if style == 'flame':
            self.magic_player.flame(self.player,cost,[self.visible_sprites,self.attack_sprites])
        if style == 'flame2':
            self.magic_player.oblivion(self.player,cost,[self.visible_sprites,self.attack_sprites])
    #defines the destroy weapon function which will destroy the weapon sprite after youve attacked
    def destroy_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
    #defiens the player attack logic function which will determine what happens if a attack interacts with a sprite
    def player_attack_logic(self):
        if self.attack_sprites:
            #scans the whole attack sprite list
            for attack_sprite in self.attack_sprites:
                #gets the sprites that collide
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        #if the attack collides with a grass sprite typ e it will execute a certain animation and delete the grass
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos - pygame.math.Vector2(0,60),[self.visible_sprites])
                            target_sprite.kill()
                        #if its not grass which means its a enemy that can be damages will get the damage that the attack should do
                        #then it will run animation for the excalibur weapon if you have it equipped
                        #finally runs the get damge function
                        else:
                            weapnn = False
                            pos = target_sprite.rect.center
                            keys = pygame.key.get_pressed()
                            if keys[pygame.K_SPACE]:
                                weapnn = True
                            if self.player.weapon_index == 5 and weapnn:
                                self.animation_player.create_weapon_particles(pos,[self.visible_sprites])
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)
    #defines the damage player function which will execute if the player is hit
    def damage_player(self,amount,attack_type):
        #if the player is not currently invincible(recently hit) it will run the following if statement
        if self.player.vulnerable:
            #it will remove the players health based off of the th endurance stat
            self.player.health -= (amount - self.player.endurance)
            self.player.vulnerable = False
            #sets the invincibilty timer back
            self.player.hurt_time = pygame.time.get_ticks()
            #creates and attack sprite where the player was
            self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])
    #defines the function that triggers a death animation when an enemy dies
    def trigger_death_particles(self,pos,particle_type):
        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)
    #toggles the menu function which is used in main to check if the menu is open or not
    def toggle_menu(self):
        self.game_paused = not self.game_paused

    # toggles the menu function which is used in main to check if the minimap is open or not
    def toggle_map(self):
        self.minimap = not self.minimap
    #adds xp to the player based off of the enemy exp amount
    def add_xp(self,amount):
        self.player.exp += amount
    #check death function which checks for the player death
    def check_death(self):
        if self.player.health <= 0:
            #if player health is under 0 which means hes dead
            #stops all the music
            self.main_sound.stop()
            self.bossmusic.stop()
            self.finalbossmusic.stop()
            #plays a game over sound effect and ends the game
            death_sound = pygame.mixer.Sound('./audio/GameOver.wav')
            death_sound.set_volume(0.04)
            death_sound.play()
            self.display_surface.fill('black')
            x = 640
            y = 360
            text_surf = self.font.render('GAMEOVER', False, TEXT_COLOR)
            text_rect = text_surf.get_rect(center=(x, y))
            self.display_surface.blit(text_surf, text_rect)
            pygame.display.update()
            pygame.time.delay(5000)
            #sends the player back to the menu by returning False
            return False
        else:
            return True
    #checks if the player clicked the return to menu button and if so will send him back to the menu
    def checkifmenu(self):
        if self.menusent:
            return False
        return True
    #defines the save function which will save all the players data into a save file
    def save(self):
        playerstats = [str(int(self.player.stats['health'])),str(int(self.player.stats['energy'])),str(int(self.player.stats['attack'])),str(int(self.player.stats['magic'])),
                       str(int(self.player.stats['speed'])),str(int(self.player.stats['stamina'])),str(int(self.player.stats['endurance'])),str(2000),str(1400),str(int(self.player.exp)),
                       str(int(self.player.upgrade_cost['health'])),str(int(self.player.upgrade_cost['energy'])),str(int(self.player.upgrade_cost['attack'])),str(int(self.player.upgrade_cost['magic'])),str(int(self.player.upgrade_cost['speed'])),
                       str(int(self.player.xcoor)),str(int(self.player.ycoor)),str(int(self.player.lvl))]
        saveinfile = open("Savefile.txt", "w")
        #puts the variables in the save file and then closes it
        for i in range(len(playerstats)):
            saveinfile.write(playerstats[i] + '\n')
        saveinfile.close()
    #defines the load game function which will load the players stats back and his position on the map
    def load(self):
        loadinfile = open("Savefile.txt", "r")
        loadeddata = (loadinfile.read().splitlines())
        self.player.stats['health'] = int(loadeddata[0])
        self.player.stats['energy'] = int(loadeddata[1])
        self.player.stats['attack'] = int(loadeddata[2])
        self.player.stats['magic'] = int(loadeddata[3])
        self.player.stats['speed'] = int(loadeddata[4])
        self.player.stats['stamina'] = int(loadeddata[5])
        self.player.stats['endurance'] = int(loadeddata[6])
        self.player.exp = int(loadeddata[9])
        self.player.upgrade_cost['health'] = int(loadeddata[10])
        self.player.upgrade_cost['energy'] = int(loadeddata[11])
        self.player.upgrade_cost['attack'] = int(loadeddata[12])
        self.player.upgrade_cost['magic'] = int(loadeddata[13])
        self.player.upgrade_cost['speed'] = int(loadeddata[14])
        self.player.lvl = int(loadeddata[17])
        loadinfile.close()
    #defines the check next weapon function which will distribute items basef off of 10 level increments
    def checknextweapon(self):
        if self.player.lvl > 10 and self.player.lvl < 20:
            self.player.weaponinv = 1
        elif self.player.lvl > 20  and self.player.lvl < 30:
            self.player.weaponinv = 2
        elif self.player.lvl > 30  and self.player.lvl < 40:
            self.player.weaponinv = 3
        elif self.player.lvl > 40  and self.player.lvl < 50:
            self.player.weaponinv = 4
        elif self.player.lvl > 50:
            self.player.magicinv = 2
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # remenants of rendering system
    # def loadsecondpart(self):
    #     global zz
    #     if (self.player.ycoor < 9000) and zz == 4:
    #         self.save()
    #         self.playerload = True
    #         zz = 1
    #         return [False,zz,True]
    #     return [True,zz,False]
    #
    # def loadsecondpart2(self):
    #     global zz
    #     if (self.player.ycoor > 9000) and zz == 4:
    #         self.save()
    #         self.playerload = True
    #         zz = 0
    #         return [False,zz,True]
    #     return [True,zz,False]
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #defines the run function which is the main fucntion in the level class
    #this will run the entire game using multiple functions to display and change various aspects
    def run(self):
        #will draw all the sprites around the player
        self.visible_sprites.custom_draw(self.player)
        #will the display the UI based off of player stats
        self.ui.display(self.player)
        #checks if the game is paused(in menu) or if the player is in the minimap
        if self.game_paused or self.minimap:
            #if it was minimap will run the minimap function
            if self.minimap:
                #will display a png image of the minimap
                image = pygame.image.load('./Menu Buttons/map.PNG').convert_alpha()
                width = image.get_width()
                height = image.get_height()
                self.image = pygame.transform.scale(image, (int(width * 0.8), int(height * 0.8)))
                self.rect = self.image.get_rect()
                self.rect.center = (640, 360)
                self.display_surface.blit(self.image, (self.rect.x, self.rect.y))
                pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.rect.inflate(1, 1), 4)
            #if the game is paused it means the player is in the upgrade/main menu
            if self.game_paused:
                #will load all of the buttons in the game and their images
                image = pygame.image.load('./Menu Buttons/Square Buttons/Square Buttons/Return Square Button.png').convert_alpha()
                width = image.get_width()
                height = image.get_height()
                self.image = pygame.transform.scale(image, (int(width * 0.3), int(height * 0.3)))
                self.rect = self.image.get_rect()
                self.rect.topleft = (780, 654)
                self.display_surface.blit(self.image, (self.rect.x, self.rect.y))
                pos = pygame.mouse.get_pos()
                image = pygame.image.load('./Menu Buttons/Square Buttons/Square Buttons/Home Square Button.png').convert_alpha()
                width = image.get_width()
                height = image.get_height()
                self.image = pygame.transform.scale(image, (int(width * 0.3), int(height * 0.3)))
                self.rect2 = self.image.get_rect()
                self.rect2.topleft = (880, 654)
                self.display_surface.blit(self.image, (self.rect2.x, self.rect2.y))
                pos = pygame.mouse.get_pos()
                #whill check if either the dave button or the return to start menu button was pressed
                if self.rect.collidepoint(pos):
                    if pygame.mouse.get_pressed()[0] == 1:
                        #if the save button was pressed it will save the game
                        self.save()
                if self.rect2.collidepoint(pos):
                    if pygame.mouse.get_pressed()[0] == 1:
                        #if the return to start menu button was pressed and it will stop music and send the player back to menu
                        self.main_sound.stop()
                        self.bossmusic.stop()
                        self.finalbossmusic.stop()
                        self.menusent = True
                #runs the upgrade display fucntion which displays the upgrade boxes and lets the player choose what to upgrade
                self.upgrade.display()
            #autosave when closed menu
            self.save()
            #if not in menu or in minimap will check for next weapon and update the visible sprites as well as the enemy
        else:
            self.checknextweapon()
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            #runs the player attack logic function which will check if the player is currently attacking and runs commands as such
            self.player_attack_logic()
        #if bossfighting is true which mean the player is in a boss fight it will play boss music
        if self.player.bossfighting and self.switchh:
            self.main_sound.stop()
            #checks if it should play regualr boss music or final boss music
            if self.player.finalorreg:
                self.finalbossmusic.play(loops=-1)
            else:
                self.bossmusic.play(loops=-1)
            self.switchh = False
        # if bossfighting is false which mean the player is not in a boss fight it will play regular music
        if not self.player.bossfighting and not self.switchh:
            if self.player.finalorreg:
                self.finalbossmusic.stop()
            else:
                self.bossmusic.stop()
            self.main_sound.play(loops=-1)
            self.switchh = True

#this is the Camera class
class YSortCameraGroup(pygame.sprite.Group):
    #init method for the camera class which gets the png image that the player will be walking on
    def __init__(self):
        super().__init__()
        #gest the display surface
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        #sets an offset value to better display sprites
        self.offset = pygame.math.Vector2(100,200)
        #gets the map and its rect
        self.floor_surface = pygame.image.load('./graphics/tilemap/mapidea.png').convert_alpha()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))
    #defines the custom draw function
    def custom_draw(self,player):
        #gets the offset x and y coords and updates them
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        #offests the floor by a certain amount
        floor_offset_pos = self.floor_rect.topleft - self.offset
        #displays the map underneath the player
        self.display_surface.blit(self.floor_surface,floor_offset_pos)
        #sets up a lambda expression which for every sprite will get sprite.rect.centery
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_rect = sprite.rect.topleft - self.offset
            #displayes the sprites
            self.display_surface.blit(sprite.image.convert_alpha(),offset_rect)
    #defines the enemy update function which will set up the enemy sprites and for each enemy will run teh enemy update function which is within the enemy class
    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type')and sprite.sprite_type == 'enemy']
        #rusn through each enemy
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

