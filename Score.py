import pygame

class Score(pygame.sprite.Sprite):
    """A sprite for the score."""

    def __init__(self, xy):
        pygame.sprite.Sprite.__init__(self)

        self.xy = xy

        self.font = pygame.font.Font(None, 50)

        self.leftscore = 0
        self.rightscore = 0
        self.reRender()

    def update(self):
        pass

    def left(self):
        """Adds a point to the left side score."""
        self.leftscore += 1
        self.reRender()

    def right(self):
        """Adds a point to the right side score."""
        self.rightscore += 1
        self.reRender()

    def reset(self):
        """Resets the scores to zero."""
        self.leftscore = 0
        self.rightscore = 0
        self.reRender()

    def reRender(self):
        """Updates the score. Renders a new image and re-centers at the initial coordinates."""
        self.image = self.font.render("%d     %d"%(self.leftscore, self.rightscore), True, (0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = self.xy
