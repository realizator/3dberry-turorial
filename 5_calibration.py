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
import cv2
import numpy as np
import json
from stereovision.calibration import StereoCalibrator
from stereovision.calibration import StereoCalibration


# Global variables preset
total_photos = 15
photo_Width = 1280
photo_Height = 720
params_file = './src/pf_'+str(photo_Width)+'_'+str(photo_Height)+'.txt'
# Chessboard parameters
rows = 6
columns = 9
square_size = 2.5


# Read pair cut parameters
f=open(params_file, 'r')
data = json.load(f)
imageWidth = data['imageWidth']
jointWidth = data['jointWidth']
leftIndent = data['leftIndent']
rightIndent = data['rightIndent']
f.close()
image_size = (imageWidth,photo_Height)


calibrator = StereoCalibrator(rows, columns, square_size, image_size)
photo_counter = 0
print ('Start cycle')

while photo_counter != total_photos:
  photo_counter = photo_counter + 1
  print ('Import pair No ' + str(photo_counter))
  leftName = './pairs/left_'+str(photo_counter).zfill(2)+'.png'
  rightName = './pairs/right_'+str(photo_counter).zfill(2)+'.png'
  if os.path.isfile(leftName) and os.path.isfile(rightName):
      imgLeft = cv2.imread(leftName,1)
      imgRight = cv2.imread(rightName,1)
      calibrator.add_corners((imgLeft, imgRight), True)
print ('End cycle')


print ('Starting calibration... It can take several minutes!')
calibration = calibrator.calibrate_cameras()
calibration.export('ress')
print ('Calibration complete!')


# Lets rectify and show last pair after  calibration
calibration = StereoCalibration(input_folder='ress')
rectified_pair = calibration.rectify((imgLeft, imgRight))

cv2.imshow('Left CALIBRATED', rectified_pair[0])
cv2.imshow('Right CALIBRATED', rectified_pair[1])
cv2.imwrite("rectifyed_left.jpg",rectified_pair[0])
cv2.imwrite("rectifyed_right.jpg",rectified_pair[1])
cv2.waitKey(0)