import tkinter as tk
from settings import Settings
LEFT = -1
RIGHT = 1
Fact = True
Lie = False



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
        self.select_digit = self.settings.default_digit
        self.digit_tags = list(range(0,len(self.gauge_format)))
        self.digit_tags.remove(self.gauge_format.index('.'))
    
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
        self.highlight(self.select_digit, self.is_active)
    
    def highlight(self, dgt, on = Fact):
        if on:
            self.label.tag_config(str(dgt), background = self.kwargs['active'], foreground = self.kwargs['bg'])
        else:
            self.label.tag_config(str(dgt), background = self.kwargs['bg'], foreground = self.kwargs['fg'])
        return dgt

    def move_select(self, direction: int):
        if not self.is_active:
            return
        new_select = self.select_digit + direction
        if new_select not in self.digit_tags:
            return
        self.highlight(self.select_digit, Lie)
        self.select_digit = self.highlight(new_select, Fact)

        
        
        

    def get_active(self):          
        return self.is_active      
    
    #A function that updates the gauge:
    def update(self, value):
        self.labeltext.set(value)
        self.label.update()
        self.label.after(1000, self.update, value)







    
        
