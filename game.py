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

        self.images = []
        self.index = 0
        self.counter = 0

        # Motion list
        for num in range(3):
            image = pygame.image.load(f'./img/bird{num+1}.png')
            self.images.append(image)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        ## Flap anime interval
        self.counter += 1
        cooldown = 10

        if self.counter > cooldown:
            self.counter = 0
            self.index += 1

            if self.index >= len(self.images):
                self.index = 0
        
            self.image = self.images[self.index]


bird_motions = pygame.sprite.Group()

flappy1 = Bird(100, HEIGHT//2)

bird_motions.add(flappy1)


# Loop
run = True

while run:
    
    clock.tick(fps)

    screen.blit(bg, (0,0))

    # Scrolling background
    screen.blit(ground, (ground_scroll, 440))
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 70:
        ground_scroll = 0


    # Draw bird
    bird_motions.draw(screen)
    bird_motions.update()


    # Quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

# Close
pygame.quit()


