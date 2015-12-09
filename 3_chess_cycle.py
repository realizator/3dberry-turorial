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

import os
import time
import picamera
import cv2
 
# Global variables preset
countdown = 5         # Interval for count-down timer, seconds
photo_counter  = 0    # Photo counter
photo_width = 1280
photo_height = 720
total_photos = 15

wn = cv2.namedWindow('preview', cv2.WINDOW_NORMAL)


# Lets start taking photos! 
print "Starting photo sequence"
with picamera.PiCamera() as camera:
    camera.resolution = (photo_width, photo_height)
    camera.start_preview()
    camera.preview.fullscreen = False
    camera.preview.window = (0,0,photo_width/2,photo_height/2)
    camera.annotate_text_size = 160
    camera.annotate_background = picamera.Color('red')
    camera.hflip = True
    while photo_counter != total_photos:
      photo_counter = photo_counter + 1
      filename = 'scene_'+str(photo_width)+'x'+str(photo_height)+'_'+\
                  str(photo_counter) + '.png'
      cntr = countdown
      while cntr >0:
        camera.annotate_text = str(cntr)
        cntr-=1
        time.sleep(1)
      camera.annotate_text = ''
      camera.capture (filename, use_video_port=True)
      print ' ['+str(photo_counter)+' of '+str(total_photos)+'] '+filename
 
print "Finished photo sequence"
 
