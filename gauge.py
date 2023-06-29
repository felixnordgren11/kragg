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
        if 'max' in self.kwargs:
            self.max = float(self.kwargs['max'])
        else:
            self.max = 999.9
        self.select_digit = self.settings.default_digit
        self.digit_tags = list(range(0,len(self.gauge_format)))
        self.digit_tags.remove(self.gauge_format.index('.'))
        self.num_dec = len(self.gauge_format.split('.')[-1])
        #print(self.digit_tags)

    def draw(self):
        '''Draws the gauge on the screen.'''
        self.label = tk.Text(
                              self.master, 
                              bg = self.kwargs['bg'], fg = self.kwargs['fg'], 
                              font = self.kwargs['font'],
                              **self.settings.textsettings['gaugetext'], relief="flat",)
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
    def highlight(self, dgt: int, on = Fact):
        '''Highlights the digit currently active.
        colours defined in settings file'''
        if on:
            self.label.tag_config(str(dgt), background = self.kwargs['active'], foreground = self.kwargs['bg'])
        else:
            self.label.tag_config(str(dgt), background = self.kwargs['bg'], foreground = self.kwargs['fg'])
            
    
    
    @enable
    def move_select(self, direction: int):
        '''Function that moves highlight of the digits in the active gauge'''
        if not self.is_active:
            return
        new_select = self.select_digit + direction
        if new_select not in range(len(self.digit_tags)):
            return
        self.highlight(self.digit_tags[self.select_digit], Lie)
        self.highlight(self.digit_tags[new_select], Fact)
        self.select_digit = new_select

    @enable
    def digit_change(self, value: int, dgt = None, hglt = Fact, max = None):
        '''Changes the value of the digit at tag with index dgt.
        It also handles changing the digits in the rest of the 
        gauge through recursive calls to itself.'''
        if dgt is None:
            dgt = self.select_digit
        current_tag = self.digit_tags[dgt]
        current_value = int(self.label.get(f"1.{current_tag}"))
        new_value = int(current_value) + value
        # Logic handling the potential crossover at 9 and 0.
        if new_value == 10:
            if all([self.label.get(f'1.{d}') == '9' for i, d in enumerate(self.digit_tags) if i < dgt]):
                new_value = 9 
            else:
                new_value = 0 
                self.digit_change(value, dgt - 1, hglt = Lie)

        elif new_value == -1:
            if all([self.label.get(f'1.{d}')=='0' for i, d in enumerate(self.digit_tags) if i < dgt]):
                new_value = 0
                self.set_gauge(0)
            else:
                new_value = 9
                self.digit_change(value, dgt - 1, hglt = Lie)

        self.label['state'] = tk.NORMAL
        self.label.delete(f"1.{current_tag}")
        self.label.insert(f"1.{current_tag}", str(new_value))
        # Reset gauge if maximum or minimum is exceeded.
        self.check_limits()
        
        self.label.tag_add(str(current_tag), f"1.{current_tag}", f"1.{current_tag + 1}")
        if hglt:
            self.highlight(current_tag)
    
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
        output = float(self.label.get('1.0', 'end-1c').split()[0])
        return output
        
    @enable
    def set_gauge(self, value: float):
        '''Sets the given gauge to value.
        '''
        if value > self.max:
            value = self.max
        elif value < 0:
            value = 0
        value = round(value, self.num_dec)
        self.label.delete('1.0', f'1.{len(self.gauge_format)}')
        if not value:
            self.label.insert('1.0', self.gauge_format)
            return
        s = str(value).split('.')
        s[0] = '0'*(2 - len(s[0])) + s[0] 
        s[1] = s[1] + '0'*(2 - len(s[1]))  
        s = '.'.join(s)
        self.label.insert('1.0', s)

    def get_active(self) -> bool:    
        '''Returns True if the gauge is in active mode and
        is being edited by the user.
        '''      
        return self.is_active      