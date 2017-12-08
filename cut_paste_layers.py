#!/usr/bin/python
#!python3

import os
from gimpfu import *


def doExport(ratio, image):
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


def cut_paste_all_layers(timg, tdrawable, x_translate = 0, y_translate = 0):
	#assume rectangles for now for simplicity
	exists, orig_x, orig_y, width, height = pdb.gimp_selection_bounds(timg)

	if exists is 0:
		pdb.gimp_message("Please make a selection on the top layer.")
		return #do nothing

	if exists is not 0:
		timg.undo_group_start()

		for layer in timg.layers:
			#cut
			pdb.gimp_edit_cut(layer)

			#paste
			flayer = pdb.gimp_edit_paste(layer, True)
			pdb.gimp_selection_none(timg)

			#translate relative to original bounds position
			pdb.gimp_layer_translate(flayer, x_translate, y_translate)

			#anchor
			pdb.gimp_floating_sel_anchor(flayer)
			
			#do selection again
			pdb.gimp_image_select_rectangle(timg, CHANNEL_OP_REPLACE, orig_x, orig_y, width - orig_x, height- orig_y)

		timg.undo_group_end()

		#undo all selections
		pdb.gimp_selection_none(timg)
	
register(
		"python_fu_cut_paste_all_layers",
		"Cuts and pastes the selection from all layers with provided translation.",
		"Cuts and pastes the selection from all layers with provided translation.",
		"Leif Stawnyczy",
		"Leif Stawnyczy",
		"2017",
		"<Image>/Image/AutoArt/Cut N Paste All Layers",
		"RGB*, GRAY*",
		[
			(PF_INT, "translate_x", "How far to move selection in X direction", 0),
			(PF_INT, "translate_y", "How far to move selection in the Y direction (negative moves up)", 0)
		],
		[],
		cut_paste_all_layers)

main()