# Copyright (C) 2015 Eugene Pomazov, <3dberry.org>
#
# This file is part of 3Dberry tutorial scripts.
#
# 3Dberry tutorial is free software: you can redistribute it 
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the 
# License, or (at your option) any later version.
#
# 3Dberry tutorial is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with 3Dberry tutorial.  
# If not, see <http://www.gnu.org/licenses/>.


from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np


# Global variables preset
photo_width = 1280
photo_height = 720
a = np.zeros((photo_height, photo_width, 3), dtype=np.uint8)
a[:, 640, :] = 0xff
filename = './scenes/photo.png'


# Create window to be able capture key press events
cv2.namedWindow("Image")


# Initialize the camera and start preview
camera = PiCamera()
camera.resolution=(photo_width, photo_height)
camera.hflip = True
camera.start_preview()
camera.preview.fullscreen = True


# Adding ovrlay with center line for camera adjust
o = camera.add_overlay(np.getbuffer(a), layer=3, alpha=64)
cv2.waitKey(0)


# Key pressed - remove overlay, stop preview
camera.remove_overlay(o)
camera.stop_preview()


# Grab an image from the camera
rawCapture = PiRGBArray(camera)
camera.capture(rawCapture, format="bgr", use_video_port=True)
image = rawCapture.array


# Display image and wait for a keypress
cv2.imshow("Image", image)
cv2.waitKey(0)


# Write image to file
cv2.imwrite(filename, image)