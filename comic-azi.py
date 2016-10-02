#!/usr/bin/python
#!python3

import os
from gimpfu import *

def add_layer_to_image(the_image, name, is_visible, width, height):
	layer = gimp.Layer(the_image, name, width, height, RGBA_IMAGE, 100, NORMAL_MODE)
	the_image.add_layer(layer, 0)
	pdb.gimp_item_set_visible(layer, is_visible)
	return layer;

def comic_aze(timg, tdrawable, bg_name = "bg", bg_color = "#FFFFFF", bg_visible = True, lineart_name = "lineart", panels_name = "panels", panels_color = "#000000", text_layer_name = "text", has_additional_layers = True, additional_layers = "whites,colours,pupils,skin,clothes1,clothes2,hair,details"):
	width = tdrawable.width
	height = tdrawable.height
	
	#pdb.gimp_message("%s" % timg.filename)
	#pdb.gimp_message("%s" % os.path.basename(timg.filename))
	
	#open_images, image_ids = pdb.gimp_image_list()
	#pdb.gimp_message("%d %s" % (open_images, image_ids))
	
	#get these for later
	initForeground = gimp.get_foreground()
	initBackground = gimp.get_background()
	
	#create bg layer, fill and add to image
	#Layer(image, name, width, height, type, opacity, mode)
	#We're keeping this RGB instead of RGBA so users can erase directly on it and not get transparencies
	bg_layer = gimp.Layer(timg, bg_name, width, height, RGB_IMAGE, 100, NORMAL_MODE)
	gimp.set_background(bg_color)
	bg_layer.fill(BACKGROUND_FILL)
	timg.add_layer(bg_layer, 0)
	
	pdb.gimp_item_set_visible(bg_layer, bg_visible)
	
	#add additional layers
	if has_additional_layers and additional_layers.strip():
		layers = additional_layers.strip().split(",")
		for layer in layers:
			add_layer_to_image(timg, layer, True, width, height)
		
	
	#create and add lineart layer
	add_layer_to_image(timg, lineart_name, True, width, height)
	
	#create panels section and set visible
	panels_layer = add_layer_to_image(timg, panels_name, False, width, height)
	gimp.set_background(panels_color)
	panels_layer.fill(BACKGROUND_FILL)
	
	#add final layer - text layer
	if text_layer_name:
		text_layer = add_layer_to_image(timg, text_layer_name, True, width, height) 
	
	#reset bg and fg
	gimp.set_foreground(initForeground)
	gimp.set_background(initBackground)
	
	#save the file
	filename = os.path.splitext(timg.filename)[0]
	pdb.gimp_file_save(timg, tdrawable, filename + ".xcf", filename + ".xcf")
	
register(
		"python_fu_comic_aze",
		"Adds layers for comic-izing a page. Optionally adds layers for colouring",
		"Adds layers for comic-izing a page. Optionally adds layers for colouring",
		"Leif Stawnyczy",
		"Leif Stawnyczy",
		"2016",
		"<Image>/Image/Comic-aze",
		"RGB*, GRAY*",
		[
			(PF_STRING, "bg_name", "Background layer name", "bg"),
			(PF_COLOR, "bg_color", "Background layer color", "#FFFFFF"),
			(PF_BOOL, "bg_visible", "Make background visible", True),
			(PF_STRING, "lineart_name", "Lineart layer name", "lineart"),
			(PF_STRING, "panels_name", "Panels layer name", "panels"),
			(PF_COLOR, "panels_color", "Panels layer color", "#000000"),
			(PF_STRING, "text_layer_name", "Text layer name", "text"),
			(PF_BOOL, "has_additional_layers", "Has Additional Layers", False),
			(PF_STRING, "additional_layers", "Additional layers (comma separated). \n Layers will be added between background layer and lineart layer", "whites,colours,pupils,skin,clothes1,clothes2,hair,details")
		],
		[],
		comic_aze)

main()