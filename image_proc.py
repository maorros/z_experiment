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

elps = cv2.fitEllipse(contours[1])
out = cv2.ellipse(th1,elps,(0,255,0),2)
plt.imshow(out)