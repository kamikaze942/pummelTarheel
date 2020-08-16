import os, pygame
from pygame.sprite import Sprite
from pygame.locals import *
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        # print 'Cannot load image:', fullname
        print('cannot load impage of chimp')
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class Chimp(Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    def __init__(self):
        super().__init__()
        
        self.init()
        
    def update(self):
        "walk or spin, depending on the monkeys state"
        self.timer()
        if self.dizzy:
            self._spin()
        else:
            self._walk()
        if self.scale:
            self._scale()

    def _walk(self):
        "move the monkey across the screen, and turn at the ends"
        newpos = self.rect.move((self.move, 0))
        if self.rect.left < self.area.left or \
            self.rect.right > self.area.right:
            self.move = -self.move
            newpos = self.rect.move((self.move, 0))
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = newpos

    def _spin(self):
        "spin the monkey image"
        center = self.rect.center
        self.dizzy = self.dizzy + 24
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        "this will cause the monkey to start spinning"
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image
        self.scale = 1
        self.width = self.width + 1
        if self.width > 5:
            self.scale = 0

    def _scale(self):
        scale = pygame.transform.scale
        self.image = scale(self.image, (self.rect.width - (4 * self.width), self.rect.height - (4 * self.width)))

    def counter(self):
        self.cnt = self.cnt + 1

    def timer(self):
        self.time = pygame.time.get_ticks()	/ 1000
  
    def init(self):
        self.image, self.rect = load_image('tylerhead.bmp', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.move = 9
        self.dizzy = 0
        self.scale = 0
        self.cnt = 0
        self.width = 0
        self.time = 0

  