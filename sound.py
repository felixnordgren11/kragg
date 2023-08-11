import pygame
import os


class Sound:
    '''
    Class used to store and play sounds from the RPi
    '''
    def __init__(self):

        # Init the mixer.
        pygame.mixer.init()
        self.sounds = self.get_filedict()
        self.volume = 0.5
    
    def get_filedict(self):
        '''
        Finds an puts all .wav files in a dictionary
        '''
        current_dir  = os.getcwd() #Check current directory

        folder = "sound"

        # Check sound folder.
        files = os.listdir(path = (current_dir + "/" + folder)) #Put all files in a list
        if files:
            lst = [file for file in files if file.split('.')[1] == 'wav'] #Save all .wav files in a new list
            print(files)
            dct = {i: pygame.mixer.Sound(os.getcwd() + "/" + folder + "/" + i) for i in lst} #Make directory with all .wav files
        else:
            dct = {}
            
        return dct
    
    def play_sound(self, audio_file : str):
        self.sounds[audio_file].set_volume(self.volume)
        playing = self.sounds[audio_file].play()
        while playing.get_busy():
            pygame.time.delay(10)
        
    def set_volume(self, volume):
        self.volume = volume


if __name__ == '__main__':
    pass