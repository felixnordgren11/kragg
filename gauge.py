import tkinter as tk
from settings import *

class Gauge:

    def __init__(self, master, label, **kwargs):
        '''Initializes a gauge to be placed in the gui.
        '''
        self.master  = master
        self.labeltext = label.upper()
        self.kwargs = kwargs
        self.settings = Settings()
        
    
    def draw(self):
        '''Draws the gauge on the screen.'''
        self.label = tk.Text(self.master, bg = self.kwargs['bg'], fg = self.kwargs['fg'], 
                              font = self.kwargs['font'],
                              **self.settings.textsettings['gaugetext'], relief='flat')
        
        self.label.insert('0.0', self.labeltext)
        self.label.place(x = (self.kwargs['a']), 
                         y = (self.kwargs['b']), 
                         anchor='nw')
        return self.label
    
    
    #A function that updates the gauge:
    def update(self, value):
        self.labeltext.set(value)
        self.label.update()
        self.label.after(1000, self.update, value)
    pass





    
        
