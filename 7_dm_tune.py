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
import cv2.cv as cv
from picamera.array import PiRGBArray
from picamera import PiCamera
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np
import json
import time
from stereovision.calibration import StereoCalibrator
from stereovision.calibration import StereoCalibration

# Global variables preset
imageToDisp = './scenes/photo.png'
#imageToDisp = ""
photo_Width = 1280
photo_Height = 720
params_file = './src/pf_1280_720.txt'


if (imageToDisp == ''):
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution=(photo_Width,photo_Height)
    rawCapture = PiRGBArray(camera)

    # allow the camera to warmup
    time.sleep(0.1)

    # grab an image from the camera
    camera.hflip = True
    camera.capture(rawCapture, format="bgr")
    imGR = cv2.cvtColor (rawCapture.array, cv2.COLOR_BGR2GRAY)
    pair_img = imGR
else:
    pair_img = cv2.imread(imageToDisp,0)
    if (pair_img is None):
        print ('Can not read image from file \"'+imageToDisp+'\"')
        exit(0)

# If flag set to 1 than a lot of "bad" job will be avoided (rebuild DM and picture redraw)
loading_settings = 0

# Read parameters for image split
print('Reading split parameters...')
f=open(params_file, 'r')
data = json.load(f)
imageWidth = data['imageWidth']
jointWidth = data['jointWidth']
leftIndent = data['leftIndent']
rightIndent = data['rightIndent']
f.close()
image_size = (imageWidth,photo_Height)

# Read image and split it in a stereo pair
print('Read and split image...')
imgLeft = pair_img [0:photo_Height,leftIndent:imageWidth] #Y+H and X+W
imgRight = pair_img [0:photo_Height,rightIndent:rightIndent+imageWidth] #Y+H and X+W


# Implementing calibration data
print('Read calibration data and rectifying stereo pair...')
calibration = StereoCalibration(input_folder='ress')
rectified_pair = calibration.rectify((imgLeft, imgRight))


# Depth map function
SWS = 5
PFS = 5
PFC = 29
MDS = -25
NOD = 128
TTH = 100
UR = 10
SR = 15
SPWS = 100

def stereo_depth_map(rectified_pair):
    print ('SWS='+str(SWS)+' PFS='+str(PFS)+' PFC='+str(PFC)+' MDS='+\
           str(MDS)+' NOD='+str(NOD)+' TTH='+str(TTH))
    print (' UR='+str(UR)+' SR='+str(SR)+' SPWS='+str(SPWS))
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
    disparity_visual = cv.CreateMat(c, r, cv.CV_8U)
    cv.Normalize(disparity, disparity_visual, 0, 255, cv.CV_MINMAX)
    disparity_visual = np.array(disparity_visual)
    return disparity_visual

disparity = stereo_depth_map(rectified_pair)

# Set up and draw interface
# Draw left image and depth map
axcolor = 'lightgoldenrodyellow'
fig = plt.subplots(1,2)
plt.subplots_adjust(left=0.15, bottom=0.5)
plt.subplot(1,2,1)
dmObject = plt.imshow(rectified_pair[0], 'gray')

saveax = plt.axes([0.3, 0.38, 0.15, 0.04]) #stepX stepY width height
buttons = Button(saveax, 'Save settings', color=axcolor, hovercolor='0.975')


def save_map_settings( event ):
    buttons.label.set_text ("Saving...")
    print('Saving to file...') 
    result = json.dumps({'SADWindowSize':SWS, 'preFilterSize':PFS, 'preFilterCap':PFC, \
             'minDisparity':MDS, 'numberOfDisparities':NOD, 'textureThreshold':TTH, \
             'uniquenessRatio':UR, 'speckleRange':SR, 'speckleWindowSize':SPWS},\
             sort_keys=True, indent=4, separators=(',',':'))
    fName = '3dmap_set.txt'
    f = open (str(fName), 'w') 
    f.write(result)
    f.close()
    buttons.label.set_text ("Save to file")
    print ('Settings saved to file '+fName)

buttons.on_clicked(save_map_settings)


