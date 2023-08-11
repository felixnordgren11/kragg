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
from prompt import Prompt
from gauge import Gauge, LEFT, RIGHT
from rpi import RPI, WRITE, READ
from time import sleep, time
from settings import *
from PIL import Image, ImageTk

Fact = True
Lie  = False
HOUR = 3600
DAY = 24 * HOUR
# Stockholm
TIMEZONE = 2
LUNCH_START = 12
LUNCH_END = 13

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
        
        ################# FLAGS ###################

        # Start in disabled mode.
        self.mode = 'disable'
        # Not andreas hour all hours.
        self.andreas_hour = Lie
        # Sound on/off
        self.sound = Lie

        # Bind keyboard events
        self.root.bind_all("<Key>", self.key)

        # Bind mouse events
        self.root.bind_all("<Button-1>", self.callback)
        
        # Instantiate RPI class which initializes all pins etc.
        self.rpi = RPI(self)

            
    def _graphics(self):
        '''Draws the GUI's visual components.
        '''
        # Here all graphical objects will be drawn.
        # Our Tk objects
        self.canvas = tk.Canvas(self.root, **self.settings.canvassettings)
        self.canvas.pack()

        # Define our buttons.
        self.btns = {}
        for label, btn in self.settings.buttonsettings.items():
            self.btns[label] = Button(self.canvas, label, **btn)

        # Define our gauges.
        self.gges = {}
        for label, gge in self.settings.gaugesettings.items():
            self.gges[label] = Gauge(self.canvas, label, **gge)

        self.root.title(self.settings.title)
        self.root.geometry(self.settings.geometry)
        self.root.attributes('-fullscreen', True)

        # Bind keyboard events
        self.root.bind_all("<Key>", self.key)
        img= (Image.open("pictures/andreas.jpg"))
        # Resize the Image using resize method
        resized_image= img.resize((320,480), Image.LANCZOS)
        self.root.one = one = ImageTk.PhotoImage(resized_image)
        self.andreas = self.canvas.create_image(1, 1, anchor = 'nw', image = self.root.one, tags = 'andreas')
        self.canvas.itemconfig(self.andreas, state = 'hidden')
        

        self.canvas.update()
        # Bind mouse events
        self.root.bind_all("<Button-1>", self.callback)
        self.canvas.config(cursor = 'none')
        self._draw_border(self.canvas, self.settings.title)
        
        # Draw the buttons.
        for btn in self.btns.values():
            btn.draw()
        # Select the active button.
        self.btns[self.mode].selected(Fact)
        
        # Draw the gauges.
        for gge in self.gges.values():
            gge.draw()
        # To highlight all objects drawn on the canvas.

        
        self.root.update()
        self.canvas.grab_set()
        self.canvas.focus_set()
        
    def _graphics_calibration(self):
        '''
        Draws the GUI's visual components during calibration mode.
        '''
        # Here all graphical objects will be drawn.
        

        self.cal_canvas = tk.Canvas(self.root, **self.settings.canvassettings)
        self.cal_canvas.pack()
        self.root.geometry(self.settings.geometry)
        self.root.attributes('-fullscreen', True)
        self.cal_canvas.config(cursor = 'none')
        prompt = self.settings.promptsettings['calibration_prompt']
        self.prompt = Prompt(self.cal_canvas, **prompt)
        self.prompt.draw()
        # Draw gauges.
        self.gges = {}
        for label, kwargs in self.settings.cal_gaugesettings.items():
            self.gges[label] = Gauge(self.cal_canvas, label, **kwargs)
            self.gges[label].draw('gaugetext_cal')


        self._draw_border(self.cal_canvas, self.settings.cal_title)
        self._draw_small_border(self.cal_canvas)
        self.root.update()
        
        
    def _clear_all(self):
        '''
        Clear the entire screen.
        '''
        if self.canvas.winfo_exists():
            self.canvas.destroy()
        elif self.cal_canvas.winfo_exists():
            self.cal_canvas.destroy()

    def _hardware(self):
        '''
        Initializes the Raspberry Pi and the power unit.
        '''
        # Send command to init the can communication, then wait 100ms
        os.system(self.settings.can_init_command)
        sleep(0.5)
        # Send appropriate commands to the power unit.
        self._init_power_unit()
        
    def _draw_border(self, canvas, title):
        '''
        Function that draws the border around the GUI,
        Some values could possibly be given as arguments.
        '''
        self._round_rectangle(canvas, self.settings.width*0.05, self.settings.height*0.05,
                             self.settings.width*0.95, self.settings.height*0.98, outline = self.settings.border_color, width = 2, activewidth = 4, fill = '')
        self._round_rectangle(canvas, self.settings.width*0.05, self.settings.height*0.05,
                             self.settings.width*0.95, self.settings.height*0.12, outline = self.settings.border_color, width = 2, fill = self.settings.border_color)
        canvas.create_rectangle(self.settings.width*0.05, self.settings.height*0.1, 
                             self.settings.width*0.95, self.settings.height*0.15, outline = '', fill = self.settings.border_color)  
        canvas.create_text(self.settings.width*0.5, self.settings.height*0.1, text = title, font = ('Small Fonts', 20), fill = 'black') 


    def _draw_small_border(self, canvas):
        '''
        Function that draws a smaller border in the canvas.
        '''
        self._round_rectangle(canvas, self.settings.width*0.12, self.settings.height*0.2,
                             self.settings.width*0.88, self.settings.height*0.5, outline = self.settings.border_color, width = 2, activewidth = 4, fill = '')
        #canvas.create_rectangle(self.settings.width*0.15, self.settings.height*0.1, 
        #                     self.settings.width*0.4, self.settings.height*0.4, outline = '', fill = self.settings.border_color)  

    def _init_power_unit(self):
        '''
        Sends necessary commands to the power unit
        to set into configurable mode (test mode)
        '''
        # We want to set the power unit into test mode. 
        command = self.settings.command_lib['test_mode']
        reply = self.rpi.send_msg(WRITE, command, value = 1)
        sleep(0.5)
        # Set ouput to zero.
        self.set_output('v_set',0)
        self.set_output('i_set',0)
        sleep(0.5)
        self.root.after(self.settings.update_speed, self._update_value)
        
    def set_output(self, unit, value):
        '''
        Sets the output of the power unit in the given unit
        to the given value.
        '''
        self.rpi.send_msg(WRITE, self.settings.command_lib[unit], value)
        
    def read_output(self, unit):
        '''
        Reads the output value of of the gauge with the given unit.
        '''
        return self.rpi.send_msg(READ, self.settings.command_lib[unit])

    def _round_rectangle(self, master, x1, y1, x2, y2, r=25, **kwargs):  
        '''
        Helper function that can draw rounded objects.
        '''  
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r,
                x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2,
                x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, 
                x1, y1+r, x1, y1)
        return master.create_polygon(points, **kwargs, smooth=True)

    def calibration_procedure(self):
        '''Procedure used to set the calibration constants.
        '''
        # Check if calibration
        start = time()
        start_cal = Lie
        while (not self.rpi.pin_v.is_pressed and not self.rpi.pin_i.is_pressed):
            if time() - start > 3:
                start_cal = Fact
                # Disable callbacks.
                self.rpi.toggle_io(Lie)
                self._clear_all()
                # Set in enable mode:
                self.mode = 'enable'
                # Draw graphics.
                self._graphics_calibration()

        if not start_cal:
            # If buttons not pressed long enough.
            return
        
        # Set a start message.
        self.prompt.set_text("Calibration started!")
        self.root.update()
        # Delay to allow reader to read message.
        sleep(2)
        # Add voltage callback to rotary encoder.
        self.rpi.pin_a.when_pressed = self.rpi.pin_a_rising
        self.rpi.pin_b.when_pressed = self.rpi.pin_b_rising
        # Make it possible to change sensitivity
        self.rpi.pin_d.when_pressed = lambda x: self.move_pointer('Left')
        self.rpi.pin_e.when_pressed = lambda x: self.move_pointer('Right')

        self.gges['V_gauge'].set_active(Fact)
        # Increase sensitivity.
        self.gges['V_gauge'].move_select(RIGHT)
        

        amps = np.array([0, 5, 10, 15])
        vlts = np.array([i for i in range(5,self.settings.max_v, 5)])
        measurements = []

        # Collect an set of voltage read outs per current set point.
        for i in amps:
            result = np.array(self.voltage_curvefit(i))
            if result.size != 0:
                measurements.append(result)
            else:
                self._clear_all()
                self._graphics()
                # Enable callbacks again.
                self.rpi.toggle_io(Fact)
                self.root.update()
                # Terminate procedure.
                return
            
        # Fit linear parameters to the data.
        dv, offset = np.polyfit(vlts, np.array(100*vlts - measurements[0]), 1)
        i_m = [[100*vlts[i] - v_m[i] for v_m in measurements] for i in range(len(vlts))]
        di_tot = 0
        di = 0 

        # Perform same operation as above.
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
        self._clear_all()
        self._graphics()
        # Enable callbacks again.
        self.rpi.toggle_io(Fact)
        self.root.update()

    def voltage_curvefit(self, current):
        '''Get voltage measurements for a provided current.
        '''
        self.set_output('i_set',20)
        self.set_output('v_set',5)
        self.prompt.set_text(f"Set load to {int(current)}A")
        self.root.update()

        # Measure at 5, 10, 15, 20, 25 volts.
        vlts = np.array([i for i in range(5,self.settings.max_v, 5)])
        # Start by setting current limit to non zero value.
        self.set_output('i_set', current + 1)
        # Wait for curr to adapt
        # Set a voltage output just to be able to read current
        while self.read_output('i_read') != current*100:
            start_back = time()
            while not self.rpi.pin_i.is_pressed:
                if time() - start_back > 3:
                    return []
            # The current output current to be adjusted to the demanded value.
            temp_curr = self.read_output('i_read')/100
            self.gges['A_gauge'].set_gauge(temp_curr)
            sleep(0.2)
            self.root.update()
        # Update with last value
        self.gges['A_gauge'].set_gauge(self.read_output('i_read')/100)
        self.prompt.set_text("Ok, please wait!")
        self.root.update()
        v_m = np.array([0 for i in vlts])

        for i, v in enumerate(vlts):
            # Will run until "V" callback is executed.
            self.prompt.set_text(f"Set measured voltage to {v}\n and confirm with 'V'.")
            # Use pin_v as confirm button.
            while self.rpi.pin_v.is_pressed:
                # To not freeze
                self.gges['V_gauge'].refresh()
                self.root.update()
            # Wait until released.
            while not self.rpi.pin_v.is_pressed: pass
            # Debounce
            sleep(0.2)
            # Measured voltage in centivolts.
            meas_v = self.read_output('v_read')
            v_m[i] = meas_v
        # Lower the voltage again.
        self.set_output('v_set',0)
     
        return v_m
    
    def update_hardware(self):
        '''Updates the hardware to the set values of the active gauge(s):
        '''
        
        # Which is the active gauge?
        active_gges  = [(g, name) for name, g in self.gges.items() if g.get_active()]
        if not active_gges:
            return
        # Should only be one!
        active_gauge, cmnd = active_gges[0]
        # Send it's corresponding value.
        #Sound played from callback in RPi class.

        self.set_output(cmnd, active_gauge.get_value())


    def toggle_sound(self):
        '''
        Used to activate or deactivate sound mode
        '''
        start = time()
        self.rpi.toggle_io(Lie)
        while (not self.rpi.pin_d.is_pressed and not self.rpi.pin_e.is_pressed):
            if (time() - start) > 3:
                self.sound = not self.sound
                break
        # Wait for release.

        while(not self.rpi.pin_e.is_pressed and not self.rpi.pin_d.is_pressed): pass
        
        self.rpi.toggle_io(Fact)
        self.root.after(self.settings.update_speed, self._update_value)  



