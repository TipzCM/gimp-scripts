#!/usr/bin/python
#!python3

import os
from gimpfu import *


def doExport(ratio, image, interpolation):
	filename = os.path.splitext(image.filename)[0]
	#pdb.gimp_message("%s" % filename)
		
	width = image.width
	height = image.height
		
	new_image = pdb.gimp_image_duplicate(image)
	layer = pdb.gimp_image_merge_visible_layers(new_image, CLIP_TO_IMAGE)
		
	#resize
	#layer.scale(int(width*ratio), int(height*ratio), 0)
	pdb.gimp_layer_scale_full(layer, int(width*ratio), int(height*ratio), True, interpolation)

	pdb.gimp_file_save(new_image, layer, filename + ".jpg", filename + ".jpg")
	#pbd.gimp_image_scale_full(new_image, )
	pdb.gimp_image_delete(new_image)

def pngify(timg, tdrawable, ratio = 1, interpolation = 1, export_all = True):
	if export_all:
		images = gimp.image_list()
		for image in images:
			#only save already saved files - ie, defined files
			if image.filename:
				doExport(ratio, image, interpolation)
	else:
		doExport(ratio, timg, interpolation)
	
	
register(
		"python_fu_jpgify",
		"Saves all open images as JPG with specified image ratio",
		"Saves all open images as JPG with specified image ratio",
		"Leif Stawnyczy",
		"Leif Stawnyczy",
		"2019",
		"<Image>/Image/AutoArt/JPG-ify",
		"RGB*, GRAY*",
		[
			(PF_FLOAT, "ratio", "Scale image", 1),
			(PF_INT, "interpolation", "Scale interpolation (0 = none, 1 = linear, 2 = cubic, 3 = nohalo, 4, lohalo)", 1),
			(PF_BOOL, "export_all", "Export all pages? (No will export just this page)", True)
		],
		[],
		pngify)

main()