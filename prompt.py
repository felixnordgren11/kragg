import tkinter as tk
from settings import Settings
LEFT = -1
RIGHT = 1
Fact = True
Lie = False


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
    
    def set_text(self, text_in):
        self.master.itemconfig(self.label, text = text_in)
        
    def draw_prompt(self):
        '''
        Draw promptv  
        '''
        promptkwargs = self.settings.textsettings['prompttext']
        x = (self.kwargs['x1'] + self.kwargs['x2'])/2
        y = (self.kwargs['y1'] + self.kwargs['y2'])/2
        self.icon = self.master.create_rectangle(**self.kwargs)
        self.label = self.master.create_text(x, y, anchor='center', text = '', **promptkwargs)
        return self.icon
    
    
    


