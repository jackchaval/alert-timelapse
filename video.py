# -*- coding: utf-8 -*-
# Copyright (c) 2014 Eric Smith

# ffmpeg -f image2 -i foo-%04d.jpeg -r 12 -s WxH foo.avi
# -f input file format
# -i input files with 4 zero-padded digits
# -r framerate
# -s frame size (wxh means use the input size)
# output filename