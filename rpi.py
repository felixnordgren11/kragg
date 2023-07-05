import gpiozero as io
from settings import Settings
import tkinter as tk
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
                # First we get the active gauge:
                self.update_hardware()
                

    def pin_b_rising(self):                   # Pin B event handler
        '''Handler for when pin is set high
        '''
        if self.pin_a.is_pressed:
             self.add_value(-1) 
             if self.GUI.mode == 'enable':
                # Update hardware
                self.update_hardware()

    def update_hardware(self):
        '''Updates the hardware to the set values of the active gauge(s):
        '''
        # Which is the active gauge?
        active_gges  = [(g, name) for name, g in self.GUI.gges.items() if g.get_active()]
        if not active_gges:
            return
        active_gauge, cmnd = active_gges
        # Send it's corresponding value.
        self.send_msg(WRITE, self.settings.command_lib[cmnd], active_gauge.get_value())

    def add_value(self, value: int):
        # Add value to the active gauge objects in the GUI
        for gauge in self.GUI.gges.values():
            # We check all as only one will be active at any time.
            if gauge.get_active():
                gauge.digit_change(value)
        

    def send_msg(self, tpe: str, command, value = 0.0) -> int:
        '''Send the specified type of message with given 
        command and value. If tpe is READ, then return value
        is the answer given by the power unit.
        '''
        # Getting the message from library written in settings 
        arb_id, msg_data = command
        # Make value to centiunits.
        if tpe == WRITE:
            if (msg_data[-1] >> 4) != 0xF:
                # +1 is to compensate for 485 setting 
                # out max when sent 0. Nocco
                value = int(100*value) + 1
                # Data is divided into bytes.
                MSB = value >> 8
                LSB = value - (MSB << 8)
                msg_data = [*msg_data, LSB, MSB] 

            else:
                value = int(value)
                msg_data = [*msg_data, value]
        # Construct a message object to be sent on the bus.
        msg = can.Message(arbitration_id = arb_id, data = msg_data, is_extended_id=False)
        self.bus.send(msg)
        # If tpe is READ them 
        if tpe == READ:
            msg = self.bus.recv(timeout = 0.2)
            if msg is not None:
                return self._decode(msg)
        else:
            #clear buffer
            self.bus.recv(timeout=0.1)
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
        # Check if negative
        MSB = data[-1]
        is_negative = (0b10000000 & MSB) == 0b10000000
        if is_negative:
            return 0
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
            print(ans/100)
            