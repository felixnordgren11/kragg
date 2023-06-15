''' Here some code will be written,
NAWRAHL CABON BRAINWOW

Tanke: Ta bort postion från gaugesettings så att allt bara är text. 

'''
import tkinter as tk
from settings import *
from button import Button
from gauge import Gauge, LEFT, RIGHT


class GUI:
    '''
    Our main class
    '''
    
    
    
    def __init__(self):
        '''Initializes variables'''

        self.root = tk.Tk()
        self.settings = Settings()
        self.canvas = tk.Canvas(self.root, **self.settings.canvassettings)
        self.canvas.pack()
        self.root.title(self.settings.title)
        self.root.geometry(self.settings.geometry)
        

        # Bind click events

        self.root.bind_all("<Key>", self.key)
        self.root.bind_all("<Button-1>", self.callback)
        self.is_active = Lie
        self.canvas.focus_set() 
        self.draw_border()
        
        #Enable buttons
        
        self.btns = {}
        for label, btn in self.settings.buttonsettings.items():
            self.btns[label] = Button(self.canvas, label, **btn)
            self.btns[label].draw()
            
        # Loop through the gauge settings dictionary we created in the settings.py file.
        # For each gauge, we create a Gauge object and store it in the gges dictionary.
        # Call the draw() method to draw the gauge.
        
        self.gges = {}
        for label, gge in self.settings.gaugesettings.items():
            self.gges[label] = Gauge(self.canvas, label, **gge)
            self.gges[label].draw()
            

        #Mock output values    
        self.gges['v_out'].set_gauge(5.00)
        self.gges['i_out'].set_gauge(3.00)


    #Function that draws the border of the screen.
    #Rounded rectangle for the border. 
    #Create rectangle for the title box. 
    #Create text for the title
    def draw_border(self):

        self.round_rectangle(self.canvas, self.settings.width*0.05, self.settings.height*0.05, 
                             self.settings.width*0.95, self.settings.height*0.98, outline = self.settings.border_color, width = 2, activewidth = 4)
        self.round_rectangle(self.canvas, self.settings.width*0.05, self.settings.height*0.05, 
                             self.settings.width*0.95, self.settings.height*0.12, outline = self.settings.border_color, width = 2, fill = self.settings.border_color)
        self.canvas.create_rectangle(self.settings.width*0.05, self.settings.height*0.1, 
                             self.settings.width*0.95, self.settings.height*0.15, outline = '', fill = self.settings.border_color)  
        ##
        self.canvas.create_text(self.settings.width*0.5, self.settings.height*0.1, text = 'Neanderball', font = ('Small Fonts', 20), fill = 'black')  
    

    
    #Define the round rectangle function
    
    def round_rectangle(self, master, x1, y1, x2, y2, r=25, **kwargs):    
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r,
                x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2,
                x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, 
                x1, y1+r, x1, y1)
        return master.create_polygon(points, **kwargs, smooth=True)
    
    
    
    
    #Activate the gauge when pressing a button:
    
    def power_value(self):
            v = self.gges['v_out'].get_value()
            i = self.gges['i_out'].get_value()
            self.gges['p'].set_gauge(i*v)
            
    

    
    def key(self, event:tk.Event):
        #When either v or i is pressed, switch the active gauge to that and deactivate the other one
        if event.char in ['v','i']:
            sel,notsel = ('v_set','i_set') if event.char == 'v' else ('i_set','v_set')
            if not isinstance(self.gges[notsel], Gauge):
                raise TypeError("Expected type Gauge for %s, but got %s instead."%(notsel,type(self.gges[notsel])))
            if self.gges[notsel].get_active():
                self.gges[notsel].set_active(Lie)
            are_active = self.gges[sel].get_active()
            self.gges[sel].set_active(not are_active)
            return
        
        
        #Bind left and right key buttons to move the active digit in the active gauge
        if event.keysym in ['Left','Right']:
            self.gges['v_set'].move_select(self.settings.moves[event.keysym])
            self.gges['i_set'].move_select(self.settings.moves[event.keysym])

        #Bind up and down to increase/decrease the active digit in the active gauge.
        if event.keysym in ['Up','Down'] and (self.gges['v_set'].get_active() or self.gges['i_set'].get_active()):
            value = 1 if event.keysym == 'Up' else -1
            if self.gges['v_set'].get_active():
                self.gges['v_set'].digit_change(value)
            elif self.gges['i_set'].get_active():
                self.gges['i_set'].digit_change(value)
        
    
    def callback(self, event):
            x, y = event.x, event.y
            # Helper function
            inside_btn = lambda x, y, btn: (x > btn.kwargs['x1'] and x < btn.kwargs['x2']) and (y > btn.kwargs['y1'] and y < btn.kwargs['y2']) 
            # Check if one of boxes are clicked.
            # First check that any of boxes is selected:
            if not any([inside_btn(x,y,btn) for btn in self.btns.values()]):
                 return 
            
            for btn in self.btns.values():
                if inside_btn(x, y, btn):
                     btn.selected(Fact)
                else:
                     btn.selected(Lie)

    # Add a line that runs the power function every 200 ms:

    def run(self):
        self.root.after(200, self.power_value)
        self.root.mainloop()
        
        pass
    
    
    
        


if '__main__' == __name__:

    gui = GUI()
    gui.run()
 
