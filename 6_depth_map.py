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

import cv2
from matplotlib import pyplot as plt
import numpy as np
import json
from stereovision.calibration import StereoCalibrator
from stereovision.calibration import StereoCalibration

# Global variables preset
imageToDisp = './scenes/photo.png'
photo_Width = 1280
photo_Height = 720
params_file = './src/pf_'+str(photo_Width)+'_'+str(photo_Height)+'.txt'

# Read parameters for image split
print ('Loading split parameters...')
f=open(params_file, 'r')
data = json.load(f)
imageWidth = data['imageWidth']
jointWidth = data['jointWidth']
leftIndent = data['leftIndent']
rightIndent = data['rightIndent']
f.close()
image_size = (imageWidth,photo_Height)


print('Reading image rof depth map...')
pair_img = cv2.imread(imageToDisp,0)
imgLeft = pair_img [0:photo_Height,leftIndent:imageWidth] #Y+H and X+W
imgRight = pair_img [0:photo_Height,rightIndent:rightIndent+imageWidth]


def plot(title, img, i):
    plt.subplot(2, 2, i)
    plt.title(title)
    plt.imshow(img, 'gray')
    plt.gca().get_xaxis().set_visible(False)
    plt.gca().get_yaxis().set_visible(False)


# Implementing calibration data
print('Load calibration data...')
calibration = StereoCalibration(input_folder='ress')
rectified_pair = calibration.rectify((imgLeft, imgRight))


# Depth map function
print('Building depth map...')
def stereo_depth_map(rectified_pair, ndisp, sws):
    stereo = cv2.StereoBM(cv2.STEREO_BM_BASIC_PRESET, \
                          ndisparities=ndisp, SADWindowSize=sws)
    return stereo.compute(rectified_pair[0], rectified_pair[1])


disparity = stereo_depth_map(rectified_pair, 80, 7)
print('Done! Let\'s look at depth map')


norm_coeff = 255 / disparity.max()-disparity.min()
plot(u'Left calibrated', rectified_pair[0], 1)
plot(u'Right calibrated', rectified_pair[1], 2)
plot(u'Depth map', disparity/255., 3)
plt.show()