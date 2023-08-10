import pygame
import os


class Sound:
    '''
    Class used to store and play sounds from the RPi
    '''
    def __init__(self):

        # Init the mixer.
        pygame.mixer.init()
        self.sounds = self.sound_files()
        self.volume = 0.5
        
        
    def get_files(self) -> list[str]:
        current_dir  = os.getcwd()
        return os.listdir(path = current_dir)
        
        
    def sound_files(self):
        files = self.get_files()
        lst = [file for file in files if file.split('.')[1] == 'wav']
        dick = {i: pygame.mixer.Sound(i) for i in lst}
        return dick
    
    def play_sound(self, audio_file : str):
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(audio_file)
        
    def set_volume(self, volume):
        self.volume = volume

            

            