''' Here some code will be written,
NAWRAHL CABON BRAINWOW

Tanke: Gör loading_screen till init.
Hur : Gör en canvas till loading screenen där allt som har med den att göra händer.
      Efter allt är färdigt, ta bord den canvasen (canvas.destroy()) och skapa den 
      vanliga som det redan finns kod för.
'''
import tkinter as tk
import sys
import os
import numpy as np
from tkinter import messagebox
from tkinter import ttk
from button import Button
from gauge import Gauge, LEFT, RIGHT
from rpi import RPI, WRITE, READ
from time import sleep, time
from settings import *

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
        
        # Our Tk objects
        self.canvas = tk.Canvas(self.root, **self.settings.canvassettings)
        self.canvas.pack()
        # Start in disabled mode.
        self.mode = 'disable'

        # Instantiate RPI class which initializes all pins etc.
        self.rpi = RPI(self)
            
    def _graphics(self):
        '''Draws the GUI's visual components.
        '''
        # Here all graphical objects will be drawn.
        
                
        # Define our buttons.
        self.btns = {}
        for label, btn in self.settings.buttonsettings.items():
            self.btns[label] = Button(self.canvas, label, **btn)

        # Define our gauges.
        self.gges = {}
        for label, gge in self.settings.gaugesettings.items():
            self.gges[label] = Gauge(self.canvas, label, **gge)

        
        
        self.canvas.grab_set()
        self.root.title(self.settings.title)
        self.root.geometry(self.settings.geometry)
        self.root.attributes('-fullscreen', True)

        # Bind keyboard events
        self.root.bind_all("<Key>", self.key)

        # Bind mouse events
        self.root.bind_all("<Button-1>", self.callback)
        self.canvas.focus_set()
        self.canvas.config(cursor = 'none')
        self._draw_border()

        # Draw the buttons.
        for btn in self.btns.values():
            btn.draw()
        # Select the active button.
        self.btns[self.mode].selected(Fact)
        
        # Draw the gauges.
        for gge in self.gges.values():
            gge.draw()
        
        self.root.update()
        
    def _graphics_calibration(self):
        '''Draws the GUI's visual components.
        '''
        # Here all graphical objects will be drawn.
        
        self.canvas.grab_set()
        self.root.cal_title(self.settings.cal_title)
        self.root.geometry(self.settings.geometry)
        self.root.attributes('-fullscreen', True)

        # Bind keyboard events
        self.root.bind_all("<Key>", self.key)

        # Bind mouse events
        self.root.bind_all("<Button-1>", self.callback)
        self.canvas.focus_set()
        self.canvas.config(cursor = 'none')
        self._draw_border()
        
        # Draw the gauge.
        for gge in self.gges.values():
            gge.draw()
        
        self.root.update()
        
    def _clear_all(self):
        for item in canvas.winfo_children():
            item.destroy()

    def _hardware(self):
        '''Initializes the Raspberry Pi and the power unit.
        '''
        # Send command to init the can communication, then wait 100ms
        os.system(self.settings.can_init_command)
        sleep(0.1)
        # Send appropriate commands to the power unit.
        self._init_power_unit()
        
    def _draw_border(self):
        '''Function that draws the border around the GUI,
        Some values could possibly be given as arguments.
        '''
        self._round_rectangle(self.canvas, self.settings.width*0.05, self.settings.height*0.05, 
                             self.settings.width*0.95, self.settings.height*0.98, outline = self.settings.border_color, width = 2, activewidth = 4, fill = '')
        self._round_rectangle(self.canvas, self.settings.width*0.05, self.settings.height*0.05, 
                             self.settings.width*0.95, self.settings.height*0.12, outline = self.settings.border_color, width = 2, fill = self.settings.border_color)
        self.canvas.create_rectangle(self.settings.width*0.05, self.settings.height*0.1, 
                             self.settings.width*0.95, self.settings.height*0.15, outline = '', fill = self.settings.border_color)  
        self.canvas.create_text(self.settings.width*0.5, self.settings.height*0.1, text = self.settings.title, font = ('Small Fonts', 20), fill = 'black')  


    def _init_power_unit(self):
        '''Sends necessary commands to the power unit
        to set into configurable mode (test mode)
        '''
        # We want to set the power unit into test mode. 
        command = self.settings.command_lib['test_mode']
        reply = self.rpi.send_msg(WRITE, command, value = 1)
        sleep(1)
        self.rpi.send_msg(WRITE, self.settings.command_lib['v_set'], value = 0)
        self.rpi.send_msg(WRITE, self.settings.command_lib['i_set'], value = 0)
        sleep(0.5)
        self.root.after(self.settings.update_speed, self._update_value)

    def _round_rectangle(self, master, x1, y1, x2, y2, r=25, **kwargs):  
        '''Helper function that can draw rounded objects.
        '''  
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r,
                x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2,
                x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, 
                x1, y1+r, x1, y1)
        return master.create_polygon(points, **kwargs, smooth=True)


    def calibration_procedure(self):
        # Check if calibration
        start = time()
        start_cal = Lie
        while (not self.rpi.pin_v.is_pressed and not self.rpi.pin_i.is_pressed):
                if time() - start > 3:
                    start_cal = Fact
                    messagebox.showinfo('Calibration', "Calibration started.")
                    break
        if not start_cal:
            return
        amps = np.array([0, 5, 10, 15])
        vlts = np.array([i for i in range(5,self.settings.max_v, 5)])
        measurements = []
        for i in amps:
            measurements.append(np.array(self.voltage_curvefit(i)))
        dv, offset = np.polyfit(vlts, np.array(100*vlts - measurements[0]), 1)
        print(measurements)
        i_m = [[100*vlts[i] - v_m[i] for v_m in measurements] for i in range(len(vlts))]
        di_tot = 0
        di = 0 
        for i in range(len(vlts)):
            di, _ = np.polyfit(amps, i_m[i], 1)
            di_tot = di_tot + di
        di_tot = di_tot/len(vlts)

        # Now write to cal file
        name = self.settings.cal_file
        with open(name, 'w') as file:
            lines = [f"offset:{offset}\n",
                     f"v:{dv}\n",
                     f"i:{di}\n"]
            file.writelines(lines)


        
    def voltage_curvefit(self, current):
        self.rpi.send_msg(WRITE, self.settings.command_lib['i_set'], value = 20)
        self.rpi.send_msg(WRITE, self.settings.command_lib['v_set'], value = 5)
        messagebox.showinfo('Calibration', f"Set load to {int(current)}A")

        # Measure at 5, 10, 15, 20, 25 volts.
        vlts = np.array([i for i in range(5,self.settings.max_v, 5)])
        # Start by setting current limit to non zero value.
        self.rpi.send_msg(WRITE, self.settings.command_lib['i_set'], value = current + 1)
        # Wait for curr to adapt
        # Set a voltage output just to be able to read current
        while (abs(self.rpi.send_msg(READ, self.settings.command_lib['i_read']) - current*100) > CURR_OFF):
            print(self.rpi.send_msg(READ, self.settings.command_lib['i_read']))
            sleep(0.2)
        v_m = np.array([0 for i in vlts])
        for i, v in enumerate(vlts):
            self.rpi.send_msg(WRITE, self.settings.command_lib['v_set'], value = v)
            # Wait for voltage to reach setpoint
            sleep(5)
            # Measured voltage in centivolts.
            meas_v = self.rpi.send_msg(READ, self.settings.command_lib['v_read'])
            v_m[i] = meas_v
        # Lower the voltage again.
        self.rpi.send_msg(WRITE, self.settings.command_lib['v_set'], value = 0)
     
        return v_m

