import sys,os
import pygame
from pygame.locals import *
from threading import Thread
import time

from GameControllerServer import GameControllerServer

from Score import Score
from Ball import Ball
from Paddle import Paddle


class NetworkControlledPong(object):
    """Our game object! This is a fairly simple object that handles the
    initialization of pygame and sets up our game to run."""

    def __init__(self):
        """Called when the the Game object is initialized. Initializes
        pygame and sets up our pygame window and other pygame tools
        that we will need for more complicated tutorials."""

        pygame.init()

        self.uiServer = GameControllerServer(self, min_players=2,max_players=2)
        self.paddleMap = {}
        self.leftPaddleFree = True
        self.rightPaddleFree = True
        self.started = False

        self.window = pygame.display.set_mode((800, 400))

        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Pong with Android Controller")

        pygame.event.set_allowed([QUIT, USEREVENT])

        self.background = pygame.Surface((800,400))
        self.background.fill((255,255,255))

        pygame.draw.line(self.background, (0,0,0), (400,0), (400,400), 2)
        self.window.blit(self.background, (0,0))

        pygame.display.flip()

        self.sprites = pygame.sprite.RenderUpdates()

        self.leftpaddle = Paddle((50,200))
        self.sprites.add(self.leftpaddle)
        self.rightpaddle = Paddle((750,200))
        self.sprites.add(self.rightpaddle)

        self.ball = Ball((400,200))
        self.sprites.add(self.ball)

        self.scoreImage = Score((400, 50))
        self.sprites.add(self.scoreImage)

        self.pingsound = pygame.mixer.Sound(os.path.join('sound', 'ping.wav'))
        self.pongsound = pygame.mixer.Sound(os.path.join('sound', 'pong.wav'))

        self.uiThread = Thread(target=self.uiServer.serve)
        self.uiThread.start()

    def addPlayer(self, id):
        if self.leftPaddleFree:
            self.paddleMap[id] = self.leftpaddle
            self.leftPaddleFree = False

        elif self.rightPaddleFree:
            self.paddleMap[id] = self.rightpaddle
            self.rightPaddleFree = False

        else:
            print "No paddle free at the moment"

    def removePlayer(self, id):
        try:
            if self.paddleMap[id] == self.leftpaddle:
                self.leftPaddleFree = True
            elif self.paddleMap[id] == self.rightpaddle:
                self.rightPaddleFree = True
            self.paddleMap[id] = None
        except KeyError:
            print "Controller not registered"

    def start(self):
        self.started = True

    def stop(self):
        self.running = False

    def pause(self):
        self.tmpBallVelY = self.ball.vely
        self.tmpBallVelX = self.ball.velx
        self.ball.vely   = 0
        self.ball.velx   = 0
        self.paused      = True

    def resume(self):
        self.ball.vely = self.tmpBallVelY
        self.ball.velx = self.tmpBallVelX
        self.paused    = False

    def run(self):
        """Runs the game. Contains the game loop that computes and renders
        each frame."""

        print 'Waiting for enough controllers'

        while not self.started:
            if self.handleEvents() == False:
                self.uiServer.stop()
                return 0
            else:
                time.sleep(0)

        print 'Enough controllers registered'
        print 'Starting Event Loop'

        self.running = True
        self.paused  = False

        while self.running:
            self.clock.tick(30)

            self.running = self.handleEvents()

            self.manageBall()

            for sprite in self.sprites:
                sprite.update()

            self.sprites.clear(self.window, self.background)    # clears the window where the sprites currently are, using the background
            dirty = self.sprites.draw(self.window)              # calculates the 'dirty' rectangles that need to be redrawn

            pygame.display.update(dirty)                        # updates just the 'dirty' areas

        print 'Quitting. Thanks for playing'
        self.uiServer.stop()
        return 0

    def handleEvents(self):
        """Poll for PyGame events and behave accordingly. Return false to stop
        the event loop and end the game."""

        for event in pygame.event.get():
            if event.type == QUIT:
                return False

            elif event.type == USEREVENT:
                if self.ball.velx == 0 and self.ball.vely == 0 and not self.paused:
                    self.ball.serve()
                if event.key.lower() == "up":
                    self.paddleMap[event.id].up()
                if event.key.lower() == "down":
                    self.paddleMap[event.id].down()
                if event.key.lower() == "stop":
                    return False

        return True


    def manageBall(self):
        self.ball.rect.x += self.ball.velx
        self.ball.rect.y += self.ball.vely

        if self.ball.rect.top < 0:
            self.ball.rect.top = 1
            self.ball.vely *= -1
            self.pongsound.play()

        elif self.ball.rect.bottom > 400:
            self.ball.rect.bottom = 399
            self.ball.vely *= -1
            self.pongsound.play()

        if self.ball.rect.left < 0:
            self.scoreImage.right()
            self.ball.reset()
            return

        elif self.ball.rect.right > 800:
            self.scoreImage.left()
            self.ball.reset()
            return

        collided = pygame.sprite.spritecollide(self.ball, [self.leftpaddle, self.rightpaddle], dokill=False)

        if len(collided) > 0:
            hitpaddle = collided[0]
            self.ball.velx *= -1
            self.ball.rect.x += self.ball.velx
            self.ball.vely += hitpaddle.velocity/3.0
            self.pingsound.play()


if __name__ == '__main__':
    game = NetworkControlledPong()
    sys.exit(game.run())

