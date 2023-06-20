# Add list of model numbers of possible units for
# interchangability.

Fact = True
Lie = False
LEFT = -1
RIGHT = 1


class Settings:

    def __init__(self):
        self.title = 'GUI'
        self.geometry = "480x800"
        self.width, self.height = map(int, self.geometry.split('x'))
        self.bg = 'black'
        self.textcolor = 'white'
        self.font = 'Small Fonts'
        # Canvas config
        self.bg = 'black'
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
                           'unit' : 'A',
                           'fg' : '#ffffff',
                           'font' : (self.font, self.output_font_size),
                           },
            'p'         : {'a' : self.width*0.1,
                           'b' : self.height*0.385,
                           'width' : 1,
                           'bg' : 'black',
                           'unit' : 'W',
                           'fg' : 'white',
                           'font' : (self.font, self.output_font_size),
                           },
            'v_set'   : {'a' : self.width*0.6,
                           'b' : self.height*0.18,
                           'width' : 1,
                           'max' : self.max_v,
                           'bg' : '#ffffff',
                           'active' : '#991100',
                           'unit' : 'V',
                           'fg' : '#000000',
                           'font' : (self.font, 15),},
            'i_set'   : {'a' : self.width*0.6,
                           'b' : self.height*0.28,
                           'width' : 1,
                           'unit' : 'A',
                           'active' : '#991100',
                           'max' : self.max_i,
                           'bg' : 'white',
                           'fg' : 'black',
                           'font' : (self.font, 15),
                           },
            
        }
        
        self.moves = {
        'Left': LEFT,
        'Right': RIGHT
        }
        # Format [ID#MESSAGE]
        id = '61B'
        self.command_lib = {
            'init' : f'{id}#2F1020FF10',
            'v_read' : f'{id}#4010202100',
            'i_read' : f'{id}#4010202100' 
        }
        
        