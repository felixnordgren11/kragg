''' Here some code will be written,
NAWRAHL CABON BRAINWOW
'''
import tkinter as tk
from settings import Settings
from settings import Fact, Lie
from button import Button


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
                             self.settings.width*0.95, self.settings.height*0.98, outline = '#fff176', width = 2, activewidth = 4)
        
        self.round_rectangle(self.canvas, self.settings.width*0.05, self.settings.height*0.05, 
                             self.settings.width*0.95, self.settings.height*0.12, outline = '#fff176', width = 2, fill = '#fff176')
        
        self.canvas.create_rectangle(self.settings.width*0.05, self.settings.height*0.1, 
                             self.settings.width*0.95, self.settings.height*0.15, outline = '', fill = '#fff176')
        
        ##
        self.canvas.create_text(self.settings.width*0.5, self.settings.height*0.1, text = 'Bacon narwhal', font = ('Comic Sans MS', 20), fill = 'black')   
        
        
        #Enable button
        for btn in self.settings.buttonsettings.values():
            a = Button(self.canvas, **btn)
            a.draw()


        self.canvas.create_rectangle(self.settings.width*0.1, self.settings.height*0.955, 
                             self.settings.width*0.90, self.settings.height*0.955, outline = '', fill = '#fff176')
        
        self.canvas.create_rectangle(self.settings.width*0.1, self.settings.height*0.955, 
                             self.settings.width*0.1, self.settings.height*0.96, outline = '', fill = '#fff176')
        
        self.canvas.create_rectangle(self.settings.width*0.90, self.settings.height*0.955, 
                             self.settings.width*0.90, self.settings.height*0.96, outline = '', fill = '#fff176')
        
        self.canvas.create_rectangle(self.settings.width*0.1, self.settings.height*0.96, 
                             self.settings.width*0.90, self.settings.height*0.96, outline = '', fill = '#fff176')
    
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
 
