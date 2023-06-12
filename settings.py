
Fact = True
Lie = False

class Settings:

    def __init__(self):
        self.title = 'GUI'
        self.geometry = "320x480"
        self.width, self.height = map(int, self.geometry.split('x'))
        self.bg = 'black'
        self.textcolor = 'white'
        self.font = 'Small Fonts'
        # Canvas config
        self.canvassettings = {
            'bg' : 'black',
            'height' : self.height,
            'width' : self.width}
        
        self.textsettings = {
            'buttontext' : {
                'width' : "10", 
                'height' : "2", 
                'bg' : self.bg,
                'fg' : self.textcolor,
                'font' : ("Helvetica", 10),
            },
            'gaugetext' : {
                'width' : "10", 
                'height' : "2", 
            }
            
        }
        
        self.buttonsettings = {
            'enable'  : {'x1' : self.width*0.1,
                         'y1' : self.height*0.51,
                         'x2' : self.width*0.9,
                         'y2' : self.height*0.64,
                         'outline' : '#00ff66', 
                         'width' : 2,
                         'fill' : 'black'},
            'disable' : {'x1' : self.width*0.1,
                         'y1' : self.height*0.66,
                         'x2' : self.width*0.9,
                         'y2' : self.height*0.79,
                         'outline' : '#00ff66', 
                         'width' : 2,
                         'fill' : 'black'},
            'keep'    : {'x1' : self.width*0.1,
                         'y1' : self.height*0.81,
                         'x2' : self.width*0.9,
                         'y2' : self.height*0.94,
                         'outline' : '#00ff66', 
                         'width' : 2,
                         'fill' : 'black'}
        }
        
        
        
        self.gaugesettings = {
            'v_out'   : {'a' : self.width*0.1,
                           'b' : self.height*0.15,
                           'width' : 1,
                           'bg' : 'black',
                           'fg' : 'white',
                           'font' : (self.font, 14),
                           },
            'i_out'   : {'a' : self.width*0.1,
                           'b' : self.height*0.26,
                           'width' : 1,
                           'bg' : 'black',
                           'fg' : 'white',
                           'font' : (self.font, 14),
                           },
            'p'         : {'a' : self.width*0.1,
                           'b' : self.height*0.36,
                           'width' : 1,
                           'bg' : 'black',
                           'fg' : 'white',
                           'font' : (self.font, 14),
                           },
            'v_set'   : {'a' : self.width*0.6,
                           'b' : self.height*0.17,
                           'width' : 1,
                           'bg' : 'white',
                           'fg' : 'black',
                           'font' : (self.font, 12),
                           },
            'i_set'   : {'a' : self.width*0.6,
                           'b' : self.height*0.27,
                           'width' : 1,
                           'bg' : 'white',
                           'fg' : 'black',
                           'font' : (self.font, 12),
                           },
            
        }
        
        