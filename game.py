import random
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
start_fly = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #ms
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

# Images
bg = pygame.image.load('./img/bg2.png')
ground = pygame.image.load('./img/ground.png')

# Score display
font = pygame.font.SysFont('Bauhaus 93', 60)
white = (255, 255, 255)
def draw_score(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

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

        self.vel = 0
        self.clicked = False

    def update(self):

        # Gravity
        if start_fly == True:
            self.vel += 0.3
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 437: 
                self.rect.y += int(self.vel)

        # Jump
        if game_over == False:

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel -= 10
            
            if self.vel < -8:
                self.vel = -5

            # Upper wall
            if self.rect.top < 0:
                self.rect.y = 0

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            

            ## Flap anime interval
            self.counter += 1
            cooldown = 10

            if self.counter > cooldown:
                self.counter = 0
                self.index += 1

                if self.index >= len(self.images):
                    self.index = 0
            
                self.image = self.images[self.index]

            # Rotation
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)

        # Game over anime
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)
            self.vel += 0.3
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 437: 
                self.rect.y += int(self.vel)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./img/pipe.png')
        self.rect = self.image.get_rect()

        # Orientation: 1 for top -1 for bottom
        if pos == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - (pipe_gap // 2)]
        if pos == -1:
            self.rect.topleft = [x, y + (pipe_gap // 2)]

    def update(self):
        self.rect.x -= scroll_speed

        if self.rect.right < 0:
            self.kill()



bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, HEIGHT//2)
bird_group.add(flappy)


# Loop
run = True

while run:
    
    clock.tick(fps)

    screen.blit(bg, (0,0))

    # Draw bird
    bird_group.draw(screen)
    bird_group.update()

    # Draw pipes
    pipe_group.draw(screen)
    
    # Draw ground after pipes
    screen.blit(ground, (ground_scroll, 440))

    # Check score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe == False:
            pass_pipe = True
        
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    # Update score 
    draw_score(str(score), font, white, WIDTH//2, 20)

    # Collision 
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
        game_over = True
        start_fly = False

    # Bird hits ground
    if flappy.rect.bottom >= 437:
        game_over = True
        start_fly = False

    # Scrolling background, draw pipes
    if game_over == False and start_fly == True:

        # New pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-80, 80)
            btm_pipe = Pipe(WIDTH, HEIGHT//2 + pipe_height, -1)
            top_pipe = Pipe(WIDTH, HEIGHT//2 + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 70:
            ground_scroll = 0

        pipe_group.update()


    # Events
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and start_fly == False and game_over == False:
            start_fly = True


    # Update screen
    pygame.display.update()

# Close
pygame.quit()


