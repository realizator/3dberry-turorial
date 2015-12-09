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


import time
import cv2
import copy
import json


# Global variables preset
showHelp = 1
pwidth=1280
pheight=720
loadImagePath = ""
# loadImagePath = "./src/scene_1280x720_1.png"
# Default settings for selecting unfocused 'joint' zone
recX = int(0.475*pwidth)
recY = pheight
recW = int(pwidth/20)


if (showHelp == 1):
    print ('\n    <><><><><><>KEY USAGE<><><><><><>')
    print ('Esc key ---------- exit')
    print ('Enter ------------ save settings to file')
    print ('Left, Right keys - move choosen zone')
    print ('Up, Down keys ---- change width of choosen zone \n')


# If path is empty than capture from camera, else load this file
if (loadImagePath == ''):
    # Import is here for compatibility with desktop usage instead of Raspberry
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    # Initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution=(pwidth,pheight)
    rawCapture = PiRGBArray(camera)

    # Allow the camera to warmup
    time.sleep(0.1)

    # Grab an image from the camera
    camera.hflip = True
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
else:
    image = cv2.imread(loadImagePath)
    if (image is None):
        print ('Can not read image from file \"'+loadImagePath+'\"')
        exit(0)


# Let user choose unfocused zone manually 
while (1):
    imTune = copy.copy(image)
    cv2.rectangle(imTune, (recX,recY), (recX+recW, 0), (0,255,0), 3)
    cv2.imshow("Image", imTune)
    k = cv2.waitKey(0)
    print (k)
    if k==27: #ESC key - just exit
        break
    elif k==-1:
        print k
        continue
    elif (k==65361) | (k==63234): #LEFT pressed
        recX = recX-1
    elif (k==65363) | (k==63235): #RIGHT pressed
        recX = recX+1
    elif (k==65362) | (k==63232): #UP pressed
        recW = recW+1
    elif (k==65364) | (k==63233): #DOWN pressed
        recW = recW-1
    elif (k==65421) | (k==13) | (k==10): #ENTER pressed - save results
        minW=min(recX, pwidth-recX-recW)
        leftX1=recX-minW
        leftX2=recX
        rightX1=recX+recW
        rightX2=rightX1+minW 
        print ('imageWidth = ', minW, ' jointWidth=', recW, ' leftIndent=', leftX1, \
                ' rightIndent=', rightX1)
        result = json.dumps({'imageWidth':minW, 'leftIndent':leftX1, \
                            'rightIndent':rightX1, 'jointWidth':recW},sort_keys=True, \
                             indent=4, separators=(',',':'))
        fName = 'pf_'+ str(pwidth) +'_'+str(pheight)+'.txt'
        f = open (str(fName), 'w') 
        f.write(result)
        f.close()
        print ('Settings saved to file'+str(fName))
        break