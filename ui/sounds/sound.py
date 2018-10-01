# import pygame

# pygame.mixer.init()
# pygame.init()

# pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
# pygame.init() #turn all of pygame on.

# Sound = pygame.mixer.Sound

class Sound(object):
    """docstring for Sound."""
    def __init__(self, arg):
        super(Sound, self).__init__()
        self.arg = arg

    def play(self):
        print('play from', self.arg)



# Sound = object

# from PySide2.QtMultimedia import QSound as Sound

# import vlc