##################################################################################
#                        RUNS CONTINUOUSLY

    def _update_value(self):
        '''Helper function that computes the measured output power.
            '''
        if (not self.rpi.pin_v.is_pressed and not self.rpi.pin_i.is_pressed):
            self.calibration_procedure()
            
        # Send v_read a
        v_value, i_value = self.rpi.send_msg(
            READ, self.settings.command_lib['v_read']), self.rpi.send_msg(READ, self.settings.command_lib['i_read'])
        # Adjust measurement
        #######################
        v_value = v_value + (self.settings.calibration['offset'] + 
                             self.settings.calibration['i']*(i_value/100) + 
                             self.settings.calibration['v']*(v_value/100))
        #######################
        self.gges['v_out'].set_gauge(v_value/100)
        self.gges['i_out'].set_gauge(i_value/100)

        # Update power gauge
        v = self.gges['v_out'].get_value()
        i = self.gges['i_out'].get_value()
    

        # Set power gauge.
        self.gges['p'].set_gauge(i*v)

        # Refresh gauges
        for gauge in self.gges.values():
            gauge.refresh()


        # Set to update again in 200ms 
        self.root.after(self.settings.update_speed, self._update_value)
            
##################################################################################


    def select_gauge(self, m: str):
        '''Selects a gauge so that it can be configured
        and thereby changing output reference values for the
        PSU.
        '''
        
        if (not self.rpi.pin_v.is_pressed and not self.rpi.pin_i.is_pressed):
            # Calibration
            print("Cal!")
            return
        # Which is the gauge we have selected. The other one is to be deactivated.
        sel,notsel = ('v_set','i_set') if m == 'v' else ('i_set','v_set')
        sel_active = self.gges[sel].get_active()

        if self.gges[notsel].get_active():
            # Means value was confirmed.
            self.gges[notsel].set_active(Lie)
            # Send the selected value if device is enabled.
            if self.mode != 'disable':
                self.rpi.send_msg(WRITE, self.settings.command_lib[notsel], self.gges[notsel].get_value())
        # If the selected gauge is active, the press meant to confirm the configuration
        elif sel_active:
            # Means we are confirming.
            if self.mode != 'disable':
                self.rpi.send_msg(WRITE, self.settings.command_lib[sel], self.gges[sel].get_value())
        self.gges[sel].set_active(not sel_active)

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
            sys.exit()
        
        elif event.char == 'c':
            self._clear_all()

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
        def inside_btn(x, y, btn):
            inside_in_x = x > btn.kwargs['x1'] and x < btn.kwargs['x2']
            inside_in_y = y > btn.kwargs['y1'] and y < btn.kwargs['y2']
            is_inside = inside_in_x and inside_in_y
            return is_inside
                
        # Check if one of boxes are clicked.
        # First check that any of boxes is selected:
        if not any(inside_btn(x,y,btn) for btn in self.btns.values()):
            return
            
        for mode, btn in self.btns.items():
            if inside_btn(x, y, btn):
                # If inside, button has been clicked: set corresponding mode. 
                self.mode = mode
                # Show button as selected.
                btn.selected(Fact)
                if mode == 'enable':
                    self.set_current_out()
                elif mode == 'disable':
                    # Disable output.
                    self.rpi.send_msg(WRITE, self.settings.command_lib['v_set'], value = 0)
            else:
                btn.selected(Lie)

    # Add a line that runs the power function every 200 ms:

    def _init(self, root):
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
        processes = [
            {'process' : 'Hardware initializing', 'func' : self._hardware, 'progress' : 50},
            {'process' : 'Secret stuff initializing', 'func' : self._dummy, 'progress' : 50}
        ]
        for process in processes:
            label.config(text=f"{process['process']}... {int(progressbar['value'])}%")
            loading_window.update_idletasks()  # Update the loading window
            sleep(1)  # Simulating a small delay between updates
            # Run the process
            try:
                process['func']()
            except Exception as e:
                print(f'Process "{process["process"]}" failed with the following exception: {e}')
            #
            progressbar['value'] += process['progress'] 
            label.config(text=f"{process['process']}... {int(progressbar['value'])}%")
            loading_window.update_idletasks()  # Update the loading window
            sleep(1)
        loading_window.destroy()
        root.deiconify()
   

    def _dummy(self):
        pass

    def run(self):
        self._graphics()
        self.root.after(200, lambda: self._init(self.root))
        self.root.mainloop()

if '__main__' == __name__:

    gui = GUI()  
    gui.run()