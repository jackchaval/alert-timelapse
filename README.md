Time-lapse creator for Logitech Alert Cameras
=============================================

This project can be used to generate time-lapse videos using Logitech Alert security cameras as the image source.

Before running anything, you'll need to edit config.json to fill in the appropriate values for authentication, identifying your camera, etc.

There are two main scripts:

* snapshot.py - Run this to capture periodic snapshots that will be the individual frames of the time-lapse video. It depends on the [requests](https://pypi.python.org/pypi/requests) package.
* video.py - Run this to generate a video from the previously captured snapshots. It depends on having [ffmpeg](https://www.ffmpeg.org/download.html) installed.

To Do
-----

* Lots of polish needed
* In particular, the video.py script is not fully generic yet. You'd need to edit it a bit (the input folder name and output filename) to have it work.
* requirements.txt
