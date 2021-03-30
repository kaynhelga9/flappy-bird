import pygame
from pygame.locals import *

# Setup
pygame.init()

WIDTH = 800
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')

clock = pygame.time.Clock()
fps = 60


# Variables
ground_scroll = 0
scroll_speed = 3


# Images
bg = pygame.image.load('./img/bg2.png')
ground = pygame.image.load('./img/ground.png')


# Bird
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        



# Loop
run = True

while run:
    
    clock.tick(fps)

    screen.blit(bg, (0,0))

    # Scrolling background
    screen.blit(ground, (ground_scroll, 400))
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 70:
        ground_scroll = 0


    # Quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

# Close
pygame.quit()


