import gpiozero as io
from settings import Settings
import tkinter as tk
import serial
import spidev
import can

ROTARY_LEFT = 3
ROTARY_RIGHT = 2
BUTTON_LEFT = 23
BUTTON_RIGHT = 24
BUTTON_V = 4
BUTTON_I = 25
WRITE = 'write'
READ = 'read'

def spi_en(func):
    '''Decorator that returns the same function
    only that the label of a Gauge object is activated
    before execution and deactivated after.
    '''
    def wrapper(self, *args, **kwargs):
        self.spi.open(0,1)
        var = func(self, *args, **kwargs)
        self.spi.open(0,0)
        return var
    return wrapper

class RPI:

    def __init__(self, GUI):
        '''Instantiates the RPI class
        '''
        # Store the GUI object that is running on the raspberry pi.
        self.GUI = GUI
        self.settings = Settings()
        # Following two pins are used for the rotary encoder
        self.pin_a = io.Button(ROTARY_LEFT)                      # Rotary encoder pin A connected to GPIO2
        self.pin_b = io.Button(ROTARY_RIGHT)                      # Rotary encoder pin B connected to GPIO3
        # Used to select the v_set gauge
        self.pin_c  = io.Button(BUTTON_V)
        # Used to toggle between the digits when setting the reference output
        self.pin_d  = io.Button(BUTTON_LEFT)
        self.pin_e  = io.Button(BUTTON_RIGHT)
        # Used to select the i_set gauge.
        self.pin_f  = io.Button(BUTTON_I)
        # Can details:
        bustype = 'socketcan'
        channel = 'can0'
        # Spi stuff for the raspberry
        self.spi = spidev.SpiDev()
        try:
            self.bus = can.Bus(channel = channel, interface = bustype)
        except Exception as e:
            print('Can initialization failed with following exception:', e)
        # Binding the pins to functions.
        self.pin_a.when_pressed = self.pin_a_rising
        self.pin_b.when_pressed = self.pin_b_rising
        self.pin_c.when_pressed = lambda x: self.GUI.select_gauge('v')
        self.pin_d.when_pressed = lambda x: self.GUI.move_pointer('Left')
        self.pin_e.when_pressed = lambda x: self.GUI.move_pointer('Right')
        self.pin_f.when_pressed = lambda x: self.GUI.select_gauge('i')
    
    def pin_a_rising(self):                # Pin A event handler
        '''Handler for when pin is set high
        '''
        if self.pin_b.is_pressed:
            self.add_value(1)
            if self.GUI.mode == 'enable':
                # Update voltage and send.
                pass

    def pin_b_rising(self):                   # Pin B event handler
        '''Handler for when pin is set high
        '''
        if self.pin_a.is_pressed:
             self.add_value(-1) 
             if self.GUI.mode == 'enable':
                # Update voltage and send.
                pass


    def add_value(self, value: int):
        # Add value to the active gauge objects in the GUI
        for gauge in self.GUI.gges.values():
            # We check all as only one will be active at any time.
            if gauge.get_active():
                self.GUI.gges['v_set'].digit_change(value)
        
    @spi_en
    def send_msg(self, tpe: str, value: int, unit: str) -> str:
        # Construct the key with which the message is obtained.
        # Will return answers. If tpe is not READ then '' will be returned.
        key = '_'.join([unit, tpe])
        # Getting the message from library written in settings 
        id, msg_data = self.settings.command_lib[key]
        
        if tpe == WRITE:
            MSB = value >> 4
            LSB = value - MSB
            msg_data = [*msg_data, LSB, MSB]

        msg = can.Message(arbitration_id = id, data = msg_data)
        self.bus.send(msg)

        if tpe == WRITE:
            return str(self.bus.recv())
        return ''
        
        