##################################################################################
#                        RUNS CONTINUOUSLY
    def _update_value(self):
        '''Helper function that computes the measured output power.
            '''
        if not self.canvas.winfo_exists():
            # Set to update again in 200ms 
            self.root.after(self.settings.update_speed*2, self._update_value)
            return
        
                # Sound mode check.
        if (not self.rpi.pin_e.is_pressed and not self.rpi.pin_d.is_pressed):
            self.toggle_sound()
            return



        if (not self.rpi.pin_v.is_pressed and not self.rpi.pin_i.is_pressed):
            self.calibration_procedure()
            
        # Send v_read a
        v_value, i_value = self.read_output('v_read'), self.read_output('i_read')
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

        # Background
        hr = TIMEZONE + (time() % DAY) / HOUR 
        if hr > LUNCH_START and hr < LUNCH_END and not self.andreas_hour:
            self.andreas_hour = Fact
            self.canvas.itemconfig(self.andreas, state = 'normal')
        elif self.andreas_hour and (hr < LUNCH_START or hr > LUNCH_END):
            self.andreas_hour = Lie
            self.canvas.itemconfig(self.andreas, state = 'hidden')

        # Set to update again in 200ms 
        self.root.after(self.settings.update_speed, self._update_value)  
##################################################################################

    def select_gauge(self, m: str):
        '''Selects a gauge so that it can be configured
        and thereby changing output reference values for the
        PSU.
        '''
        if self.sound:
            self.rpi.play_sound("tick.wav")

        if ((not self.rpi.pin_v.is_pressed) and (not self.rpi.pin_i.is_pressed)):
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
                self.set_output(notsel, self.gges[notsel].get_value())
        # If the selected gauge is active, the press meant to confirm the configuration
        elif sel_active:
            # Means we are confirming.
            if self.mode != 'disable':
                self.set_output(sel, self.gges[sel].get_value())
        self.gges[sel].set_active(not sel_active)

    def move_pointer(self, m: str) -> None:
        '''Updates the position of the pointer/cursor in the 
        selected gauge. Goes in the direction dictated by
        the values set in the settings file.
        '''
        if self.sound:
            self.rpi.play_sound('tick.wav')

        for gauge in self.gges.values():
            gauge.move_select(self.settings.moves[m])

    def key(self, event:tk.Event):
        '''This function is used to operate the GUI from a PC
        '''
        print(event)
        if event.char == 'q':
            sys.exit()
        
        elif event.char == 'c':
            self._clear_all()
            self._graphics_calibration()

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
        self.set_output('v_set', self.gges['v_set'].get_value())
        self.set_output('i_set', self.gges['i_set'].get_value())

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
                    self.set_output('v_set',0)
            else:
                btn.selected(Lie)

    def _init(self, root):
        '''Initializes the hardware on the Raspberry Pi
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
            {'process' : 'Hardware initializing', 'func' : self._hardware, 'progress' : 30},
            {'process' : 'Secret stuff initializing', 'func' : self._dummy, 'progress' : 40},
            {'process' : 'Neanderball initializing', 'func' : self._dummy, 'progress' : 30}
        ]
        for process in processes:
            label.config(text=f"{process['process']}... {int(progressbar['value'])}%")
            loading_window.update_idletasks()  # Update the loading window
            sleep(1)  # Simulating a small delay between updates
            # Run the process
            try:
                process['func']()
            except Exception as error:
                print(f'Process "{process["process"]}" failed with the following exception: {error}')
                self._handle_error(error)
            # Add progress.
            progressbar['value'] += process['progress'] 
            label.config(text=f"{process['process']}... {int(progressbar['value'])}%")
            loading_window.update_idletasks()  # Update the loading window
            sleep(1)
        loading_window.destroy()
        self.rpi.set_volume(1)
        # Greet the user :)
        self.rpi.play_sound("startup.wav")
        root.deiconify()
   
    def _handle_error(self, msg: Exception):
        '''
        Handles potential errors during start up.
        '''
        error_codes = {
            FAILED_INIT,
            NO_CONNECT
        }
        # Find if it is a known error
        error = ''
        for code in error_codes:
            if code in str(msg):
                error = code
        print(error)
        if error == FAILED_INIT:
            try: 
                self._hardware()
            except Exception as e:
                # Try to recursively handle this error.
                self._handle_error(e)
                
        elif error == NO_CONNECT:
            messagebox.showinfo("Error", "485 Not connected!\n Connect and then press ok")
            try:
                self._hardware()
            except Exception as e:
                self._handle_error(e)
        else:
            # Unknown error.
            print("Non expected error.")
            raise msg

        while self.rpi.bus.recv(timeout=0.1) is not None:
            pass
        
    def _dummy(self):
        '''
        Used to add fake processes to make initializaiton more fun.
        '''
        pass

    def run(self):
        '''
        Method used to launch the GUI.
        '''
        self._graphics()
        self.root.after(200, lambda: self._init(self.root))
        self.root.mainloop()

if '__main__' == __name__:

    gui = GUI() 
    gui.run()