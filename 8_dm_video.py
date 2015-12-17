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
import cv2.cv as cv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button
import json
from stereovision.calibration import StereoCalibrator
from stereovision.calibration import StereoCalibration
from datetime import datetime


# Preset parameters
photo_Width = 1280
photo_Height = 720
params_file = './src/pf_'+str(photo_Width)+'_'+str(photo_Height)+'.txt'


# Depth map default preset
SWS = 5
PFS = 5
PFC = 29
MDS = -25
NOD = 128
TTH = 100
UR = 10
SR = 15
SPWS = 100


# Read parameters for image split
print('Reading split parameters...')
f=open(params_file, 'r')
data = json.load(f)
imageWidth = data['imageWidth']
jointWidth = data['jointWidth']
leftIndent = data['leftIndent']
rightIndent = data['rightIndent']
f.close()

# Overlay preset
# Overlay buffer size must be dividable by 16
if (int(photo_Height/16)*16<photo_Height):
    buf_height = (int(photo_Height/16)+1)*16
else:
    buf_height = photo_Height

if (int(photo_Width/16)*16<photo_Width):
    buf_width = (int(photo_Width/16)+1)*16
else:
    buf_width = photo_Width
a = np.zeros((buf_height, buf_width, 3), dtype=np.uint8)


# Create window to be able capture key press events
cv2.namedWindow("Image")
cv2.namedWindow("Disparity")

# Implementing calibration data
print('Read calibration data and rectifying stereo pair...')
calibration = StereoCalibration(input_folder='ress')

# Initialize the camera and start preview
camera = PiCamera()
camera.resolution=(photo_Width, photo_Height)
camera.start_preview()
camera.preview.alpfa = 128
camera.hflip = True
camera.preview.fullscreen = True
#camera.preview.window = (0,0,photo_Width/2,photo_Height/2)
rawCapture = PiRGBArray(camera)


def stereo_depth_map(rectified_pair):
    c, r = rectified_pair[0].shape
    disparity = cv.CreateMat(c, r, cv.CV_32F)
    sbm = cv.CreateStereoBMState()
    sbm.SADWindowSize = SWS
    sbm.preFilterType = 1
    sbm.preFilterSize = PFS
    sbm.preFilterCap = PFC
    sbm.minDisparity = MDS
    sbm.numberOfDisparities = NOD
    sbm.textureThreshold = TTH
    sbm.uniquenessRatio= UR
    sbm.speckleRange = SR
    sbm.speckleWindowSize = SPWS
    dmLeft = cv.fromarray (rectified_pair[0])
    dmRight = cv.fromarray (rectified_pair[1])
    cv.FindStereoCorrespondenceBM(dmLeft, dmRight, disparity, sbm)
    disparity_grayscale = cv.CreateMat(c, r, cv.CV_8UC1)
    cv.Normalize(disparity, disparity_grayscale, 0, 255, cv2.NORM_MINMAX)

    disparity_grayscale = np.array(disparity_grayscale, dtype=np.uint8) #without UINT8 returns grayscale
    disparity_color = cv2.applyColorMap(disparity_grayscale, cv2.COLORMAP_JET)
    return disparity_color

def load_map_settings( fName ):
    global SWS, PFS, PFC, MDS, NOD, TTH, UR, SR, SPWS, loading_settings
    print('Loading parameters from file...')
    f=open(fName, 'r')
    data = json.load(f)
    SWS=data['SADWindowSize']
    PFS=data['preFilterSize']
    PFC=data['preFilterCap']
    MDS=data['minDisparity']
    NOD=data['numberOfDisparities']
    TTH=data['textureThreshold']
    UR=data['uniquenessRatio']
    SR=data['speckleRange']
    SPWS=data['speckleWindowSize']    
    f.close()
    print ('Parameters loaded from file '+fName)


load_map_settings ("3dmap_set.txt")

o = camera.add_overlay(np.getbuffer(a), layer=3, alpha = 160)
a[0:photo_Height,imageWidth:photo_Width,:] = 0
counter = 0
while (counter <100):
    t1 = datetime.now()
    counter+=1
    print ('Counter: '+str(counter))
    rawCapture.truncate(0)
    camera.capture(rawCapture, format="bgr", use_video_port=True)
    image = rawCapture.array
    pair_img = cv2.cvtColor (image, cv2.COLOR_BGR2GRAY)
    imgLeft = pair_img [0:photo_Height,leftIndent:imageWidth] #Y+H and X+W
    imgRight = pair_img [0:photo_Height,rightIndent:rightIndent+imageWidth] #Y+H and X+W
    rectified_pair = calibration.rectify((imgLeft, imgRight))
    disparity = stereo_depth_map(rectified_pair)
    disparity = cv2.cvtColor (disparity, cv2.COLOR_BGR2RGB)
    a[0:photo_Height,0:imageWidth,:] = disparity
    o.update(a)
    t2 = datetime.now()
    print (t2-t1)

camera.remove_overlay(o)
camera.stop_preview()