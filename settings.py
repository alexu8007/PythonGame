#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Final Summative: Settings
# Author: Alex U
# Date: Jan 24 2023
# Description: This is the Settings file that holds all of the settings for the game to run
# settings include Tilesize, Colors, Constant values and player and enemy attributes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#sets the width and height of the screen
WIDTH    = 1280
HEIGTH   = 720
#sets the FPS of the game
FPS      = 60
#tilesize of each tile in the game
TILESIZE = 64
#gest the bar heights for all the bars in the game
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
#item bos size values
ITEM_BOX_SIZE = 80
#gets the world map which was used previously before world map generating was implemented
WORLD_MAP = [
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ','p',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
]
#sets the general font size for the game and the font used
UI_FONT = './graphics/font/joystix.ttf'
UI_FONT_SIZE = 18
#sets the color for various variables used in the game
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'
#sets the inital values fo each of the waepons in the game it includes images damage and cooldowns
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'./graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 200, 'damage': 30,'graphic':'./graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 50, 'graphic':'./graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'damage': 45, 'graphic':'./graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'damage': 60, 'graphic':'./graphics/weapons/sai/full.png'},
	'Excalibur':{'cooldown': 320, 'damage': 300, 'graphic':'./graphics/weapons/Excalibur/full.png'}}
#sets the magic data for all the spells which include the images the cost and the damage
magic_data = {
	'flame': {'strength': 20,'cost': 20,'graphic':'./graphics/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'./graphics/particles/heal/heal.png'},
	'flame2': {'strength': 150,'cost': 20,'graphic':'./graphics/particles/thunder/4.png'}}
#sets the monster data for the monsters and the npcs in the game, the enemies all have hp, exp,damage,attack_types,sounds,speed and resistance
monster_data = {
	'squid': {'health': 300,'exp':200,'damage':20,'attack_type': 'slash', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 3000,'exp':10000,'damage':50,'attack_type': 'claw',  'attack_sound':'./audio/attack/claw.wav','speed': 2.5, 'resistance': 100, 'attack_radius': 120, 'notice_radius': 200},
	'spirit': {'health': 200,'exp':250,'damage':30,'attack_type': 'flame', 'attack_sound':'./audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 100,'exp':100,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 1, 'attack_radius': 50, 'notice_radius': 300},
	'dragon': {'health': 400,'exp':400,'damage':30,'attack_type': 'slash', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 100, 'notice_radius': 400},
	'dragon2': {'health': 1000,'exp':1000,'damage':50,'attack_type': 'slash', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 100, 'notice_radius': 400},
	'beast': {'health': 2000,'exp':1500,'damage':80,'attack_type': 'claw', 'attack_sound':'./audio/attack/claw.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 100, 'notice_radius': 400},
	'GiantFlame': {'health': 6000,'exp':25000,'damage':120,'attack_type': 'claw', 'attack_sound':'./audio/attack/slash.wav', 'speed': 2.5, 'resistance': 5, 'attack_radius': 120, 'notice_radius': 400},
	'Reptile': {'health': 12000, 'exp': 50000, 'damage': 120, 'attack_type': 'claw','attack_sound': './audio/attack/slash.wav', 'speed': 2.5, 'resistance': 5, 'attack_radius': 120,'notice_radius': 400},
	'GiantFlame2': {'health': 10000, 'exp': 50000, 'damage': 80, 'attack_type': 'claw','attack_sound': './audio/attack/slash.wav', 'speed': 2.5, 'resistance': 5, 'attack_radius': 120,'notice_radius': 400},
	'Akshar': {'health': 30000, 'exp': 100000, 'damage': 200, 'attack_type': 'claw','attack_sound': './audio/attack/claw.wav', 'speed': 2.5, 'resistance': 5, 'attack_radius': 120,'notice_radius': 800},
	'Yatagarasu': {'health': 100000, 'exp': 10000000, 'damage': 400, 'attack_type': 'slash','attack_sound': './audio/attack/slash.wav', 'speed': 4.5, 'resistance': 5, 'attack_radius': 120,'notice_radius': 1000},
	'NPC1': {'health': 1000000, 'exp': 1000000, 'damage': 0, 'attack_type': 'claw','attack_sound': './audio/attack/claw.wav', 'speed': 0, 'resistance': 5, 'attack_radius': 0,'notice_radius': 200},
	'NPC2': {'health': 1000000, 'exp': 1000000, 'damage': 0, 'attack_type': 'claw','attack_sound': './audio/attack/claw.wav', 'speed': 0, 'resistance': 5, 'attack_radius': 0,'notice_radius': 200},
	'NPC3': {'health': 1000000, 'exp': 1000000, 'damage': 0, 'attack_type': 'claw','attack_sound': './audio/attack/claw.wav', 'speed': 0, 'resistance': 5, 'attack_radius': 0,'notice_radius': 200},
	'NPC4': {'health': 1000000, 'exp': 1000000, 'damage': 0, 'attack_type': 'claw','attack_sound': './audio/attack/claw.wav', 'speed': 0, 'resistance': 5, 'attack_radius': 0,'notice_radius': 200},
	'NPC5': {'health': 1000000, 'exp': 1000000, 'damage': 0, 'attack_type': 'claw','attack_sound': './audio/attack/claw.wav', 'speed': 0, 'resistance': 5, 'attack_radius': 0,'notice_radius': 200},
	'NPC6': {'health': 1000000, 'exp': 1000000, 'damage': 0, 'attack_type': 'claw','attack_sound': './audio/attack/claw.wav', 'speed': 0, 'resistance': 5, 'attack_radius': 0,'notice_radius': 200},
}