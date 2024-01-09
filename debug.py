#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Final Summative: Debug
# Author: Alex U
# Date: Jan 24 2023
# Description: This is the Debug function which i used to get important values when
# the game didnt work
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pygame
pygame.init()
font = pygame.font.Font(None,30)

#debug fucntion setup gets the display function and will display certain values on screen like (x,y) coords so its easier
#to code certain locations knwoing player x and y coords or any other entities location
#can also display other information
def debug(info, y = 10, x = 10):
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    pygame.draw.rect(display_surface, 'Black',debug_rect)
    display_surface.blit(debug_surf,debug_rect)