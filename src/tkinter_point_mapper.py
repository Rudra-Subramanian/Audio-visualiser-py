"""
Making an easy module to visualize a list of 2d or 3d points using tkinter.
"""

import tkinter
import numpy as np 
from scipy.spatial.transform import Rotation


class camera:
    def __init__(self, position=(0,0,0), rotation=(0,0,0)):
        self.position = position
        self.rotation = rotation

    def project_point_on_camera(self, point):
        # Placeholder for camera projection logic
        point = self.transform_point_position(point)
        point = self.transform_point_rotation(point)
        return point


    def transform_point_position(self, point):
        #check if point is 2d or 3d
        if len(point) == 2:
            x, y = point
            z = 0
            x = x - self.position[0]
            y = y - self.position[1]
            return (x, y)
        elif len(point) == 3:
            x, y, z = point
            x = x - self.position[0]
            y = y - self.position[1]
            z = z - self.position[2]
            return (x, y, z)
    
    def transform_point_rotation(self, point):
        #check if point is 2d or 3d
        if len(point) == 2:
            initial = np.array(point)
            #2d rotation matrix
            r = Rotation.from_euler('xy', [self.rotation[0], self.rotation[1]], degrees=True)
            rotated = r.apply(initial)
            return (rotated[0], rotated[1])
        elif len(point) == 3:
            initial = np.array(point)
            r = Rotation.from_euler('xyz', [self.rotation[0], self.rotation[1], self.rotation[2]], degrees=True)
            rotated = r.apply(initial)
            return (rotated[0], rotated[1], rotated[2])
        


        return point



class twoDimensionalPointMapper:
    def __init__(self, point_list, width=800, height=600, point_radius=3, centerx=True, centery=True, camera=None):
        self.centerx = centerx
        self.centery = centery
        self.point_list = point_list
        self.width = width
        self.height = height
        self.point_radius = point_radius
        self.all_points_on_canvas = []
        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.root, width=self.width, height=self.height, bg='black')
        self.canvas.pack()

    
    def run(self):
        
        self.draw_points()

        self.root.mainloop()

    def draw_points(self):
        self.all_points_on_canvas = []
        for point in self.point_list:
            x, y = point
            x, y = self.translate_point((x, y), self.centerx, self.centery)
            newpoint = self.canvas.create_oval(x, y,
                                    x, y,
                                    width=self.point_radius,
                                    fill='green',
                                    outline='green')
            self.all_points_on_canvas.append(newpoint)
    
    def change_points(self, new_point_list):
        self.point_list = new_point_list
        for point in self.all_points_on_canvas:
            self.canvas.delete(point)
        self.draw_points()
    
    def delete_all(self):
        self.canvas.delete("all")

    def delete_window(self):
        self.root.destroy()

    """
    This function will translate the given x,y point (on a 0,0 being in the middle coordinate system) to the proper tkinter coordinate system
    #where 0,0 is at the top left corner +x is right and +y is down.
    """
    def translate_point(self, point, centerx=True, centery=True):
        x, y = point
        if centerx:
            translated_x = ((self.width+1) // 2) + x
        else:
            translated_x = x
        if centery:
            translated_y = ((self.height-1) // 2) - y
        else:
            translated_y = (self.height-1) - y
        return (translated_x, translated_y)

"""
by default the center of the screen is at 0,0,0, so something placed at 0z will not be visible as it is in the same plane as the camera
adding camera position and rotation that will do matrix transformations to find projected position of point
"""
class threeDimensionalPointMapper(twoDimensionalPointMapper):
    def __init__(self, point_list, width=800, height=600, point_radius=3, centerx=True, centery=True, camera=None):
        super().__init__([], width, height, point_radius, centerx, centery)
        self.camera=camera
        self.point_list_3d = point_list
        self.projected_point_list = self.project_points(self.point_list_3d)
        self.change_points(self.projected_point_list)
    

    def project_points(self, point_list_3d):
        projected_points = []
        for point in point_list_3d:
            point = self.camera.project_point_on_camera(point)
            x, y, z = point
            projected_x = x/z
            projected_y = y/z
            projected_points.append((projected_x, projected_y))
        return projected_points


class twoDimensionalPointAnimator(twoDimensionalPointMapper):
    def __init__(self, list_of_point_lists, width=800, height=600, point_radius=3, centerx=True, centery=True, frames_per_second=24):
        super().__init__(list_of_point_lists[0], width, height, point_radius, centerx, centery)
        self.list_of_point_lists = list_of_point_lists
        self.fps = frames_per_second
        self.current_frame = 0
        self.total_frames = len(list_of_point_lists)
        self.frame_text = self.canvas.create_text(50, 20, fill="white", font="Times 10 bold", text=f'2D Point Mapper')
        

        

    def animate(self):
        self.frame = 0

        
        self.change_points(self.list_of_point_lists[self.current_frame])
        self.root.after(int(1000 / self.fps), self.update_frame)

        self.root.mainloop()
    

    def update_frame(self):
        self.canvas.itemconfigure(self.frame_text, text=f'Frame: {self.current_frame}')
        self.change_points(self.list_of_point_lists[self.current_frame])
        self.current_frame = (self.current_frame + 1)
        if self.current_frame < self.total_frames:
            self.root.after(int(1000 / self.fps), self.update_frame)


class threeDimensionalPointAnimator(threeDimensionalPointMapper):
    def __init__(self, list_of_point_lists_3d, width=800, height=600, point_radius=3, centerx=True, centery=True, frames_per_second=24, camera=None):
        super().__init__(list_of_point_lists_3d[0], width, height, point_radius, centerx, centery, camera)
        self.fps = frames_per_second
        self.current_frame = 0
        self.total_frames = len(list_of_point_lists_3d)
    
    def animate(self):
        self.frame = 0
        newpointlist = self.project_points(self.list_of_point_lists_3d[self.current_frame])
        self.change_points(newpointlist)
        self.root.after(int(1000 / self.fps), self.update_frame)
        self.root.mainloop()
    
    def update_frame(self):
        self.newpoints = self.project_points(self.list_of_point_lists_3d[self.current_frame])
        self.change_points(self.newpoints)
        self.current_frame = (self.current_frame + 1)
        if self.current_frame < self.total_frames:
            self.root.after(int(1000 / self.fps), self.update_frame)


    