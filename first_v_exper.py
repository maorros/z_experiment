from RobotPainter import *
from Grid import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from scipy import interpolate
import cv2

def detect_changes(img1, img2):
    dif = np.abs(img1 - img2)

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
    y_vec = [25,25]

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

def generate_v(grid,v):
    robot = RobotPainter()
    vis = Camera()
    # simulation
    #robot.init('134.34.231.221:33333')
    #vis.init('134.34.231.221:55555')

    # big robot
    robot.init('192.168.1.6:33333')
    vis.init('192.168.1.6:55555')

    robot.start()
    [width, height] = robot.get_canvas_size()
    print ('canvas_size', width, height)

    vis.get_resolution()

    robot.hide_pose()
    png = vis.get_png('grid_all_v' + '.png')
    robot.home_pose()

    x_vec = [50,550]
    y_vec = [25,25]

    col = 3
    row = 12
    robot.dip_slot_paint(0)

    for i in range(col):
        for j in range(row):
            if i*row+j+1 > len(v):
                break
            print ('v', v[i * row + j])
            x_c, y_c = grid.grid_to_canvas_cord(x_vec, y_vec, i, j)
           # robot.dip_slot_paint(0)
            robot.move_pose_safe(x_c, y_c, z = 0*np.ones(len(x_c)), v=v[i*row+j]*np.ones(len(x_c)))
            robot.hide_pose()
            png = vis.get_png('grid_' + str(i) + '_' + str(j) + '.png')
            robot.home_pose()
            robot.dip_slot_paint(0)

    robot.hide_pose()
    png = vis.get_png('grid_all_v_end' + '.png')
    robot.home_pose()

def analyse_z(grid, z):
    col = 3
    row = 12
    brush_width = []
    stroke_length = []

    fig1 = plt.figure(1)
    fig2 = plt.figure(2)

    for i in range(1,col):
        for j in range(row):
            if i*row+j+1 > len(z):
                break
            #img = cv2.imread('grid_' + str(i) + '_' + str(j) + '.png',0)
            img = cv2.imread('grid_all_v_end' + '.png', 0)
            x, y, w, h = grid.grid_to_camera_rect(i, j)
            #out = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi = img[y:(y + h), x:(x + w)]
            ret1, th1 = cv2.threshold(roi, 250, 255, cv2.THRESH_BINARY)
            plt.figure(1)
            plt.imshow(th1)
            plt.pause(0.5)
            _, contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, offset=(x, y))
            cnt_len = [len(cnt) for cnt in contours]
            print cnt_len
            max_ind = np.argmax(cnt_len)
            if len(contours[max_ind]) > 4:
                out = cv2.drawContours(img, [contours[max_ind]], 0, (0, 0, 255), 4)
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
                out = cv2.drawContours(out, [box], 0, (0, 0, 255), 4)
                plt.figure(2)
                plt.imshow(out)
                plt.pause(0.5)
            else:
                brush_width.append(0)
                stroke_length.append(0)


            print ('z', z[i*row+j], 'brush_width', brush_width[-1], 'stroke_length', stroke_length[-1])



    plt.figure()
    plt.plot(z,brush_width)
    plt.title('Brush width as a function of Z')
    # plt.pause(5)

    fig = plt.figure()
    plt.plot(z,stroke_length)
    plt.title('Stroke length as a function of Z')
    plt.pause(10)
    plt.pause(1) # <-------
    raw_input("<Hit Enter To Close>")
    plt.close(fig)


# real canvas grid
#grid = Grid(grid_len_x = 250, grid_len_y = 70, canvas_len_x = 1200, canvas_len_y = 800, \
                 # canvas_translation_x = 170, canvas_translation_y=100, \
                 # camera_translation_x = 150*3.07, camera_translation_y = 120*3.07, camera_ratio = 3.07)

# simulation grid
grid = Grid(grid_len_x = 600, grid_len_y = 50, canvas_len_x = 1200, canvas_len_y = 800, \
            canvas_translation_x = 170+250, canvas_translation_y=100+200, \
            camera_translation_x = (170+250)*2, camera_translation_y = (100+200)*2, camera_ratio = 2)

z = np.arange(-60,10,5)

v = np.arange(0.1,0.9,0.1)

generate_v(grid,v)

#generate_z(grid,z)
analyse_z(grid, v)
    #
# grid.grid_to_camera_cord([0,10], [10,20], 0,0)
#
# img = cv2.imread('sim_line.png',0)
#
# ret1,th1 = cv2.threshold(img,150,255,cv2.THRESH_BINARY)
# _,contours,hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# out = cv2.drawContours(img,contours, -1, (0,0,255),2)
# plt.imshow(out)
#
#
# for cnt in contours:
#     print ('len', len(cnt))
#     img = cv2.drawContours(img, [cnt], 0, (0, 0, 255), 2)
#     plt.imshow(img)
#
#
# out = cv2.drawContours(img,contours[0],0,(0,0,255),2)
# plt.imshow(out)
#
# cnt = contours[1]
# rect = cv2.minAreaRect(cnt)
# box = cv2.boxPoints(rect)
# box = np.int0(box)
# out = cv2.drawContours(img,[box],0,(0,0,255),2)
#
# cv2.pointPolygonTest(box, (400-27,526), True)
#
#
# # x,y,w,h = cv2.boundingRect(contours[1])
# # out = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
# # plt.imshow(out)
#
# # elps = cv2.fitEllipse(contours[1])
# # out = cv2.ellipse(img,elps,(0,255,0),2)
# plt.imshow(out)
#
# # png = mpimg.imread('sim_line.png')
#
#
# robot = RobotPainter()
# vis = Camera()
# # simulation
# robot.init('134.34.231.221:33333')
# vis.init('134.34.231.221:55555')
#
# # big robot
# #robot.init('192.168.1.6:33333')
# #vis.init('192.168.1.6:55555')
# robot.start()
# [width, height] = robot.get_canvas_size()
# print (width, height)
#
# x_offset = 170
# y_offset = 100
#
# k = 0
# # depth = [-15,-10,-5,0,5,10]
# depth = [-40,-35,-30,-25,-20,-15]
# robot.dip_slot_paint(0)
#
# y_jump = 50
#
#
# for k in range(6):
# #    robot.dip_slot_paint(0)
#     start_point = (10+x_offset, 50+k*y_jump+y_offset)
#     end_point = (110+x_offset, 50+k*y_jump+y_offset)
#
#     robot.move_pose_safe([start_point[0], end_point[0]],[start_point[1], end_point[1]], depth[k]*np.ones(2))
#     png = vis.get_png('test_'+str(k)+'.png')
# #img = vis.get_image()
#
# # k = 1
# # robot.dip_slot_paint(0)
# # robot.move_pose_safe([100,200], [100+k*100,100+k*100], k*np.ones(2))
# # img = vis.get_image()
# #
# # k = 2
# # robot.dip_slot_paint(0)
# # robot.move_pose_safe([100,200], [100+k*100,100+k*100], k*np.ones(2))
# # img = vis.get_image()
# #
# #
# # #res = vis.get_resolution()
# # #img = vis.get_image()
# # #png = vis.get_png()
# #
# # png = mpimg.imread('sim_line.png')