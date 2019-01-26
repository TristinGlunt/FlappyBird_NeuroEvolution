import pygame
import nnet
import numpy as np
import random

# rect objects have (x,y), top, topright, left, center, right bottomleft, bottom, bottomright
import pygame.gfxdraw

FLAP_AMT = -40               # the amount our bird jumps
# the dimensions of the neural network [#inputs, hiddenlayer, outputs]
brain_dims = [5, 5, 1]
ORANGE = (100, 100, 100)
WHITE = (255, 255, 255)


class Bird(pygame.sprite.Sprite):
    def __init__(self, height, parameters):
        # draw.circle is not anti-aliased and looks rather ugly.
        # pygame.draw.circle(ATOM_IMG, (0, 255, 0), (15, 15), 15)
        # gfxdraw.aacircle looks a bit better.
        ATOM_IMG = pygame.Surface((21, 21), pygame.SRCALPHA)
        transparancy = random.randint(150, 230)
        pygame.gfxdraw.aacircle(ATOM_IMG, 10, 10, 10,
                                (0, 120, 150, transparancy))
        # pygame.gfxdraw.filled_circle(ATOM_IMG, 10, 10, 11, WHITE)
        pygame.gfxdraw.filled_circle(
            ATOM_IMG, 10, 10, 10, (0, 120, 150, transparancy))

        pygame.sprite.Sprite.__init__(self)
        # self.picture = pygame.image.load("flappy_bird.png")
        # self.image = pygame.transform.scale(self.picture, (45, 45))

        self.image = ATOM_IMG  # pygame surface you can draw on, 50x50 pixels
        # self.image = self.image.convert_alpha()
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()  # builds rectangle around surface
        # starts bird at 0 x coordinate and middle of screen
        self.rect.center = (100, height/2)
        self.WINDOW_HEIGHT = height
        self.y_before_jump = 35  # max
        self.score = 0  # the min. score (not getting through first pipe)
        self.fitness = 0
        self.velocity = 0

        if parameters == None:
            self.brain = nnet.NeuralNetwork(brain_dims, None)
        else:
            self.brain = nnet.NeuralNetwork(brain_dims, parameters)

    # update sprite
    def update(self):
        self.score += 1
        if(self.rect.bottom < self.WINDOW_HEIGHT):
            self.velocity = 3.5
            self.rect.y += self.velocity  # simulate falling

    def think(self, pipes):

        # initializing closest pipe and dist
        dist_to_closest_pipe = -1
        closest_pipe = pipes[0]

        # determine closest pipe
        for pipe in pipes:
            dist_to_pipe = pipe.getXRight() - self.rect.x
            if dist_to_pipe >= 0:
                if dist_to_pipe < dist_to_closest_pipe:
                    dist_to_closest_pipe = dist_to_pipe
                    closest_pipe = pipe

        inputs = [self.rect.y/self.WINDOW_HEIGHT, closest_pipe.getTopY()/self.WINDOW_HEIGHT,
                  closest_pipe.getBottomY()/self.WINDOW_HEIGHT, closest_pipe.getX()/700, self.velocity/40]

        inputs = np.array(inputs).reshape(-1, 1)  # inputs have to be columns

        # train our network, ie. initialize parameters, would usually tune weights here...
        # self.brain.train(inputs, outputs, 1)
        output = self.brain.predict(inputs)
        # print("Brains output: " + str(output))

        if output > 0.5:
            self.flap()

    def flap(self):
        if self.velocity > 0 and (self.y_before_jump - 22 < self.rect.y):
            self.y_before_jump = self.rect.y
            self.velocity = FLAP_AMT
            self.rect.y += self.velocity

    def mutate(self, mutate_perc):
        self.brain.mutate(mutate_perc, self.score)
