import capnp
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

#
# This class enables interaction with the robot or the simulation.
#
# This class requires that FeedbackCamera.capnp and RobotService.capnp will be at the same directory.
#
#  in order to initialize the connection do the following:
#
# from RobotPainter import *
#
# robot = RobotPainter()
# robot.init('134.34.231.221:33333')
# robot.start()
#
# In order to initiate the camera do:
#
# vis = Camera()
# vis.init('134.34.231.221:55555')
#



class RobotPainter():
    service = None
    client = None
    robot = None

    def init(self, socket):
        capnp.remove_import_hook()
        self.service = capnp.load('RobotService.capnp')
        self.client = capnp.TwoPartyClient(socket)
        self.robot = self.client.bootstrap()
        self.robot = self.robot.cast_as(self.service.RobotService)

    def start(self):
        eval_promise = self.robot.start()
        result = eval_promise.wait()
        return result

    def get_canvas_size(self):
        eval_promise = self.robot.getCanvasSize()
        result = eval_promise.wait()
        width = result.size.width
        height = result.size.height
        return [width, height]

    def dip_slot_paint(self, index):
        eval_promise = self.robot.dipSlotPaint(index)
        result = eval_promise.wait()

    def home_pose(self):
        eval_promise = self.robot.moveMacro('homePose')
        result = eval_promise.wait()

    def hide_pose(self):
        eval_promise = self.robot.moveMacro('hidePose')
        result = eval_promise.wait()

    def move_pose_safe(self, x, y, z=None, q_x=None, q_y=None, q_z=None, q_w=None, v=None):
        if len(x) != len(y):
            print 'x and y are not at the same length'
        if z is None:
            z = np.zeros(len(x))
        if q_x is None:
            q_x = np.zeros(len(x))
        if q_y is None:
            q_y = np.zeros(len(x))
        if q_z is None:
            q_z = np.zeros(len(x))
        if q_w is None:
            q_w = np.ones(len(x))
        if v is None:
            v = 0.5*np.ones(len(x))

        poses_list = []
        for n in range(len(x)):
            # Point = {'x':x[n], 'y':y[n], 'z':z[n]}
            # Quaternion = {'x': q_x[n], 'y': q_y[n], 'z': q_z[n], 'w': q_w[n]}
            Point = {'x': np.float64(x[n]).item(), 'y': np.float64(y[n]).item(), 'z': np.float64(z[n]).item()}
            Quaternion = {'x': np.float64(q_x[n]).item(), 'y': np.float64(q_y[n]).item(), 'z': np.float64(q_z[n]).item(), 'w': np.float64(q_w[n]).item()}
            Pose = {'position': Point, 'orientation': Quaternion, 'velocity' : np.float64(v[n]).item()}
            poses_list.append(Pose)
        eval_promise = self.robot.movePathSafe(poses_list)
        result = eval_promise.wait()
        return result

class Camera():
    service = None
    client = None
    camera = None

    def init(self, socket):
        capnp.remove_import_hook()
        self.service = capnp.load('FeedbackCamera.capnp')
        self.client = capnp.TwoPartyClient(socket)
        self.camera = self.client.bootstrap()
        self.camera = self.camera.cast_as(self.service.FeedbackCamera)

    def get_image(self):
        eval_promise = self.camera.get()
        result = eval_promise.wait()
        return result

    def get_png(self, filename = 'test.png'):
        eval_promise = self.camera.get()
        result = eval_promise.wait()
        img_dict = result.picture.to_dict()
        png_str = img_dict['png']
        with open(filename, "wb") as file:
            file.write(png_str)
        png = mpimg.imread(filename)
        return png

    def get_resolution(self):
        eval_promise = self.camera.imageResolution()
        result = eval_promise.wait()
        print ('pic_size','width: ', result.size.width, 'height: ', result.size.height)
        return result.size








