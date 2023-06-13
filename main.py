''' Here some code will be written,
NAWRAHL CABON BRAINWOW

Tanke: Ta bort postion från gaugesettings så att allt bara är text. 

'''
import tkinter as tk
from settings import *
from button import *
from gauge import Gauge


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
        

        # Bind click event

        self.root.bind_all("<Key>", self.key)
        self.root.bind_all("<Button-1>", self.callback)
        self.canvas.focus_set() 
        self.draw_border()
        
        #Enable buttons
        self.btns = {}
        for label, btn in self.settings.buttonsettings.items():
            self.btns[label] = Button(self.canvas, label, **btn)
            self.btns[label].draw()
        
        self.gges = {}
        for label, gge in self.settings.gaugesettings.items():
            self.gges[label] = Gauge(self.canvas, label, **gge)
            self.gges[label].draw()

    def draw_border(self):

        self.round_rectangle(self.canvas, self.settings.width*0.05, self.settings.height*0.05, 
                             self.settings.width*0.95, self.settings.height*0.98, outline = self.settings.border_color, width = 2, activewidth = 4)
        self.round_rectangle(self.canvas, self.settings.width*0.05, self.settings.height*0.05, 
                             self.settings.width*0.95, self.settings.height*0.12, outline = self.settings.border_color, width = 2, fill = self.settings.border_color)
        self.canvas.create_rectangle(self.settings.width*0.05, self.settings.height*0.1, 
                             self.settings.width*0.95, self.settings.height*0.15, outline = '', fill = self.settings.border_color)  
        ##
        self.canvas.create_text(self.settings.width*0.5, self.settings.height*0.1, text = 'TrumpSoft', font = ('Small Fonts', 20), fill = 'black')  
    


    def round_rectangle(self, master, x1, y1, x2, y2, r=25, **kwargs):    
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r,
                x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2,
                x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, 
                x1, y1+r, x1, y1)
        return master.create_polygon(points, **kwargs, smooth=True)
    

    def key(self, event):
            pass
                 
            
    def callback(self, event):
            x, y = event.x, event.y
            print(x,y)
            # Helper function
            inside_btn = lambda x, y, btn: (x > btn.kwargs['x1'] and x < btn.kwargs['x2']) and (y > btn.kwargs['y1'] and y < btn.kwargs['y2']) 
            # Check if one of boxes are clicked.
            # First check that any of boxes is selected:
            if not any([inside_btn(x,y,btn) for btn in self.btns.values()]):
                 return 
            
            for btn in self.btns.values():
                if inside_btn(x, y, btn):
                     btn.selected(Fact)
                else:
                     btn.selected(Lie)


    def run(self):
        self.root.mainloop()

        pass


if '__main__' == __name__:
    print("America is great")
    print("Tack som fan bror")
    gui = GUI()
    gui.run()
 
