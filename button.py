import tkinter as tk

class Button:

    def __init__(self, master, label, **kwargs):
        '''Instantiates the button according to the given data
        '''
        self.master = master
        self.labeltext = tk.text
        self.kwargs = kwargs

    def round_rectangle(self, master, x1, y1, x2, y2, r=25, **kwargs):    
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r,
                x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2,
                x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, 
                x1, y1+r, x1, y1)
        return master.create_polygon(points, **kwargs, smooth=True)

    def draw(self):
        '''Draw button on screen. 
        '''
        self.label = tk.Label(self.master, textvariable=self.labeltext)
        self.label.place(x = (self.kwargs['x1'] + self.kwargs['x2'])/2, y= (self.kwargs['y1'] + self.kwargs['y2'])/2, anchor='center')
        return self.round_rectangle(self.master, **self.kwargs)

    