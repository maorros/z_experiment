import capnp
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

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

    def move_pose_safe(self, x, y, z=None, q_x=None, q_y=None, q_z=None, q_w=None):
        if len(x) != len(y):
            print 'x and y are not at the same length'
        if z is None:
            z = np.zeros(len(x))
            q_x = np.zeros(len(x))
            q_y = np.zeros(len(x))
            q_z = np.zeros(len(x))
            q_w = np.ones(len(x))

            poses_list = []
            for n in range(len(x)):
                # Point = {'x':x[n], 'y':y[n], 'z':z[n]}
                # Quaternion = {'x': q_x[n], 'y': q_y[n], 'z': q_z[n], 'w': q_w[n]}
                Point = {'x': np.float64(x[n]).item(), 'y': np.float64(y[n]).item(), 'z': np.float64(z[n]).item()}
                Quaternion = {'x': np.float64(q_x[n]).item(), 'y': np.float64(q_y[n]).item(), 'z': np.float64(q_z[n]).item(), 'w': np.float64(q_w[n]).item()}
                Pose = {'position': Point, 'orientation': Quaternion}
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

    def get_png(self):
        eval_promise = self.camera.get()
        result = eval_promise.wait()
        img_dict = result.picture.to_dict()
        png_str = img_dict['png']
        with open("test.png", "wb") as file:
            file.write(png_str)
        png = mpimg.imread('test.png')
        return png

    def get_resolution(self):
        eval_promise = self.camera.imageResolution()
        result = eval_promise.wait()
        print ('width: ', result.size.width, 'height: ', result.size.height)
        return result.size








