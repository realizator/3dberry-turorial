3Dberry tutorial scripts
===========

Set of tutorial scripts for disparity map building on Raspberry Pi with 3Dberry camera add-on.

Detailed information with video you can find in a set of lessons (Russian language):
http://3dberry.org/node/6 

Brief scripts description:

<b>1_show_image.py</b> - takes picture from camera, adds vertical overlayed line for camera 
align.<br>
<b>2_pair_fit.py</b> - takes picture from camera or from file and let user set picture
split parameters for stereopair.<br>
<b>3_chess_cycle.py</b> - takes a series of photos for stereopair calibration, shows count
down timer. You need a printed chessboard with 9x6 parameters.<br>
<b>4_pairs_cut.py</b> - just cuts set of captured photos to stereopair according to 
script 2 result.<br>
<b>5_calibration.py</b> - calibrate 3Dberry stereopair using pairs with chessboards from
script 4.<br>
<b>6_depth_map.py</b> - sample script for "quick and easy" disparity map building. Gives
you bad results, but a lot of understanding.<br>
<b>7_dm_tune.py</b> - script for fine tune of disparity map with your 3Dberry device.<br>
<b>8_dm_video.py</b> - script builds disparity map in real time and show it as overlay
on fullscreen video.<br>