loadax = plt.axes([0.5, 0.38, 0.15, 0.04]) #stepX stepY width height
buttonl = Button(loadax, 'Load settings', color=axcolor, hovercolor='0.975')
def load_map_settings( event ):
    global SWS, PFS, PFC, MDS, NOD, TTH, UR, SR, SPWS, loading_settings
    loading_settings = 1
    fName = '3dmap_set.txt'
    print('Loading parameters from file...')
    buttonl.label.set_text ("Loading...")
    f=open(fName, 'r')
    data = json.load(f)
    sSWS.set_val(data['SADWindowSize'])
    sPFS.set_val(data['preFilterSize'])
    sPFC.set_val(data['preFilterCap'])
    sMDS.set_val(data['minDisparity'])
    sNOD.set_val(data['numberOfDisparities'])
    sTTH.set_val(data['textureThreshold'])
    sUR.set_val(data['uniquenessRatio'])
    sSR.set_val(data['speckleRange'])
    sSPWS.set_val(data['speckleWindowSize'])    
    f.close()
    buttonl.label.set_text ("Load settings")
    print ('Parameters loaded from file '+fName)
    print ('Redrawing depth map with loaded parameters...')
    loading_settings = 0
    update(0)
    print ('Done!')

buttonl.on_clicked(load_map_settings)


plt.subplot(1,2,2)
dmObject = plt.imshow(disparity, aspect='equal')

# Draw interface for adjusting parameters
print('Start interface creation (it takes up to 30 seconds)...')

SWSaxe = plt.axes([0.15, 0.01, 0.7, 0.025], axisbg=axcolor) #stepX stepY width height 
PFSaxe = plt.axes([0.15, 0.05, 0.7, 0.025], axisbg=axcolor) #stepX stepY width height 
PFCaxe = plt.axes([0.15, 0.09, 0.7, 0.025], axisbg=axcolor) #stepX stepY width height 
MDSaxe = plt.axes([0.15, 0.13, 0.7, 0.025], axisbg=axcolor) #stepX stepY width height 
NODaxe = plt.axes([0.15, 0.17, 0.7, 0.025], axisbg=axcolor) #stepX stepY width height 
TTHaxe = plt.axes([0.15, 0.21, 0.7, 0.025], axisbg=axcolor) #stepX stepY width height 
URaxe = plt.axes([0.15, 0.25, 0.7, 0.025], axisbg=axcolor) #stepX stepY width height
SRaxe = plt.axes([0.15, 0.29, 0.7, 0.025], axisbg=axcolor) #stepX stepY width height
SPWSaxe = plt.axes([0.15, 0.33, 0.7, 0.025], axisbg=axcolor) #stepX stepY width height

sSWS = Slider(SWSaxe, 'SWS', 5.0, 255.0, valinit=5)
sPFS = Slider(PFSaxe, 'PFS', 5.0, 255.0, valinit=5)
sPFC = Slider(PFCaxe, 'PreFiltCap', 5.0, 63.0, valinit=29)
sMDS = Slider(MDSaxe, 'MinDISP', -100.0, 100.0, valinit=-25)
sNOD = Slider(NODaxe, 'NumOfDisp', 16.0, 256.0, valinit=128)
sTTH = Slider(TTHaxe, 'TxtrThrshld', 0.0, 1000.0, valinit=100)
sUR = Slider(URaxe, 'UnicRatio', 1.0, 20.0, valinit=10)
sSR = Slider(SRaxe, 'SpcklRng', 0.0, 40.0, valinit=15)
sSPWS = Slider(SPWSaxe, 'SpklWinSze', 0.0, 300.0, valinit=100)


# Update depth map parameters and redraw
def update(val):
    global SWS, PFS, PFC, MDS, NOD, TTH, UR, SR, SPWS
    SWS = int(sSWS.val/2)*2+1 #convert to ODD
    PFS = int(sPFS.val/2)*2+1
    PFC = int(sPFC.val/2)*2+1    
    MDS = int(sMDS.val)    
    NOD = int(sNOD.val/16)*16  
    TTH = int(sTTH.val)
    UR = int(sUR.val)
    SR = int(sSR.val)
    SPWS= int(sSPWS.val)
    if ( loading_settings==0 ):
        print ('Rebuilding depth map')
        disparity = stereo_depth_map(rectified_pair)
        dmObject.set_data(disparity)
        print ('Redraw depth map')
        plt.draw()


# Connect update actions to control elements
sSWS.on_changed(update)
sPFS.on_changed(update)
sPFC.on_changed(update)
sMDS.on_changed(update)
sNOD.on_changed(update)
sTTH.on_changed(update)
sUR.on_changed(update)
sSR.on_changed(update)
sSPWS.on_changed(update)

print('Show interface to user')
plt.show()



