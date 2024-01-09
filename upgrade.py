#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Final Summative: Upgrade
# Author: Alex U
# Date: Jan 24 2023
# Description: This is the Upgrade file, this is where the player upgrade menu displays
# it is also where the players stats are increased and cost is increased, additionally
# it displays a return to menu button and a save button
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import pygame
from settings import *
from level import *

#defines the Upgrade class which is responsible for the upgrade menu displaying and
#all of its functionality from increasing the players stats, increasing cost, increasing lvl
class Upgrade():
    def __init__(self,player):
        #sets initial variables for the class
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_nr = len(player.stats) - 2
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
        self.lvl = 0
    #defines the input function which will check for user inputs and determine what to do with them
    def input(self):
        #gets the key pressed
        keys = pygame.key.get_pressed()
        #if self.can_mose is true lets you move thorugh the upgrade boxes
        if self.can_move:
            #if player click on the right arrow key moves the selection box(white box) to the right
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            #if player clicks to the left moves the selection box to the left
            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            #if player clicks on space(confirming an update) it will run the function to increase the player stats
            #and increase the cost and level
            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)
    #defines the create item function which will make the attributes for the 5 boxes that will display
    #it will be used later to check what is upgraded and which is the current selection
    def create_items(self):
        #makes a empty list
        self.item_list = []
        #makes 5 item objects each with different values for the 5 item boxes to be displayed
        for item,index in enumerate(range(self.attribute_nr)):
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_nr
            left = (item * increment) + (increment -self.width) // 2

            top = self.display_surface.get_size()[1] * 0.1
            #makes a item Object from the Item class from the previous calculated values
            item = Item(left,top,self.width,self.height,index,self.font,self.player)
            #adds the item to the list
            self.item_list.append(item)
    #defines the selection cooldown so that pressing right or left wont move over hundreds of times
    #as python counts a input if your right arrow is pressed so for the 0.2-0.5 sec that your key is pressed
    #it will move multiple times not just once, this function makes sure you can only move the box once every 0.3 sec
    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True
    #defines the display function which will display the whole upgrade menu
    def display(self):
        #checks the input of the user
        self.input()
        self.selection_cooldown()
        # for each item it will set values to be used in the bar,title,cost and box creation
        for index, item in enumerate(self.item_list):
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface,self.selection_index,name,value,max_value,cost)

#defines the Item class which is responsible for the creation of each of the 5 boxes
class Item():
    def __init__(self,l,t,w,h,index,font,player):
        #sets initial values
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font
        self.player = player
    #defines the display names function which will display the name above the box(health,energy,attack)
    #then it will display the cost and the level.
    def display_names(self,surface,name,cost,selected,player):
        #displays the level
        text_surf = self.font.render('Level: '+str(int(player.lvl)), False, TEXT_COLOR)
        x = 1060
        y = 689
        text_rect = text_surf.get_rect(center=(x, y))
        pygame.draw.rect(surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        surface.blit(text_surf, text_rect)
        pygame.draw.rect(surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)
        #displays the title and the cost based off of object attributes
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        title_surf = self.font.render(name,False,color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))
        cost_surf = self.font.render(f'{int(cost)}',False,color)
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0,20))
        surface.blit(title_surf,title_rect)
        surface.blit(cost_surf, cost_rect)
    #defines the display bar function which will display the bar going down the middle of the box
    #the bar is there to indicate the player if theyve reached the maximum upgradebility of that stat
    def display_bar(self,surface,value,max_value,selected):
        #gest the location of where to place the bar based off of object attributes
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0,60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR
        #sets its full height
        full_height = bottom[1] - top[1]
        relative_number = (value/max_value) * full_height
        #gets the actual value to display
        value_rect = pygame.Rect(top[0]-15,bottom[1]-relative_number,30,10)
        pygame.draw.line(surface,color,top,bottom,5)
        pygame.draw.rect(surface, color, value_rect)
    #defines the trigger function which will run once the player has pressed space and therefore
    #opted to upgrade one of his stats
    def trigger(self,player):
        #gets the player attribues
        upgrade_attribute = list(player.stats.keys())[self.index]
        #checks if the player has enough exp and that the stat he wants to upgrade isnt at its maximum value
        if player.exp >= player.upgrade_cost[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
            player.exp -= player.upgrade_cost[upgrade_attribute]
            #checks which stat it is and increases it by a certain multiplication value
            if upgrade_attribute == 'speed':
                player.stats[upgrade_attribute] *= 1.05
                player.stats['stamina'] *= 1.1
            elif upgrade_attribute == 'health':
                player.stats[upgrade_attribute] *= 1.1
                player.stats['endurance'] += 0.5
            else:
                player.stats[upgrade_attribute] *= 1.1
            #increase the upgrade cost of the attribute, and the level by one
            player.upgrade_cost[upgrade_attribute] *= 1.2
            player.lvl += 1
        #checks if his stats are above the max and if so regulates it
        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]
    #defines the display fucntion which will display the 5 boxes, the bars, title and cost
    def display(self,surface,selection_num,name,value,max_value,cost):
        #makes the box your currently on white to indicate it is your current selection
        if self.index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            #draws other boxes normally if they arent the one you have selected
            pygame.draw.rect(surface,UI_BG_COLOR,self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect,4)
        #displays the title,cost and bar
        self.display_names(surface,name,cost,self.index == selection_num,self.player)
        self.display_bar(surface, value, max_value, self.index == selection_num)
