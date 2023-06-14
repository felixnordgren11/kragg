import tkinter as tk
from settings import Settings
LEFT = -1
RIGHT = 1
Fact = True
Lie = False

# To do:
# Se till att digits behåller sin färg när man ändrar
# Lägg också till att den klarar att slå om från 0 till 9

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
        print(self.digit_tags)
    
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
        self.highlight(self.digit_tags[self.select_digit], self.is_active)
    
    def highlight(self, dgt, on = Fact):
        if on:
            self.label.tag_config(str(dgt), background = self.kwargs['active'], foreground = self.kwargs['bg'])
        else:
            self.label.tag_config(str(dgt), background = self.kwargs['bg'], foreground = self.kwargs['fg'])

    def move_select(self, direction: int):
        if not self.is_active:
            return
        new_select = self.select_digit + direction
        if new_select not in range(len(self.digit_tags)):
            return
        self.highlight(self.digit_tags[self.select_digit], Lie)
        self.highlight(self.digit_tags[new_select], Fact)
        self.select_digit = new_select

        
    def digit_change(self, value, dgt = None, hglt = Fact):
        # Fixa så den klara omslag vid 0.
        if dgt is None:
            dgt = self.select_digit
        current_tag = self.digit_tags[dgt]
        current_value = int(self.label.get(f"1.{current_tag}"))
        new_value = int(current_value) + value
        if current_value == 9:
            if current_tag == min(self.digit_tags):
                new_value = 9
            else:
                new_value = 0
                self.digit_change(value, dgt-1, hglt = Lie)

        self.label.delete(f"1.{current_tag}")
        self.label.insert(f"1.{current_tag}", str(new_value))
        self.label.tag_add(str(current_tag), f"1.{current_tag}", f"1.{current_tag + 1}")
        if hglt:
            self.highlight(current_tag)
        
        

    def get_active(self):          
        return self.is_active      
    
    #A function that updates the gauge:
    def update(self, value):
        self.labeltext.set(value)
        self.label.update()
        self.label.after(1000, self.update, value)







    
        
