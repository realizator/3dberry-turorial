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
import json

# Global variables preset
total_photos = 15
photo_Width = 1280
photo_Height = 720
params_file = './src/pf_1280_720.txt'
photo_counter = 0


# Read pair cut parameters
f = open(params_file, 'r')
data = json.load(f)
imageWidth = data['imageWidth']
jointWidth = data['jointWidth']
leftIndent = data['leftIndent']
rightIndent = data['rightIndent']
f.close()


# Main pair cut cycle
while photo_counter != total_photos:
    photo_counter +=1
    filename = './src/scene_'+str(photo_Width)+'x'+str(photo_Height)+\
               '_'+str(photo_counter) + '.png'
    pair_img = cv2.imread(filename,-1)
#    cv2.imshow("ImagePair", pair_img)
    imgLeft = pair_img [0:photo_Height,leftIndent:imageWidth] #Y+H and X+W
    imgRight = pair_img [0:photo_Height,rightIndent:rightIndent+imageWidth]
    leftName = './pairs/left_'+str(photo_counter).zfill(2)+'.png'
    rightName = './pairs/right_'+str(photo_counter).zfill(2)+'.png'
    cv2.imwrite(leftName, imgLeft)
    cv2.imwrite(rightName, imgRight)
    print ('Pair No '+str(photo_counter)+' saved.')
    
print ('End cycle')

