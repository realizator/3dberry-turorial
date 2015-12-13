3Dberry tutorial scripts
===========

Set of tutorial scripts for depth map building on Raspberry Pi camera with OpenCV.

Detailed information with video you can find in a set of lessons (Russian language):
http://3dberry.org/node/6 

Brief scripts description:

<b>1_show_image.py</b> - takes picture from camera, adds vertical overlayed line for camera 
align.
<b>2_pair_fit.py</b> - takes picture from camera or from file and let user set picture
split parameters for stereopair.
<b>3_chess_cycle.py</b> - takes a series of photos for stereopair calibration, shows count
down timer. You need a printed chessboard with 9x6 parameters.
<b>4_pairs_cut.py</b> - just cuts set of captured photos to stereopair according to 
script 2 result.
<b>5_calibration.py</b> - calibrate 3Dberry stereopair using pairs with chessboards from
script 4.
<b>6_depth_map.py</b> - sample script for "quick and easy" disparity map building. Gives
you bad results, but a lot of understanding.
<b>7_dm_tune.py</b> - script for fine tune of disparity map with your 3Dberry device.
<b>8_dm_video.py</b> - script builds disparity map in real time and show it as overlay
on fullscreen video.


