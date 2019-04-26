#!/usr/bin/python
#!python3

import os
from gimpfu import *

def add_layer_to_image(the_image, name, opacity, width, height):
	layer = gimp.Layer(the_image, name, width, height, RGBA_IMAGE, opacity, NORMAL_MODE)
	the_image.add_layer(layer, 0)
	return layer

def sprite_eaze(timg, tdrawable):
	width = tdrawable.width
	height = tdrawable.height

	timg.undo_group_start()
	
	add_layer_to_image(timg, "colours", 100, width, height)
	add_layer_to_image(timg, "lineart", 100, width, height)
	add_layer_to_image(timg, "dark-shading", 60, width, height)
	add_layer_to_image(timg, "light-shading", 40, width, height)

	timg.undo_group_end()
	
register(
		"python_fu_sprite_eaze",
		"Adds layers for creating a sprite.",
		"Adds layers for creating a sprite.",
		"Leif Stawnyczy",
		"Leif Stawnyczy",
		"2019",
		"<Image>/Image/AutoSprite/Sprite-eaze",
		"RGB*, GRAY*",
		[],
		[],
		sprite_eaze)

main()