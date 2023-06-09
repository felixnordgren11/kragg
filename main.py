''' Here some code will be written,
NAWRAHL CABON BRAINWOW
'''
import tkinter as tk
from settings import Settings

class GUI:
    '''
    Our main class
    '''

    def __init__(self):
        '''Initializes variables'''

        self.root = tk.Tk()
        self.settings = Settings()
        self.canvas = tk.Canvas(self.root, **self.settings.canvassettings)
        self.canvas.pack()
        self.root.title(self.settings.title)
        self.root.geometry(self.settings.geometry)
  
        ## EXPERIMENT

        self.round_rectangle(self.canvas, self.settings.width*0.05, self.settings.height*0.05, 
                             self.settings.width*0.95, self.settings.height*0.95, outline = 'green', width = 2, activewidth = 4)
        
        self.round_rectangle(self.canvas, self.settings.width*0.05, self.settings.height*0.05, 
                             self.settings.width*0.95, self.settings.height*0.12, outline = 'green', width = 2, fill = 'green')
        
        self.canvas.create_rectangle(self.settings.width*0.05, self.settings.height*0.1, 
                             self.settings.width*0.95, self.settings.height*0.15, outline = '', fill = 'green')
        
        ## 


    def round_rectangle(self, master, x1, y1, x2, y2, r=25, **kwargs):    
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r,
                x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2,
                x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, 
                x1, y1+r, x1, y1)
        return master.create_polygon(points, **kwargs, smooth=True)

    def run(self):
        self.root.mainloop()
        pass


if '__main__' == __name__:
    gui = GUI()
    gui.run()
 
