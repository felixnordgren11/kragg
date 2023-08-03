import tkinter as tk
from settings import Settings
LEFT = -1
RIGHT = 1
Fact = True
Lie = False

# To do:
# Se till att digits behåller sin färg när man ändrar
# Lägg också till att den klarar att slå om från 0 till 9



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


class Gauge:
    '''
    Class that handles the gauges on the GUI
    '''

    def __init__(self, master, label, **kwargs):
        '''Initializes a gauge to be placed in the gui.
        '''
        # Canvas object from the GUI
        self.master  = master
        # The name of the gauge.
        self.labeltext = label.upper()
        self.is_active = Lie
        self.kwargs = kwargs
        self.settings = Settings()
        self.gauge_format = self.settings.gauge_format
        self.display = self.gauge_format + ' ' + self.kwargs['unit']
        self.value = 0

        if 'max' in self.kwargs:
            self.max = float(self.kwargs['max'])
        else:
            self.max = 999.9
            
        self.select_digit = self.settings.default_digit
        self.digit_tags = list(range(0,len(self.gauge_format)))
        self.digit_tags.remove(self.gauge_format.index('.'))
        self.num_dec = len(self.gauge_format.rsplit('.', maxsplit = 1)[-1])
        #print(self.digit_tags)

    def draw(self, text = None):
        '''Draws the gauge on the screen.'''
        if text is None:
            text = 'gaugetext'
        self.label = tk.Text(
                              self.master,
                              bg = self.kwargs['bg'], fg = self.kwargs['fg'],
                              font = self.kwargs['font'],
                              **self.settings.textsettings[text], relief="flat",)
        self.label.insert('1.0', self.display)
        self.label['state'] = tk.DISABLED
        self.label.place(x = (self.kwargs['a']),
                         y = (self.kwargs['b']),
                         anchor='nw')

        # Add labels
        for dgt in self.digit_tags:
            self.label.tag_add(str(dgt), f"1.{dgt}", f"1.{dgt + 1}")
        return self.label
    
    
    @enable
    def set_active(self, value: bool):
        '''Function that activates gauges'''
        self.is_active = value
        self.highlight(self.digit_tags[self.select_digit], self.is_active)

    
    
    @enable
    def highlight(self, dgt: int, on=Fact):
        '''Highlights the digit currently active.
        colours defined in settings file'''
        if on:
            self.label.tag_config(str(dgt), background=self.kwargs['active'], foreground=self.kwargs['bg'])
        else:
            self.label.tag_config(str(dgt), background=self.kwargs['bg'], foreground=self.kwargs['fg'])

            
    
    
    @enable
    def move_select(self, direction: int):
        '''Function that moves highlight of the digits in the active gauge'''
        # If the gauge is not selected, don't bother.
        if not self.is_active:
            return
        # Change in desired direction, either left or right.
        new_select = (self.select_digit + direction) % 4
        # Set new one highlighted and remove from old one.
        self.highlight(self.digit_tags[self.select_digit], Lie)
        self.highlight(self.digit_tags[new_select], Fact)
        # Change which digit is the currently selected one.
        self.select_digit = new_select

    
    def change_value(self, value: float):
        '''Changes the stored value in the gauge.
        '''
        self.value = self.value + value
        if self.value < 0:
            self.value = 0
        elif self.value > self.max:
            self.value = self.max
    
    def check_limits(self):
        '''This method checks if the gauge has passed its maximum
        values. If that is the case, it resets the gauge to the limits. 
        '''
        if (self.get_value() >= self.max):
            self.set_gauge(self.max)
            for dgt in self.digit_tags:
                self.label.tag_add(str(dgt), f"1.{dgt}", f"1.{dgt + 1}")
        elif self.get_value() == 0:
            for dgt in self.digit_tags:
                self.label.tag_add(str(dgt), f"1.{dgt}", f"1.{dgt + 1}")
    
    @enable
    def get_value(self) -> float:
        '''Returns the displayed value of the gauge
        '''
        return self.value
        
    @enable
    def set_gauge(self, value: float, rounding = None):
        '''Sets the given gauge to value.
        '''
        self.value = value
        # Begin by setting this to false
        if type(value) is not float:
            value = float(value)
        large = Lie
        # If no specific rounding is given.
        if rounding is None:
            rounding = self.num_dec
        # If outside of bounds.
        if value > self.max:
            value = self.max
        elif value < 0:
            value = 0
        # If larger than 99.99 it can only have one decimal.
        if value > 99.99:
            rounding = 1
            large = Fact
        value = round(value, rounding)
        # Remove previous value.
        self.label.delete('1.0', f'1.{len(self.gauge_format)}')
        # If zero, insert the given standard format (00.00)
        if not value:
            self.label.insert('1.0', self.gauge_format)
        else:
            # If not large (> 99.99), insert zeros to fill out.
            if not large:
                s = str(value).split('.')
                s[0] = '0'*(2 - len(s[0])) + s[0]
                s[1] = s[1] + '0'*(2 - len(s[1]))
                s = '.'.join(s)
            else:
                # Otherwise just take the value as is.
                s = str(value)
            self.label.insert('1.0', s)
        # Restore tags.
        for dgt in self.digit_tags:
                self.label.tag_add(str(dgt), f"1.{dgt}", f"1.{dgt + 1}")

    def get_active(self) -> bool:    
        '''Returns True if the gauge is in active mode and
        is being edited by the user.
        '''      
        return self.is_active     
    
    def refresh(self):
        '''Refreshes the gauge to match the latest
        set value.
        '''
        if self.get_active():
            self.set_gauge(self.value)
