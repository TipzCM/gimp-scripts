#!/usr/bin/python
#!python3

import os
from gimpfu import *

def sprite_ify(timg, tdrawable, starts_with = ""):
    # gimp.image_list() returns list in console
    # but we'll use timg
    has_skippable = (starts_with != "")
    for index in range(len(timg.layers)):
        layer = timg.layers[index]

        if (pdb.gimp_drawable_is_text_layer(layer) != 0):
            continue
        
        if (has_skippable and (layer.name.startswith(starts_with))):
            continue

        pdb.gimp_file_save(timg, layer, layer.name + ".png", layer.name + ".png")

register(
    "python_fu_sprite_ify",
    "Exports each layer as a png image.",
    "Exports each layer as a png image.",
    "Leif Stawnyczy",
    "Leif Stawnyczy",
    "2019",
    "<Image>/Image/AutoSprite/Sprite-ify",
    "RGB*, GRAY*",
    [
        (PF_STRING, "starts_with", "Skip layers that start with: (if blank, no layers are skipped)", "")
    ],
    [],
    sprite_ify)

main()