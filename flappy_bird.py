# Import a library of functions called 'pygame'
import pygame
import random
import math
from math import pi
import pipes as pipeModule
import bird
from ga import nextGeneration, getBestBirdBrain
import slider as slider_module

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.picture = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.picture, (700, 400))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

GREY = (200, 200, 200)
ORANGE = (200, 100, 50)
TRANS = (1, 1, 1)

# Initialize the game engine
pygame.init()
pygame.font.init()

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

# Set the height and width of the screen
size = [700, 400]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("T flappy birds")

#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 60
all_sprites = pygame.sprite.Group()

#flappy-bird specific
#TODO: load in best bird as option
slider = slider_module.Slider("Speed", 1, 20, 1, 25)
totalBirds = 1
birds = []
savedBirds = []
score = 0
current_generation = 0
pipesOnScreen = []
BackGround = Background('background.png', [0,0])

if totalBirds == 1:
    birds.append(getBestBirdBrain())
else:
    # initialize totalBirds
    for i in range(totalBirds):
        # create new bird, add to list of birds
        birds.append(bird.Bird(size[1], None))

flag_key_released = True
all_sprites.add(birds)


while not done:

    # Clear the screen and set the screen background
    screen.fill(BLACK)
    # screen.blit(BackGround.image, BackGround.rect)

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if slider.button_rect.collidepoint(pos):
                slider.hit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            slider.hit = False

        """ comment below out if actually wanting to play, commented for nnet purposes"""
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE and flag_key_released == True:
        #         bird.flap()
        #         flag_key_released = False
        # elif event.type == pygame.KEYUP:
        #     if event.key == pygame.K_SPACE:
        #         flag_key_released = True
        # if event.type == pygame.MOUSEBUTTONDOWN: # If user clicked
        #     pos = pygame.mouse.get_pos()
        #     pygame.draw.circle(screen, WHITE, (pos), 20, 1) # Flag that we are done so we exit this loop

    # adjust speed of generations based on slider
    for t in range(int(slider.val)):
        score += 1
        # if no pipes on screen, create new pipe
        if not pipesOnScreen:
            newPipe = pipeModule.Pipe(size[0], size[1])
            pipesOnScreen.append(newPipe)

        """ deal with adding and removing pipes on screen """
        for pipes in pipesOnScreen:
            if((pipes.getXRight() < 0.7*size[0]) and (pipes.lessThanX is False)):
                # print("adding new pipe!!")
                pipes.lessThanX = True
                newPipe = pipeModule.Pipe(size[0], size[1])
                pipesOnScreen.append(newPipe)
            if(pipes.getXRight() < 0):
                pipesOnScreen.remove(pipes)

        """ deal with moving the pipes..."""
        dist_to_closest_pipe = 9999999
        # determine closest pipe
        for pipe in pipesOnScreen:

            dist_to_pipe = pipe.getXRight() - birds[0].rect.x

            # barely detect the pipe going behind bird (can still hit pipe)
            if dist_to_pipe >= 0:

                if dist_to_pipe < dist_to_closest_pipe:

                    dist_to_closest_pipe = dist_to_pipe
                    closest_pipe = pipe

        for pipe in pipesOnScreen:
            currentPipe = pipe
            cpx = currentPipe.getX()
            cpty = currentPipe.getTopY() #current pipe, top pipe's bottom y
            cpby = currentPipe.getBottomY() # current pipe, bottom pipe's top y
            if int(slider.val) < 10:
                pygame.draw.rect(screen, WHITE, (cpx, 0, 50, cpty)) #(x, y, width (Top left -> top right), height (top left to bottom))
                pygame.draw.rect(screen, WHITE, (cpx, cpby, 50, size[1] - cpby))
            currentPipe.setX(currentPipe.getX()-2)

            # only ever check hits and have bird worry about the closest pipe... BIG SPEED UP
            if pipe == closest_pipe:
                for bird in birds:
                    if(currentPipe.hits(bird)):
                        savedBirds.append(bird) # add bird for saving before we delete it
                        birds.remove(bird)
                        all_sprites.remove(bird)
                    else:
                        bird.think(pipesOnScreen)

        # reset game and create next generation of birds
        if not birds:
            birds = nextGeneration(totalBirds, savedBirds)
            savedBirds = []
            all_sprites.add(birds)              # add new birds to sprite group
            current_generation += 1
            score = 0
            pipesOnScreen = []                  # remove pipes off of screen, like resetting game

        #update sprites
        all_sprites.update()

    """ begin drawing stuff... excluding pipes because it's stuck where it is """
    if slider.hit:
        slider.move()

    slider.draw(screen)

    #score counter
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render("score :" + str(score), True, (255, 255, 2))
    textsurface2 = myfont.render("generation: " + str(current_generation), True, (255, 255, 2))
    textBirds = myfont.render("total birds: " + str(len(birds)), True, (255, 255, 2))
    screen.blit(textsurface,(50,50))
    screen.blit(textsurface2, (50, 75))
    screen.blit(textBirds, (50, 100))

    #draw
    for bird in birds:
        screen.blit(bird.image, bird.rect)

    #update display
    pygame.display.update()
    clock.tick(fps)

# Be IDLE friendly
pygame.quit()
