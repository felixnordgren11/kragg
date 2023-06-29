import gpiozero as io
from settings import Settings
import tkinter as tk
import serial
import can

ROTARY_LEFT = 0
ROTARY_RIGHT = 1
BUTTON_LEFT = 5
BUTTON_RIGHT = 6
BUTTON_V = 13
BUTTON_I = 12
WRITE = 'write'
READ = 'read'


class RPI:

    def __init__(self, GUI = None):
        '''Instantiates the RPI class
        '''
        # Store the GUI object that is running on the raspberry pi.
        if GUI is None:
            print("Test mode")
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

        try:
            self.bus = can.Bus(channel = channel, interface = bustype)
        except Exception as e:
            print('Can initialization failed with following exception:', e)
        # Binding the pins to functions.
        if GUI is not None:
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
        

    def send_msg(self, tpe: str, command, value = 0.0) -> int:
   
        # Getting the message from library written in settings 
        arb_id, msg_data = command
        # Make value to centiunits.
        if tpe == WRITE:
            if (msg_data[-1] >> 4) != 0xF:
                value = int(100*value)
                # Data is divided into bytes.
                MSB = value >> 8
                LSB = value - (MSB << 8)
                msg_data = [*msg_data, LSB, MSB]
            else:
                value = int(value)
                msg_data = [*msg_data, value]

        msg = can.Message(arbitration_id = arb_id, data = msg_data)
        self.bus.send(msg)

        if tpe == READ:
            msg = self.bus.recv()
            if msg is not None:
                return self._decode(msg)
        return 0
    

    @staticmethod
    def _decode(msg: can.Message) -> int:
        '''Returns the data contained in the
        most recent 
        '''
        # msg.data is a byte array
        data = list(msg.data) 
        # The relevant data lies in bytes 4 - 8
        data = data[4:]
        # Now, convert from this array which is little endian
        data = sum([d << i*8 for i, d in enumerate(data)])
        return data
    
if __name__ == '__main__':

    rpi = RPI()
    while 1:
        id, cmnd = rpi.settings.command_lib[input('Command: ')]
        if cmnd[0] == 0x2F:
            value = float(input('Value: '))
            tpe = WRITE
            rpi.send_msg(tpe, (id,cmnd),  value= value)
        else:
            tpe = READ
            ans = rpi.send_msg(tpe, (id,cmnd))
            print(ans)
            