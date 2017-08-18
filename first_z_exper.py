from RobotPainter import *
from Grid import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from scipy import interpolate
import cv2

# ('canvas_size', 1199.9719162622098, 800.8501084560082)
# ('width: ', 3701, 'height: ', 2445)

def generate_z(grid,z):
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
    print ('canvas_size', width, height)

    vis.get_resolution()

    robot.hide_pose()
    png = vis.get_png('grid_all_2' + '.png')
    robot.home_pose()

    x_vec = [25,150]
    y_vec = [25,50]

    col = 3
    row = 7
    #robot.dip_slot_paint(0)

    for i in range(col):
        for j in range(row):
            if i*row+j+1 > len(z):
                break
            print ('z', z[i * row + j])
            x_c, y_c = grid.grid_to_canvas_cord(x_vec, y_vec, i, j)
           # robot.dip_slot_paint(0)
            robot.move_pose_safe(x_c, y_c, z[i*row+j]*np.ones(len(x_c)))
            robot.hide_pose()
            png = vis.get_png('grid_' + str(i) + '_' + str(j) + '.png')
            robot.home_pose()
        robot.dip_slot_paint(0)

    robot.hide_pose()
    png = vis.get_png('grid_all' + '.png')
    robot.home_pose()
    print 'move png to another directory'


def analyse_z(grid, z):
    col = 3
    row = 7
    brush_width = []
    stroke_length = []

    fig1 = plt.figure(1)
    fig2 = plt.figure(2)

    for i in range(col):
        for j in range(row):
            if i*row+j+1 > len(z):
                break
            #img = cv2.imread('grid_' + str(i) + '_' + str(j) + '.png',0)
            img = cv2.imread('grid_all_3' + '.png', 0)  # image is after some processing
            x, y, w, h = grid.grid_to_camera_rect(i, j)
            #out = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi = img[y:(y + h), x:(x + w)]
            ret1, th1 = cv2.threshold(roi, 150, 255, cv2.THRESH_BINARY)
            plt.figure(1)
            plt.imshow(th1)
            #plt.pause(0.1)
            _, contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, offset=(x, y))
            cnt_len = [len(cnt) for cnt in contours]
            print cnt_len
            max_ind = np.argmax(cnt_len)
            if len(contours[max_ind]) > 4:
                out = cv2.drawContours(img, [contours[max_ind]], 0, (0, 0, 255), 6)
                # find bounding rectangle
                rect = cv2.minAreaRect(contours[max_ind])

                if rect[1][0] > rect[1][1]:
                    brush_width.append(rect[1][1])
                    stroke_length.append(rect[1][0])
                else:
                    brush_width.append(rect[1][0])
                    stroke_length.append(rect[1][1])
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                out = cv2.drawContours(out, [box], 0, (0, 0, 255), 6)
                plt.figure(2)
                plt.imshow(out)
                plt.pause(0.1)
            else:
                brush_width.append(0)
                stroke_length.append(0)


            print ('z', z[i*row+j], 'brush_width', brush_width[-1], 'stroke_length', stroke_length[-1])



    plt.figure()
    plt.plot(z,brush_width)
    plt.title('Brush width as a function of Z')
    #plt.pause(5)

    fig = plt.figure()
    plt.plot(z,stroke_length)
    plt.title('Stroke length as a function of Z')
    plt.pause(10)
    plt.pause(1) # <-------
    raw_input("<Hit Enter To Close>")
    plt.close(fig)


# real canvas grid
grid = Grid(grid_len_x = 250, grid_len_y = 70, canvas_len_x = 1200, canvas_len_y = 800, \
                 canvas_translation_x = 170, canvas_translation_y=100, \
                 camera_translation_x = 150*3.07, camera_translation_y = 120*3.07, camera_ratio = 3.07)

# simulation grid
#grid = Grid(grid_len_x = 250, grid_len_y = 50, canvas_len_x = 1200, canvas_len_y = 800, \
                 # canvas_translation_x = 170, canvas_translation_y=100, \
                 # camera_translation_x = 170*2, camera_translation_y = 100*2, camera_ratio = 2)

z = np.arange(-60,10,5)

v = np.arange(0.1,0.9,0.1)

#generate_v(grid,v)

#generate_z(grid,z)
analyse_z(grid, z)
