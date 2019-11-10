#!/usr/bin/python
#!python3

import os
from gimpfu import *

def quick_colour(timg, tdrawable, color_layer = None, selection_overlap = 3):
    exists, orig_x, orig_y, width, height = pdb.gimp_selection_bounds(timg)

    if exists == 0:
        pdb.gimp_message("Please make a selection")
        return #do nothing

    if color_layer is None:
        pdb.gimp_message("Please provide the layer to color.")
        return #do nothing

    timg.undo_group_start()

    currentSampleTransparentSetting = pdb.gimp_context_get_sample_transparent()
    pdb.gimp_context_set_sample_transparent(1) #allow selecting transparencies

    #grow the selection (so that there's no ugly white spaces)
    pdb.gimp_selection_grow(timg, selection_overlap)

    selection = pdb.gimp_image_get_selection(timg)

    #Colour it!
    #drawable, fill_mode, paint_mode, opacity, threshold (not valid when selection is present),
    #    sample_merged (false to use drawable),
    # x (not valid when selection is present), y (not valid when selection is present)
    pdb.gimp_edit_bucket_fill(color_layer, FG_BUCKET_FILL, NORMAL_MODE, 100, 0, False, 0, 0)

    #set sample transparent back
    pdb.gimp_context_set_sample_transparent(currentSampleTransparentSetting)

    timg.undo_group_end()
    
    #unselect everything
    pdb.gimp_selection_none(timg)    

	
register(
		"python_fu_quick_colour",
		"Colourizes all selected areas with the selected foreground colour.",
		"Colourizes all selected areas with the selected foreground colour.",
		"Leif Stawnyczy",
		"Leif Stawnyczy",
		"2017",
		"<Image>/Image/AutoArt/Quick_Colour",
		"RGB*, GRAY*",
		[
			(PF_LAYER, "color_layer", "Layer to colour", None),
            (PF_INT, "selection_overlap", "Enlarge selection (pixles)? A slightly larger selection reduces white space.", 1)
		],
		[],
		quick_colour)

main()