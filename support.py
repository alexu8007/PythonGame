#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Final Summative: Support
# Author: Alex U
# Date: Jan 24 2023
# Description: This is the support file which will import all the comma seperated value
# layouts and the folder path for certain items
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pygame
from csv import reader
from os import walk

#definees the import csv layout which will import the cssv based off a path given and place it into
# a list that the computer can read to be able to properly rendering things in based on their csv values
def import_csv_layout(path):

    terrian_map = []

    with open(path) as level_map:
        layout = reader(level_map,delimiter = ',')
        for row in layout:
            terrian_map.append(list(row))

        return terrian_map
#defines the import folder function which takes the given path and import the folders and all the images in the folder
def import_folder(path):
    surface_list = []
    #loops through every image in the folder
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            print(full_path)
            image_surf = pygame.image.load(full_path).convert_alpha()
            #adds the completed image to a list that is returned
            surface_list.append(image_surf)
        return surface_list