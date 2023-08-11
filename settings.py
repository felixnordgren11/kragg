# Add list of model numbers of possible units for
# interchangability.

Fact = True
Lie = False
LEFT = -1
RIGHT = 1
# Some error codes
FAILED_INIT = '100'
NO_CONNECT = '105'
import tkinter as tk

class Settings:
    '''This class is used to keep track of all settings through out the
    program.
    '''
    def __init__(self):
        self.title = 'GUI'
        self.cal_title = 'CALIBRATION'
        self.geometry = "320x480"
        self.width, self.height = map(int, self.geometry.split('x'))
        self.bg = 'black'
        self.textcolor = 'white'
        self.font = 'Small Fonts'
        self.title = "Kragg"
        self.set_fontsize = 16
        self.file = "dickmas.jpg"
        # Canvas config
        self.bg = '#000000'
        self.textcolor = 'white'
        self.model_nr = 'SMP485'
        self.border_color = 'white'
        self.enable_color = '#00ff66'
        self.disable_color = '#ff5500'
        self.keep_color = '#0066ff'
        self.canvassettings = {
            'bg' : self.bg,
            'height' : self.height,
            'width' : self.width}
         
        # To calibrate the output voltage.
        self.cal_file = 'cal.sheesh'
        self.calibration = self.read_calibration(self.cal_file)
         
        # Screen update speed
        self.update_speed = 100
         # Voltage first, current second.
        self.maximums = {
            'SMP485' : [30, 25],
            'SMP358' : [69, 420]
         }

        self.max_v, self.max_i = self.maximums[self.model_nr]

        # For different types of text
        self.textsettings = {
            # create_canvas is used for this object.
            'buttontext' : {
                'fill' : '#fff',
                'font' : ("Small Fonts", 15),
            },
            'gaugetext' : {
                'width' : "8", 
                'height' : "1", 
            },
            'gaugetext_cal' : {
                'width' : "8", 
                'height' : "1",
            },
            'prompttext' : {
                'font' : (self.font, 13), 
                'fg' : '#ffffff',
                'bg' : '#000000',
                'anchor' : 'center',
                'height' : 2,
            }
            
        }
        self.buttonsettings = {
            'enable'  : {'x1' : self.width*0.1,
                         'y1' : self.height*0.51,
                         'x2' : self.width*0.9,
                         'y2' : self.height*0.64,
                         'outline' : self.enable_color, 
                         'width' : 2,
                         'fill' : 'black'},
            'disable' : {'x1' : self.width*0.1,
                         'y1' : self.height*0.66,
                         'x2' : self.width*0.9,
                         'y2' : self.height*0.79,
                         'outline' : self.disable_color, 
                         'width' : 2,
                         'fill' : 'black'},
            'keep'    : {'x1' : self.width*0.1,
                         'y1' : self.height*0.81,
                         'x2' : self.width*0.9,
                         'y2' : self.height*0.94,
                         'outline' : self.keep_color, 
                         'width' : 2,
                         'fill' : 'black'}
        }
        #
        
        self.promptsettings = {
            'calibration_prompt': {'x1' : self.width*0.2,
                         'y1' : self.height*0.24,
                         'x2' : self.width*0.8,
                         'y2' : self.height*0.45,
                         'fill' : 'black'},
        }
        
        self.gauge_format = '00.00'
        # Change this to select what the default precision is when setting the gauges
        self.default_digit = 1
        # Change these to configure gauges.
        self.output_font_size = 20
        
        self.gaugesettings = {
            'v_out'   : {'a' : self.width*0.1,
                           'b' : self.height*0.185,
                           'width' : 1,
                           'bg' : 'black',
                           'unit' : 'V',
                           'fg' : 'white',
                           'font' : (self.font, self.output_font_size),
                           },
            'i_out'   : {'a' : self.width*0.1,
                           'b' : self.height*0.285,
                           'width' : 1,
                           'bg' : '#000000',
                           'max': self.max_i,
                           'unit' : 'A',
                           'fg' : '#ffffff',
                           'font' : (self.font, self.output_font_size),
                           },
            'p'         : {'a' : self.width*0.1,
                           'b' : self.height*0.385,
                           'width' : 1,
                           'bg' : 'black',
                           'unit' : 'W',
                           'fg' : '#f1b434',
                           'font' : (self.font, self.output_font_size-3),
                           },
            'v_set'   : {'a' : self.width*0.58,
                           'b' : self.height*0.19,
                           'width' : 1,
                           'bg' : '#ffffff',
                           'active' : '#991100',
                           'max' : self.max_v,
                           'unit' : 'V',
                           'fg' : '#000000',
                           'font' : (self.font, 15),},
            'i_set'   : {'a' : self.width*0.58,
                           'b' : self.height*0.295,
                           'width' : 1,
                           'unit' : 'A',
                           'active' : '#991100',
                           'max' : self.max_i,
                           'bg' : 'white',
                           'fg' : 'black',
                           'font' : (self.font, 15),
                           },
            
        }

        self.cal_gaugesettings = {
            'A_gauge' : {
                'a' : self.width*0.1,
                'b' : self.height*0.75,
                'width' : 2,
                'bg' : '#ffffff',
                'max': self.max_i,
                'unit' : 'A',
                'fg' : '#000000',
                'font' : ("Small Fonts", 35),
            },
            'V_gauge' : {
                'a' : self.width*0.1,
                'b' : self.height*0.55,
                'width' : 2,
                'active' : '#991100',
                'bg' : '#ffffff',
                'max': self.max_v,
                'unit' : 'V',
                'fg' : '#000000',
                'font' : ("Small Fonts", 35),
        }
        }
        
        self.moves = {
        'Left': LEFT,
        'Right': RIGHT
        }
        
        
        # Format [ID#MESSAGE]
        id = 0x61B
        self.command_lib = {
            'init'   : (id, [0x2F, 0x10, 0x20, 0xFF]),
            'v_read' : (id, [0x40, 0x10, 0x20, 0x21]),
            'i_read' : (id, [0x40, 0x10, 0x20, 0x22]),
            'v_set'  : (id, [0x2F, 0x10, 0x20, 0x11]),
            'V_gauge'  : (id, [0x2F, 0x10, 0x20, 0x11]),
            'i_set'  : (id, [0x2F, 0x10, 0x20, 0x10]),
            'test_mode' : (id, [0x2F, 0x10, 0x20, 0xFF]),
            'enable_powertrain' : (id, [0x2F, 0x10, 0x20, 0xF1]),
            'test_dp' : (id, [0x2F, 0x10, 0x20, 0xFE])
        }

        self.can_init_command = 'sudo ip link set can0 up type can bitrate 500000'
        
    def read_calibration(self, cal_file: str):
        '''Reads calibration data from text file
        '''
        with open(cal_file, 'r', encoding = 'utf-8') as data:
            lines = data.readlines()

        cal_data = {}

        for line in lines:
            line = line.replace(' ', '')
            key, value = line.split(':')
            cal_data[key] = float(value)

        return cal_data