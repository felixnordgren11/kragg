import gpiozero as io
import tkinter as tk
ROTARY_LEFT = 3
ROTARY_RIGHT = 2
BUTTON_LEFT = 23
BUTTON_RIGHT = 24
BUTTON_V = 4

class RPI:

    def __init__(self, GUI):

        self.GUI = GUI
        self.pin_a = io.Button(ROTARY_LEFT)                      # Rotary encoder pin A connected to GPIO2
        self.pin_b = io.Button(ROTARY_RIGHT)                      # Rotary encoder pin B connected to GPIO3
        self.pin_c  = io.Button(BUTTON_V)
        self.pin_d  = io.Button(BUTTON_LEFT)
        self.pin_e  = io.Button(BUTTON_RIGHT)

        self.pin_a.when_pressed = self.pin_a_rising
        self.pin_b.when_pressed = self.pin_b_rising
        self.pin_c.when_pressed = lambda x: self.keypress('char', 'v')
        self.pin_d.when_pressed = lambda x: self.keypress('keysym', 'Left')
        self.pin_e.when_pressed = lambda x: self.keypress('keysym', 'Right')
    
    def pin_a_rising(self):   
        print(1)              # Pin A event handler
        if self.pin_b.is_pressed:
            self.add_value(1)
            

    def pin_b_rising(self):   
        print(2)                 # Pin B event handler
        if self.pin_a.is_pressed:
             self.add_value(-1) 


    def add_value(self, value):
        if self.GUI.gges['v_set'].get_active():
            self.GUI.gges['v_set'].digit_change(value)
        elif self.GUI.gges['i_set'].get_active():
            self.GUI.gges['i_set'].digit_change(value) 

    def keypress(self, attr, value):
        event = tk.Event()
        setattr(event, attr, value)
        self.GUI.key(event)
