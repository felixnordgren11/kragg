import tkinter as tk
from settings import *

class Gauge:

    def __init__(self, master, label, **kwargs):
        '''Initializes a gauge to be placed in the gui.
        '''
        self.master  = master
        self.labeltext = label.upper()
        self.is_active = Lie
        self.kwargs = kwargs
        self.settings = Settings()
        self.gauge_format = self.settings.gauge_format
        self.display = self.gauge_format + ' ' + self.kwargs['unit']
        self.default_digit = self.settings.default_digit
        self.digit_tags = list(range(0,len(self.gauge_format)))
    
    def draw(self):
        '''Draws the gauge on the screen.'''
        self.label = tk.Text(self.master, 
                              bg = self.kwargs['bg'], fg = self.kwargs['fg'], 
                              font = self.kwargs['font'],
                              **self.settings.textsettings['gaugetext'], relief="flat")
        self.label.insert('1.0', self.display)
        self.label.place(x = (self.kwargs['a']), 
                         y = (self.kwargs['b']), 
                         anchor='nw')
        # Add labels
        for dgt in self.digit_tags:
            self.label.tag_add(str(dgt), f"1.{dgt}", f"1.{dgt + 1}")
        return self.label
    
    def set_active(self, value: bool):
        self.is_active = value
        if self.is_active:
            self.label.tag_config(str(self.default_digit), background = self.kwargs['fg'], foreground = self.kwargs['bg'])
        else:
            self.label.tag_config(str(self.default_digit), background = self.kwargs['bg'], foreground = self.kwargs['fg'])


    def get_active(self):          
        return self.is_active      
    
    #A function that updates the gauge:
    def update(self, value):
        self.labeltext.set(value)
        self.label.update()
        self.label.after(1000, self.update, value)







    
        
