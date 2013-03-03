import math, os, random
import pygame

class Ball(pygame.sprite.Sprite):
    """A ball sprite. Subclasses the pygame sprite class."""

    def __init__(self, xy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images','pong_ball.gif'))
        self.rect = self.image.get_rect()

        self.rect.centerx, self.rect.centery = xy
        self.maxspeed = 10
        self.servespeed = 5
        self.velx = 0
        self.vely = 0

    def reset(self):
        """Put the ball back in the middle and stop it from moving"""
        self.rect.centerx, self.rect.centery = 400, 200
        self.velx = 0
        self.vely = 0

    def serve(self):
        angle = random.randint(-45, 45)

        # if close to zero, adjust again
        if abs(angle) < 5 or abs(angle-180) < 5:
            angle = random.randint(10,20)

        # pick a side with a random call
        if random.random() > .5:
            angle += 180

        # do the trig to get the x and y components
        x = math.cos(math.radians(angle))
        y = math.sin(math.radians(angle))

        self.velx = self.servespeed * x
        self.vely = self.servespeed * y

