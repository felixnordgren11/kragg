''' Here some code will be written,
NAWRAHL CABON BRAINWOW
'''
import tkinter as tk
from settings import Settings

class GUI:
    '''
    Our main class
    '''

    def __init__(self):
        '''Initializes variables'''

        self.root = tk.Tk()
        self.settings = Settings()
        self.canvas = tk.Canvas(self.root, **self.settings.canvassettings)
        self.canvas.pack()
        
        self.root.title(self.settings.title)
        self.root.geometry(self.settings.geometry)

    def run(self):
        self.root.mainloop()
        pass


if '__main__' == __name__:
    gui = GUI()
    gui.run()
 
