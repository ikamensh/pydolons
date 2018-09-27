import pygame

# pygame.mixer.init()
# pygame.init()

pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init() #turn all of pygame on.

Sound = pygame.mixer.Sound

# from PySide2.QtMultimedia import QSound as Sound

# import vlc
