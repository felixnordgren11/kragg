''' Here some code will be written,
NAWRAHL CABON BRAINWOW

Tanke: Gör loading_screen till init.
Hur : Gör en canvas till loading screenen där allt som har med den att göra händer.
      Efter allt är färdigt, ta bord den canvasen (canvas.destroy()) och skapa den 
      vanliga som det redan finns kod för.
'''
import tkinter as tk
import os
from tkinter import ttk
from settings import *
from button import Button
from gauge import Gauge, LEFT, RIGHT
from rpi import RPI, WRITE, READ
from time import sleep
#import ctypes

Fact = True
Lie  = False

'''
To do:
Remove unused files and incorporate reading of the gauges at 
timed intervals.
Also, add a "485-init"-method or something like it. It will act as
'''

class GUI:
    '''
    Our main class
    '''
    def __init__(self):
        '''Initializes variables'''
        # This is our window.
        self.root = tk.Tk()
        self.loaded = Lie
        self.settings = Settings()

    def graphics(self):
        '''Draws the GUI's visual components.
        '''
        # Here all graphical objects will be drawn.
        self.canvas = tk.Canvas(self.root, **self.settings.canvassettings)
        self.canvas.pack()
        self.canvas.grab_set()
        self.root.title(self.settings.title)
        self.root.geometry(self.settings.geometry)
        self.root.attributes('-fullscreen', True)
        '''photo = tk.PhotoImage(file = "iconphoto.png")
        self.root.iconphoto(False, photo)'''
        # Initialize as disabled. Otherwise it will start with an output voltage neq 0.
        self.mode = 'disable'
        # Bind keyboard events
        self.root.bind_all("<Key>", self.key)
        # Bind mouse events
        self.root.bind_all("<Button-1>", self.callback)
        self.is_active = Lie
        self.canvas.focus_set() 
        self.canvas.config(cursor = 'none')
        self.draw_border()
        
        # Loop through the button settings dictionary and create the specified
        # buttons. After that they are drawn using the draw() method.
        
        self.btns = {}
        for label, btn in self.settings.buttonsettings.items():
            self.btns[label] = Button(self.canvas, label, **btn)
            self.btns[label].draw()
        self.btns[self.mode].selected(Fact)
        
        # Loop through the gauge settings dictionary we created in the settings.py file.
        # For each gauge, we create a Gauge object and store it in the gges dictionary.
        # Call the draw() method to draw the gauge.
        self.gges = {}
        for label, gge in self.settings.gaugesettings.items():
            self.gges[label] = Gauge(self.canvas, label, **gge)
            self.gges[label].draw()
        
        self.root.update()

    def hardware(self):
        '''Initializes the Raspberry Pi and the power unit.
        '''
        # Send command to init the can communication, then wait 100ms
        os.system(self.settings.can_init_command)
        sleep(0.1)
        # Instantiate RPI class which initializes all pins etc.
        self.rpi = RPI(self)
        # Send appropriate commands to the power unit.
        self.init_power_unit()
        
    def draw_border(self):
        '''Function that draws the border around the GUI,
        Some values could possibly be given as arguments.
        '''
        self.round_rectangle(self.canvas, self.settings.width*0.05, self.settings.height*0.05, 
                             self.settings.width*0.95, self.settings.height*0.98, outline = self.settings.border_color, width = 2, activewidth = 4, fill = '')
        self.round_rectangle(self.canvas, self.settings.width*0.05, self.settings.height*0.05, 
                             self.settings.width*0.95, self.settings.height*0.12, outline = self.settings.border_color, width = 2, fill = self.settings.border_color)
        self.canvas.create_rectangle(self.settings.width*0.05, self.settings.height*0.1, 
                             self.settings.width*0.95, self.settings.height*0.15, outline = '', fill = self.settings.border_color)  
        self.canvas.create_text(self.settings.width*0.5, self.settings.height*0.1, text = 'Neanderball', font = ('Small Fonts', 20), fill = 'black')  


    def init_power_unit(self):
        '''Sends necessary commands to the power unit
        to set into configurable mode (test mode)
        '''
        # We want to set the power unit into test mode. 
        command = self.settings.command_lib['test_mode']
        reply = self.rpi.send_msg(WRITE, command, value = 1)
        sleep(1)
        self.root.after(200, self.update_value)
        self.rpi.send_msg(WRITE, self.settings.command_lib['v_set'], value = 0)
        

    def round_rectangle(self, master, x1, y1, x2, y2, r=25, **kwargs):  
        '''Helper function that can draw rounded objects.
        '''  
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r,
                x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2,
                x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, 
                x1, y1+r, x1, y1)
        return master.create_polygon(points, **kwargs, smooth=True)

