import os
import pygame

class Paddle(pygame.sprite.Sprite):
    def __init__(self, xy):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join('images','pong_paddle.gif'))
        self.rect = self.image.get_rect()

        self.rect.centerx, self.rect.centery = xy

        self.movementspeed = 5

        self.velocity = 0

    def up(self):
        """Increases the vertical velocity"""
        self.velocity -= self.movementspeed

    def down(self):
        """Decreases the vertical velocity"""
        self.velocity += self.movementspeed

    def move(self, dy):
        """Move the paddle in the y direction. Don't go out the top or bottom"""
        if self.rect.bottom + dy > 400:
            self.rect.bottom = 400
        elif self.rect.top + dy < 0:
            self.rect.top = 0
        else:
            self.rect.y += dy

    def update(self):
        """Called to update the sprite. Do this every frame. Handles
        moving the sprite by its velocity"""
        self.move(self.velocity)
