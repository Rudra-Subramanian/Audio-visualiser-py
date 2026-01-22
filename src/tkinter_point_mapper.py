"""
Making an easy module to visualize a list of 2d or 3d points using tkinter.
"""

import tkinter 

class twoDimensionalPointMapper:
    def __init__(self, point_list, width=800, height=600, point_radius=3, centerx=True, centery=True):
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


class threeDimensionalPointMapper(twoDimensionalPointMapper):
    def __init__(self, point_list, width=800, height=600, point_radius=3, centerx=True, centery=True):
        super().__init__([], width, height, point_radius, centerx, centery)
        self.point_list_3d = point_list
        self.projected_point_list = self.project_points(self.point_list_3d)
        self.change_points(self.projected_point_list)
    

    def project_points(self, point_list_3d):
        projected_points = []
        for point in point_list_3d:
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
    def __init__(self, list_of_point_lists_3d, width=800, height=600, point_radius=3, centerx=True, centery=True, frames_per_second=24):
        super().__init__(list_of_point_lists_3d[0], width, height, point_radius, centerx, centery)
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


    