from RobotPainter import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from scipy import interpolate

png = mpimg.imread('sim_line.png')


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

#res = vis.get_resolution()
#img = vis.get_image()
#png = vis.get_png()

png = mpimg.imread('sim_line.png')