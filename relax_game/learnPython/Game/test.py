import pygame
pygame.init()

win = pygame.display.set_mode((500,480))
pygame.display.set_caption("learn Python")

#load sound
#bulletSound = pygame.mixer.Sound("Game/bullet.wav")
#hitSound = pygame.mixer.Sound("Game/hit.wav")

music = pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)