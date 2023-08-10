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
        files = os.listdir(path = current_dir) #Put all files in a list
        lst = [file for file in files if file.split('.')[1] == 'wav'] #Save all .wav files in a new list
        dict = {i: pygame.mixer.Sound(i) for i in lst} #Make directory with all .wav files
        return dict
    
    def play_sound(self, audio_file : str):
        playing = self.sounds[audio_file].play()
        while playing.get_busy():
            pygame.time.delay(100)
        
    def set_volume(self, volume):
        self.volume = volume

            

            
