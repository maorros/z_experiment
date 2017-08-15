from RobotPainter import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

class Grid:
    def __init__(self, grid_len_x = 100, grid_len_y = 100, canvas_len_x = 400, canvas_len_y = 400, \
                 canvas_translation_x = 170, canvas_translation_y=100, \
                 camera_translation_x = 100, camera_translation_y = 100, camera_ratio = 2):
        self.grid_len_x = grid_len_x
        self.grid_len_y = grid_len_y
        self.canvas_len_x = canvas_len_x
        self.canvas_len_y = canvas_len_y
        self.canvas_translation_x = canvas_translation_x
        self.canvas_translation_y = canvas_translation_y

        self.camera_ratio = camera_ratio
        self.camera_translation_x = camera_translation_x
        self.camera_translation_y = camera_translation_y


    def grid_to_canvas_cord(self, x_vec_grid, y_vec_grid, grid_i, grid_j):
        x_vec_canvas = []
        y_vec_canvas = []
        for n in range(len(x_vec_grid)):
            x_c = x_vec_grid[n] + grid_i * self.grid_len_x + self.canvas_translation_x
            y_c = y_vec_grid[n] + grid_j * self.grid_len_y + self.canvas_translation_y
            x_vec_canvas.append(x_c)
            y_vec_canvas.append(y_c)
        return x_vec_canvas, y_vec_canvas

    def grid_to_camera_cord(self, x_vec_grid, y_vec_grid, grid_i, grid_j):
        x_vec_camera = []
        y_vec_camera = []
        for n in range(len(x_vec_grid)):
            x_c = (x_vec_grid[n] + grid_i * self.grid_len_x) * self.camera_ratio + self.camera_translation_x
            y_c = (y_vec_grid[n] + grid_j * self.grid_len_y) * self.camera_ratio + self.camera_translation_y
            x_vec_camera.append(x_c)
            y_vec_camera.append(y_c)
        return x_vec_camera, y_vec_camera

    def grid_to_camera_rect(self, grid_i, grid_j):
        x_vec, y_vec = self.grid_to_camera_cord([0, self.grid_len_x], [0, self.grid_len_y], grid_i, grid_j)
        x = int(x_vec[0])
        y = int(y_vec[0])
        w = int(x_vec[1] - x_vec[0])
        h = int(y_vec[1] - y_vec[0])
        return x,y,w,h


