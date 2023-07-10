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
        
    def round_rectangle(self, master, x_1, y_1, x_2, y_2, r=25, **kwargs):   
        '''
        Draws a rectangle with rounded corners.
        '''
        points = (x_1+r, y_1, x_1+r, y_1, x_2-r, y_1, x_2-r, y_1, x_2, y_1, x_2, y_1+r,
                x_2, y_1+r, x_2, y_2-r, x_2, y_2-r, x_2, y_2, x_2-r, y_2, x_2-r, y_2,
                x_1+r, y_2, x_1+r, y_2, x_1, y_2, x_1, y_2-r, x_1, y_2-r, x_1, y_1+r, 
                x_1, y_1+r, x_1, y_1)
        return master.create_polygon(points, **kwargs, smooth=True)
    
    def draw(self):
        '''
        Draw button on screen. 
        '''
        btnkwargs = self.settings.textsettings['buttontext']
        x = (self.kwargs['x_1'] + self.kwargs['x_2'])/2
        y = (self.kwargs['y_1'] + self.kwargs['y_2'])/2
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
