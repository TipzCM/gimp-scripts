#!/usr/bin/python
#!python3

import os
from gimpfu import *


def get_top_layer_index(timg, onlyVisible):
	active_layer = timg.active_layer

	active_layer_found = False

	for index in range(len(timg.layers)):
		layer = timg.layers[index]

		if active_layer.ID == layer.ID:
			active_layer_found = True

		#we skip text layers
		if active_layer_found and (not pdb.gimp_drawable_is_text_layer(layer)):
			if (onlyVisible and layer.visible) or not onlyVisible:
				return index

	return -1

def cut_paste_all_layers(timg, tdrawable, x_translate = 0, y_translate = 0, onlyVisible = True):
	#assume rectangles for now for simplicity
	exists, orig_x, orig_y, width, height = pdb.gimp_selection_bounds(timg)

	if exists is 0:
		pdb.gimp_message("Please make a selection on the active layer.")
		return #do nothing

	#find top_index (ie, index of the top-most layer, starting from the active layer,
	# that is not a text layer and is visible if onlyVisible)
	top_index = get_top_layer_index(timg, onlyVisible)
	if top_index < 0:
		#no top_index found
		if onlyVisible:
			pdb.gimp_message("There are no visible non-text layers. Nothing will be done.")
		else:
			pdb.gimp_message("There are no non-text layers. Nothing will be done.")
		return # do nothing

	if exists is not 0 and top_index >= 0:
		timg.undo_group_start()

		for i in range(top_index, len(timg.layers)):
			layer = timg.layers[i]

			if (pdb.gimp_drawable_is_text_layer(layer)) or (onlyVisible and not layer.visible):
				#skip text layers or invisible layers (when onlyVisible is selected)
				continue

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
		"Cuts and pastes the selection from all (image sized) layers, from active layer down, with provided translation.",
		"Cuts and pastes the selection from all (image sized) layers, from active layer down, with provided translation.",
		"Leif Stawnyczy",
		"Leif Stawnyczy",
		"2017",
		"<Image>/Image/AutoArt/Cut N Paste All Layers",
		"RGB*, GRAY*",
		[
			(PF_INT, "translate_x", "How far to move selection in X direction", 0),
			(PF_INT, "translate_y", "How far to move selection in the Y direction (negative moves up)", 0),
			(PF_BOOL, "onlyVisible", "Only alter visible layers?", True)
		],
		[],
		cut_paste_all_layers)

main()