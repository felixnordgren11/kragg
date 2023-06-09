

class Settings:

    def __init__(self):
        self.title = 'GUI'
        self.geometry = "320x480"
        self.width, self.height = map(int, self.geometry.split('x'))
        # Canvas config
        self.canvassettings = {'bg' : 'black',
                               'height' : self.height,
                               'width' : self.width}
        
        