import tkinter as tk
from settings import *


class Button:
    '''
    Class used to handle buttons in the GUI
    '''

    def __init__(self, master, label, **kwargs):
        '''Instantiates the button according to the given data
        '''
        self.master = master
        self.kwargs = kwargs
        self.labeltext = label
        self.settings = Settings()
        # Selected variable
        self.icon = None
        self.is_selected = Lie
        
    def round_rectangle(self, master, x1, y1, x2, y2, r=25, **kwargs):   
        '''
        Draws a rectangle with rounded corners.
        '''
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r,
                x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2,
                x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, 
                x1, y1+r, x1, y1)
        return master.create_polygon(points, **kwargs, smooth=True)
    
    def draw(self):
        '''
        Draw button on screen. 
        '''
        btnkwargs = self.settings.textsettings['buttontext']
        x = (self.kwargs['x1'] + self.kwargs['x2'])/2
        y = (self.kwargs['y1'] + self.kwargs['y2'])/2
        self.icon = self.round_rectangle(self.master, **self.kwargs)
        self.label = self.master.create_text(x, y, anchor='center', text = self.labeltext.upper(), **btnkwargs)
        return self.icon
    
    def selected(self, mode):
        '''
        Function that shows when a button is selected and active
        '''
        if mode:
            self.master.itemconfig(self.icon, fill = self.kwargs['outline'])
        else:
            self.master.itemconfig(self.icon, fill = 'black')
        self.is_selected = mode
        return self.is_selected