##################################################################################
#                        RUNS CONTINUOUSLY


    def update_value(self):
            '''Helper function that computes the measured output power.
            '''

            # Send v_read a
            v_value, i_value = self.rpi.send_msg(
                READ, self.settings.command_lib['v_read']), self.rpi.send_msg(READ, self.settings.command_lib['i_read'])
            self.gges['v_out'].set_gauge(v_value/100)
            self.gges['i_out'].set_gauge(i_value/100)

            # Update power gauge
            v = self.gges['v_out'].get_value()
            i = self.gges['i_out'].get_value()
            self.gges['p'].set_gauge(i*v, rounding = 2)

            self.root.after(self.settings.update_speed, self.update_value)
            
##################################################################################


    def select_gauge(self, m: str):
        '''Selects a gauge so that it can be configured
        and thereby changing output reference values for the
        PSU.
        '''
        # Which is the gauge we have selected. The other one is to be deactivated.
        sel,notsel = ('v_set','i_set') if m == 'v' else ('i_set','v_set')

        if self.gges[notsel].get_active():
            # Means value was confirmed.
            self.gges[notsel].set_active(Lie)
            # Send the selected value if device is enabled.
            if self.mode == 'enable':
                self.rpi.send_msg(WRITE, self.settings.command_lib[notsel], self.gges[notsel].get_value())
        # If the selected gauge is active, the press meant to confirm the configuration
        are_active = self.gges[sel].get_active()
        if are_active:
            # Means we are confirming.
            if self.mode == 'enable':
                self.rpi.send_msg(WRITE, self.settings.command_lib[sel], self.gges[sel].get_value())
        self.gges[sel].set_active(not are_active)

    def move_pointer(self, m: str) -> None:
        '''Updates the position of the pointer/cursor in the 
        selected gauge. Goes in the direction dictated by
        the values set in the settings file.
        '''
        self.gges['v_set'].move_select(self.settings.moves[m])
        self.gges['i_set'].move_select(self.settings.moves[m])

    def key(self, event:tk.Event):
        '''This function is used to operate the GUI from a PC
        '''
        print(event)
        if event.char == 'q':
             quit()

        elif event.char in ['v','i']:
            self.select_gauge(event.char)
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
        
    
    def set_current_out(self):
        '''Sets the current output values.
        '''
        self.rpi.send_msg(WRITE, self.settings.command_lib['v_set'], self.gges['v_set'].get_value())
        self.rpi.send_msg(WRITE, self.settings.command_lib['i_set'], self.gges['i_set'].get_value())



    def callback(self, event):
            '''Handles all left-mouse-click events.
            '''
            x, y = event.x, event.y
            # Helper function
            inside_btn = lambda x, y, btn: (x > btn.kwargs['x1'] and x < btn.kwargs['x2']) and (y > btn.kwargs['y1'] and y < btn.kwargs['y2']) 
            # Check if one of boxes are clicked.
            # First check that any of boxes is selected:
            if not any([inside_btn(x,y,btn) for btn in self.btns.values()]):
                 return 
            
            for mode, btn in self.btns.items():
                if inside_btn(x, y, btn):
                     self.mode = mode
                     print(mode)
                     btn.selected(Fact)
                     if mode == 'enable':
                         self.set_current_out()
                     elif mode == 'disable':
                         self.rpi.send_msg(WRITE, self.settings.command_lib['v_set'], value = 0)
                else:
                     btn.selected(Lie)

    # Add a line that runs the power function every 200 ms:

    def init(self, root):
        '''Initializes the hardware one the Raspberry Pi
        '''
        loading_window = tk.Toplevel()
        loading_window.title("Loading...")
        loading_window.geometry(f"250x250+{'+'.join(map(lambda x: str(int(0.25*int(x))), self.settings.geometry.split('x')))}")
        
        label = tk.Label(loading_window, text="Loading... 0%", font=("Arial", 12))
        label.pack(pady=20)
        
        progressbar = ttk.Progressbar(loading_window, length=150, mode="determinate")
        progressbar.pack(pady=10)
        
        loading_window.transient(root)
        loading_window.grab_set()
        root.update()
        
        # Simulate some loading process and update the progress bar
        # Here is the loading process
        import time
        processes = [
            {'process' : 'Hardware initializing', 'func' : self.hardware, 'progress' : 50},
            {'process' : 'Dickmas initializing', 'func' : self.dummy, 'progress' : 50}
        ]
        for process in processes:
            label.config(text=f"{process['process']}... {int(progressbar['value'])}%")
            loading_window.update_idletasks()  # Update the loading window
            time.sleep(1)  # Simulating a small delay between updates
            # Run the process
            try:
                process['func']()
            except Exception as e:
                print(f'Process "{process["process"]}" failed with the following exception: {e}')
            #
            progressbar['value'] += process['progress'] 
            label.config(text=f"{process['process']}... {int(progressbar['value'])}%")
            loading_window.update_idletasks()  # Update the loading window
            time.sleep(1)
        loading_window.destroy()
        root.deiconify()
   

    def dummy(self):
        pass

    def run(self):
        self.graphics()
        self.root.after(200, lambda: self.init(self.root))
        self.root.mainloop()

if '__main__' == __name__:

    gui = GUI()
    gui.run()