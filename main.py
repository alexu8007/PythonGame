#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Final Summative: Main
# Author: Alex U
# Date: Jan 24 2023
# Description: This is the main file where the game will execute from. It includes game info
# The running function and the menu.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import time
import pygame, sys
from settings import *
from level import *

# this is the game Class which deals with everything that involves the running of the game and its menus
class Game:
    #def init method to set up attributes
    def __init__(self,x,y,scale,x2,y2):
        #initialises pygame and sets attributes for the game class that will be used later
        pygame.init()
        pygame.display.set_caption("Warrior Souls")
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock()
        self.loadorrender = True
        self.zz = 0
        self.font = pygame.font.Font(UI_FONT,30)
        self.fontt = pygame.font.Font(UI_FONT,70)
        self.font2 = pygame.font.Font(UI_FONT, 18)
        self.font3 = pygame.font.Font(UI_FONT, 11)
        #sets up the sounds and music for the menu screen and for the button clicks
        self.menu_sound = pygame.mixer.Sound('./audio/lobby.wav')
        self.main_sound = pygame.mixer.Sound('./audio/main.wav')
        self.menu_sound.set_volume(0.04)
        self.main_sound.set_volume(0.04)
        self.click = pygame.mixer.Sound('./audio/Click.wav')
        self.click.set_volume(0.04)
        self.tr = False
        self.canplay = True
        self.difficulty = True
    #this is the run function where the game runs here it checks for if its a new game or load file
    #it will also deal with exitings the game as well as menu a minimap toggle
    def run(self):
        #initialises the level function to a object attribute
        self.level = Level(self.playerload,self.zz,self.difficulty)
        #checks if the game should be loaded or a new game
        if self.playerload:
            self.level.load()
        #running conditions for the game are checked and must all be True to run
        running = True
        running2 = True
        running3 = True
        running4 = True
        while running and running2 and running3 and running4:
            #checks if the player has closed the game, in that case it will exit program
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #if player presses m it will open the menu function
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()
                #if player presses n it will open the minimap
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        self.level.toggle_map()
                #if player presses s it will save the game, saving can also be done within the menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.level.save()
            #fill the screen with the same color as water sprite to make sure there arent any black holes
            self.screen.fill(WATER_COLOR)
            #after level is created it will run the level function which will begin the game
            self.level.run()
            #checks if the player sprite is dead
            running = self.level.check_death()
            #checks if the player has clicked the return to menu button
            running4 = self.level.checkifmenu()
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            #this entire section is part of a rendering system that can be put in place for larger maps
            #this ensure that the game can alternate map sizes with minor adjustements to the code
            #currently it is not in use as a triggering condition has been set as False
            #however for future refrence if larger map were to be desired it is here
            # runningg = self.level.loadsecondpart()
            # running2 = runningg[0]
            # if running2 == False:
            #     self.loadorrender = False
            #     self.zz = runningg[1]
            #     self.playerload = runningg[2]
            # else:
            #     runninggg = self.level.loadsecondpart2()
            #     running3 = runninggg[0]
            #     if running3 == False:
            #         self.loadorrender = False
            #         self.zz = runninggg[1]
            #         self.playerload = runninggg[2]
            # Lines: 2248
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            #updates the python display
            pygame.display.update()
            #sets the time and fps
            self.clock.tick(60)
    #defines the info function which will display all the game info once the player clicks on it in the main menu
    def info(self):
        #fills the screen with a background color
        self.screen.fill('#737373')
        #these following lines will display different text boxes and images that help the player learn how to play the game
        text_surf = self.font2.render('Welcome to the info page, this page will teach you how to play the game', False, TEXT_COLOR)
        x = 640
        y = 80
        text_rect = text_surf.get_rect(center=(x, y))
        pygame.draw.rect(self.screen, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.screen.blit(text_surf, text_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
        text_surf = self.font.render('CONTROLS', False, TEXT_COLOR)
        x = 240
        y = 160
        text_rect = text_surf.get_rect(center=(x, y))
        pygame.draw.rect(self.screen, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.screen.blit(text_surf, text_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
        text_surf = self.font2.render('Attack/select: SPACE', False, TEXT_COLOR)
        x = 240
        y = 210
        text_rect = text_surf.get_rect(center=(x, y))
        pygame.draw.rect(self.screen, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.screen.blit(text_surf, text_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
        text_surf = self.font2.render('MOVE: ARROWKEYS', False, TEXT_COLOR)
        x = 240
        y = 255
        text_rect = text_surf.get_rect(center=(x, y))
        pygame.draw.rect(self.screen, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.screen.blit(text_surf, text_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
        text_surf = self.font2.render('SWITCH WEAPON: Q', False, TEXT_COLOR)
        x = 240
        y = 300
        text_rect = text_surf.get_rect(center=(x, y))
        pygame.draw.rect(self.screen, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.screen.blit(text_surf, text_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
        text_surf = self.font2.render('SWITCH MAGIC: E', False, TEXT_COLOR)
        x = 240
        y = 345
        text_rect = text_surf.get_rect(center=(x, y))
        pygame.draw.rect(self.screen, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.screen.blit(text_surf, text_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
        text_surf = self.font2.render('USE MAGIC: LCTRL', False, TEXT_COLOR)
        x = 240
        y = 390
        text_rect = text_surf.get_rect(center=(x, y))
        pygame.draw.rect(self.screen, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.screen.blit(text_surf, text_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
        text_surf = self.font2.render('SAVE: S', False, TEXT_COLOR)
        x = 240
        y = 435
        text_rect = text_surf.get_rect(center=(x, y))
        pygame.draw.rect(self.screen, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.screen.blit(text_surf, text_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
        text_surf = self.font2.render('MENU: M', False, TEXT_COLOR)
        x = 240
        y = 480
        text_rect = text_surf.get_rect(center=(x, y))
        pygame.draw.rect(self.screen, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.screen.blit(text_surf, text_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
        text_surf = self.font3.render('Objective is to kill all the bosses and reach the final boss', False, TEXT_COLOR)
        x = 288
        y = 540
        text_rect = text_surf.get_rect(center=(x, y))
        pygame.draw.rect(self.screen, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.screen.blit(text_surf, text_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
        #these will make clickable buttons that the player can use to set the difficulty and also return to menu
        text_surf = self.font.render('BACK', False, TEXT_COLOR)
        x = 1180
        y = 640
        text_rect = text_surf.get_rect(center=(x, y))
        self.back_rect = text_rect
        pygame.draw.rect(self.screen, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.screen.blit(text_surf, text_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
        text_surf = self.font.render('EASY', False, TEXT_COLOR)
        x = 1180
        y = 440
        text_rect = text_surf.get_rect(center=(x, y))
        self.easy_rect = text_rect
        pygame.draw.rect(self.screen, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.screen.blit(text_surf, text_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
        text_surf = self.font.render('NORMAL', False, TEXT_COLOR)
        x = 1194
        y = 340
        text_rect = text_surf.get_rect(center=(x, y))
        self.normal_rect = text_rect
        pygame.draw.rect(self.screen, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.screen.blit(text_surf, text_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
        image = pygame.image.load('./Menu Buttons/Inkedinfo.PNG').convert_alpha()
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * 0.4), int(height * 0.4)))
        self.rect = self.image.get_rect()
        self.rect.center = (850, 255)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        image = pygame.image.load('./Menu Buttons/info2.PNG').convert_alpha()
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * 0.4), int(height * 0.4)))
        self.rect = self.image.get_rect()
        self.rect.center = (850, 555)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
    #this is the menu function from which the starting menu will load from
    def menu(self):
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #remanants of a rendering system
        if self.loadorrender == True:
            self.playerload = False
        running = self.loadorrender
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #fill the screen in a certain color
        self.screen.fill('#737373')
        #this will load the background image for the start menu
        image = pygame.image.load('./Menu Buttons/background.PNG').convert_alpha()
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * 1.2), int(height * 1.2)))
        self.rect = self.image.get_rect()
        self.rect.center = (640, 360)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        #this will make the title
        text_surf = self.fontt.render('Warrior Souls', False, TEXT_COLOR)
        x = 640
        y = 120
        text_rect = text_surf.get_rect(center=(x, y))
        pygame.draw.rect(self.screen, UI_BG_COLOR, text_rect.inflate(200, 20))
        self.screen.blit(text_surf, text_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, text_rect.inflate(200, 20), 4)
        #these three functions will make the 3 buttons for newgame, loadgame and game info
        text_surf = self.font.render('New Game', False, TEXT_COLOR)
        x = 640
        y = 290
        text_rect = text_surf.get_rect(center=(x, y))
        self.newgamerect = text_rect
        pygame.draw.rect(self.screen, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.screen.blit(text_surf, text_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
        text_surf = self.font.render('Load Game', False, TEXT_COLOR)
        x = 640
        y = 390
        text_rect = text_surf.get_rect(center=(x, y))
        self.loadgamerect = text_rect
        pygame.draw.rect(self.screen, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.screen.blit(text_surf, text_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
        text_surf = self.font.render('Game Info', False, TEXT_COLOR)
        x = 640
        y = 490
        text_rect = text_surf.get_rect(center=(x, y))
        self.infogamerect = text_rect
        pygame.draw.rect(self.screen, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.screen.blit(text_surf, text_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, text_rect.inflate(20, 20), 4)
        self.menu_sound.play(loops=-1)
        #This is the while function that continuously runs the start menu
        while running:
            #gets the position of the mouse on the screen
            pos = pygame.mouse.get_pos()
            #if the mouse position and the new geme rect collide it will check if the mouse is also clicked down it will execute the following code
            if self.newgamerect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    #will play some music
                    self.click.play()
                    #this will play the start of game cutscene where it will introduce the player to the game
                    self.screen.fill('black')
                    x = 650
                    y = 100
                    text_surf = self.font.render('Welcome Wanderer', False, TEXT_COLOR)
                    text_rect = text_surf.get_rect(center=(x, y))
                    self.screen.blit(text_surf, text_rect)
                    pygame.display.update()
                    pygame.time.delay(2000)
                    x = 650
                    y = 200
                    text_surf = self.font2.render('You awake from a deep slumber not recognizing anything around you...', False, TEXT_COLOR)
                    text_rect = text_surf.get_rect(center=(x, y))
                    self.screen.blit(text_surf, text_rect)
                    pygame.display.update()
                    pygame.time.delay(2000)
                    x = 650
                    y = 300
                    text_surf = self.font2.render('You look around you and find a sword...', False, TEXT_COLOR)
                    text_rect = text_surf.get_rect(center=(x, y))
                    self.screen.blit(text_surf, text_rect)
                    pygame.display.update()
                    pygame.time.delay(2000)
                    x = 650
                    y = 400
                    text_surf = self.font2.render('A sense of purpose grows over you as you get up', False, TEXT_COLOR)
                    text_rect = text_surf.get_rect(center=(x, y))
                    self.screen.blit(text_surf, text_rect)
                    pygame.display.update()
                    pygame.time.delay(2000)
                    x = 650
                    y = 500
                    text_surf = self.font2.render('A new journey has just begun...', False, TEXT_COLOR)
                    text_rect = text_surf.get_rect(center=(x, y))
                    self.screen.blit(text_surf, text_rect)
                    pygame.display.update()
                    pygame.time.delay(2000)
                    #will stop the menu while loop and will play the game
                    self.canplay = True
                    running = False
            #if the player clicks on the loadgame button it will run the load game function and stop the menu
            if self.loadgamerect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    #plays a sound and loads the game
                    self.click.play()
                    self.playerload = True
                    self.canplay = True
                    running = False
            # if the player clicks on the gameinfo button it will run the info function and stop the menu
            if self.infogamerect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    #will run the info function and activate a attribute that makes it so you can click on the back button
                    self.click.play()
                    self.info()
                    #makes it so you can click on the back button
                    self.tr = True
            #if you can click on the back button i.e. you are in game menu it will check if youve clicked it and if you have it will take you to menu
            if self.tr:
                if self.back_rect.collidepoint(pos):
                    if pygame.mouse.get_pressed()[0] == 1:
                        #will play a sound and take you to menu
                        self.click.play()
                        self.canplay = False
                        running =False
                #if your in the game menu it will check if you've clicked easy mode and if so will aplly easy mode
                if self.easy_rect.collidepoint(pos):
                    if pygame.mouse.get_pressed()[0] == 1:
                        #plays a sounds and sets the difficulty to false therefore easy
                        self.click.play()
                        self.difficulty = False
                if self.normal_rect.collidepoint(pos):
                    if pygame.mouse.get_pressed()[0] == 1:
                        # plays a sounds and sets the difficulty to True therefore normal
                        self.click.play()
                        self.difficulty = True
            #checks if the player has quit the game and if so will stop the program
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            #updates the screen
            pygame.display.update()
            #sets clock and fps
            self.clock.tick(60)
        #stops the menu sound and rendering variable
        self.menu_sound.stop()
        self.loadorrender = True

#this is where everything starts running, from the start menu to the game running
#it cycles through menu and play to ensure that the player is either playing or in a menu and not neither
if __name__ == '__main__':
    game = Game(200, 300, 0.5, 800, 300)
    while True:
        game.menu()
        if game.canplay:
            game.run()