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
    
    def __init__(self, master, **kwargs):
        '''Instantiates the prompt
        '''
        self.master = master
        self.kwargs = kwargs
        self.settings = Settings()
        self.icon = None
    
    def set_text(self, text):
        ''' Updates the label text
        '''
        self._clear()
        self._insert(text)

    def _clear(self):
        '''Clears text'''
        self.label.delete("1.0","end")

    def _insert(self, text):
        '''Inserts provided text'''
        self.label.insert("1.0", text)

    def draw_prompt(self):
        '''
        Draw promptv  
        '''
        promptkwargs = self.settings.textsettings['prompttext']
        x = (self.kwargs['x1'] + self.kwargs['x2'])/2
        y = (self.kwargs['y1'] + self.kwargs['y2'])/2
        self.icon = self.master.create_rectangle(self.kwargs['x1'], self.kwargs['y1'], self.kwargs['x2'], self.kwargs['y2'], fill = self.kwargs['fill'])
        self.label = tk.Text(self.master, **promptkwargs)
        self.label.place(x = x, y = y, anchor = 'center')
        return self.icon

    
    


