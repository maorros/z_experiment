from RobotPainter import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from scipy import interpolate
import cv2

img = cv2.imread('sim_line.png',0)
ret1,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
_,contours,hierarchy = cv2.findContours(th1, 1, 2)
elps = cv2.fitEllipse(contours[1])
out = cv2.ellipse(img,elps,(0,255,0),2)
plt.imshow(out)

# png = mpimg.imread('sim_line.png')


robot = RobotPainter()
vis = Camera()
# simulation
robot.init('134.34.231.221:33333')
vis.init('134.34.231.221:55555')

# big robot
# robot.init('192.168.1.6:33333')
# vis.init('192.168.1.6:55555')
robot.start()
[width, height] = robot.get_canvas_size()
print (width, height)

k = 0
robot.dip_slot_paint(0)
robot.move_pose_safe([100,200],[100+k*100,100+k*100], k*np.ones(2))
img = vis.get_image()

k = 1
robot.dip_slot_paint(0)
robot.move_pose_safe([100,200], [100+k*100,100+k*100], k*np.ones(2))
img = vis.get_image()

k = 2
robot.dip_slot_paint(0)
robot.move_pose_safe([100,200], [100+k*100,100+k*100], k*np.ones(2))
img = vis.get_image()


#res = vis.get_resolution()
#img = vis.get_image()
#png = vis.get_png()

png = mpimg.imread('sim_line.png')