
Fact = True
Lie = False

class Settings:

    def __init__(self):
        self.title = 'GUI'
        self.geometry = "320x480"
        self.width, self.height = map(int, self.geometry.split('x'))
        # Canvas config
        self.canvassettings = {
            'bg' : 'black',
            'height' : self.height,
            'width' : self.width}
        
        
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
        
        