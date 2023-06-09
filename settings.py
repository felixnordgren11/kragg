

class Settings:

    def __init__(self):
        self.title = 'GUI'
        self.geometry = "480x320"
        self.width, self.height =  self.geometry.split('x')
        # Canvas config
        self.canvassettings = {'bg' : 'black',
                               'height' : self.height,
                               'width' : self.width}
        
        