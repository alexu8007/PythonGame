#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Final Summative: UI
# Author: Alex U
# Date: Jan 24 2023
# Description: This is the UI file where the player UI is displayed. the UI includes
# health bar, energy bar, stamina bar, weapon display, magic display and exp display
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pygame
from settings import *

#defines the UI class which will deal with teh player ui and its functions
class UI:
    def __init__(self):
        #sets up initial attributes for the UI object
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
        #sets up rectangles for each bar
        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10,34, ENERGY_BAR_WIDTH, BAR_HEIGHT)
        self.stamina_bar_rect = pygame.Rect(10, 58, 160, BAR_HEIGHT)
        self.weapon_graphics = []
        #gest the weapon image so it can display in the bottom left corner
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)
        self.magic_graphics = []
        #gets the magic images so that it can display in the bottom left corner
        for magic in magic_data.values():
            magic = pygame.image.load(magic['graphic']).convert_alpha()
            self.magic_graphics.append(magic)
    #defines the show bar methond which will display the health, mana and stamina bar as well as updating them based off of changing player attributes
    def show_bar(self,current,max_amount,bg_rect,color):
        global z
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        font = pygame.font.Font(UI_FONT,14)
        #if the color is red therefore hp will display as such
        if color == 'red':
            text = font.render(str(int(current))+'/'+str(int(max_amount)),True,'white')
            textRect = text.get_rect(center = self.health_bar_rect.center)
        #if the color is blue therefore mana will display as such
        if color == 'blue':
            text = font.render(str(int(current))+'/'+str(int(max_amount)),True,'white')
            textRect = text.get_rect(center = self.energy_bar_rect.center)
        #if the color is green therefore stamina will display as such
        if color == 'green':
            text = font.render(str(int(current)) + '/' + str(int(max_amount)), True, 'white')
            textRect = text.get_rect(center=self.stamina_bar_rect.center)
        #displayes the bars
        pygame.draw.rect(self.display_surface,color,current_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
        self.display_surface.blit(text, textRect)
    #defines the show exp function which will display the xp counter in the bottom right hand corner
    def show_exp(self,exp):
        #displays the exp based off player attributes and coordinates
        text_surf = self.font.render(str(int(exp)),False,TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x,y))
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(20,20))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(20,20),3)
    #defines the selection box function which will display the weapon and magic in the bottom left corner
    def selection_box(self,left,top,has_switched):
        #draws the item box
        bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        #makes the box gold if the player has just switched weapons
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect,3)
        return bg_rect
    #defines the weapon overlay function which will display the weapon within the item box
    def weapon_overlay(self,weapon_index,has_switched):
        #checks which weapon to place in the box
        bg_rect =self.selection_box(40,600,has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)
        #updates the display
        self.display_surface.blit(weapon_surf,weapon_rect)

    # defines the magic overlay function which will display the spell within the item box
    def magic_overlay(self,magic_index,has_switched):
        #gets the image based off index and display that image into the item box
        bg_rect = self.selection_box(110, 610, has_switched)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(magic_surf, magic_rect)
    #defines the display function which will use all the previous functions to display each of the bars
    #the item boxes the weapons with the item boxes, the exp counter and change the color of the item box based off of if the player switched the weapon
    def display(self,player):
        #display the bars at the top
        self.show_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_bar(player.stamina, player.stats['stamina'], self.stamina_bar_rect, 'green')
        #display the show exp function
        self.show_exp(player.exp)
        #displays the weapon and magic in their item boxes
        self.weapon_overlay(player.weapon_index,not player.switch_weapon)
        self.magic_overlay(player.magic_index, not player.switch_magic)