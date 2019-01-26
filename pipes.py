import pygame
import random

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, height):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.height = height
        ranNum = random.uniform(0.1, 0.9)
        space = 75 #100 * ranNum
        self.topY = 300 * ranNum
        self.bottomY = self.topY + space
        self._lessThanX = False

    def getX(self):
        return self.x

    def getXRight(self):
        return self.x + 50

    def getY(self):
        return self.y

    def getTopY(self):
        return self.topY

    def getBottomY(self):
        return self.bottomY

    def setX(self, x):
        self.x = x

    @property
    def lessThanX(self):
        return self._lessThanX

    @lessThanX.setter
    def lessThanX(self, bool):
        self._lessThanX = bool

    @lessThanX.deleter
    def lessThanX(self):
        del self._lessThanX

    def hits(self, bird):
        # adding/subtracting 3 because of flappy birds shape
        if(((bird.rect.top+5) < self.topY) or ((bird.rect.bottom-5) > self.bottomY)):
            if(bird.rect.x > self.x and bird.rect.x < self.x + 50): #TODO UPDATE WITH PARAM
                return True
        # not a hit on a pipe, but the bottom of the scree... just doing all hit detection here
        if(bird.rect.bottom > self.height or bird.rect.bottom == self.height or (bird.rect.top == 0 or bird.rect.top < 0)):
            return True
