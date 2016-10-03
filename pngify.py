#!/usr/bin/python
#!python3

import os
from gimpfu import *


def pngify(timg, tdrawable, ratio = 1):
	images = gimp.image_list()
	for image in images:
		#only save already saved files - ie, defined files
		if image.filename:
			filename = os.path.splitext(image.filename)[0]
			#pdb.gimp_message("%s" % filename)
			
			width = image.width
			height = image.height
			
			new_image = pdb.gimp_image_duplicate(image)
			layer = pdb.gimp_image_merge_visible_layers(new_image, CLIP_TO_IMAGE)
			
			#resize
			layer.scale(int(width*ratio), int(height*ratio), 0)
			
			pdb.gimp_file_save(new_image, layer, filename + ".png", filename + ".png")
			pdb.gimp_image_delete(new_image)
		
	
	
register(
		"python_fu_pngify",
		"Saves all open images as PNG with specified image ratio",
		"Saves a;; open images as PNG with specified image ratio",
		"Leif Stawnyczy",
		"Leif Stawnyczy",
		"2016",
		"<Image>/Image/AutoArt/PNG-ify",
		"RGB*, GRAY*",
		[
			(PF_FLOAT, "ratio", "Scale image", 1)
		],
		[],
		pngify)

main()