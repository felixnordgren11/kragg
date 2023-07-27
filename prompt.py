import tkinter as tk
from settings import Settings
LEFT = -1
RIGHT = 1
Fact = True
Lie = False

def enable(func):
    '''Decorator that returns the same function
    only that the label of a Gauge object is activated
    before execution and deactivated after.
    '''
    def wrapper(self, *args, **kwargs):
        self.label['state'] = tk.NORMAL
        var = func(self, *args, **kwargs)
        self.label['state'] = tk.DISABLED
        return var
    return wrapper

class Prompt:
    '''
    Class that handles the prompt in calibration mode
    '''
    
    def __init__(self, master, label, **kwargs):
        '''Instantiates the prompt
        '''
        self.master = master
        self.kwargs = kwargs
        self.labeltext = label
        self.settings = Settings()
        self.icon = None
        
    def create_rectangle(self, master, x1, y1, x2, y2, **kwargs)
        '''
        Draws a rectangle
        '''
        points = (x1,y1,x2,y2)
        return master.create_polygon(points, **kwargs, smooth=True)
    
    def set_text(self, text_in)
        self.master.itemconfig(self.label, text = text_in)
        
    def draw_prompt(self):
        '''
        Draw prompt
        '''
        promptkwargs = self.settings.textsettings['prompttext']
        x = (self.kwargs['x1'] + self.kwargs['x2'])/2
        y = (self.kwargs['y1'] + self.kwargs['y2'])/2
        self.icon = self.create_rectangle(**self.kwargs)
        self.label = self.master.create_text(x, y, anchor='center', text = '', **promptkwargs)
        return self.icon
    
    
    


