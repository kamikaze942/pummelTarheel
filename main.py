#!/usr/bin/env python
"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""


#Import Modules
import os, pygame
from pygame.locals import *
from Fist import Fist
from chimp import Chimp
if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')


#functions to create our resources

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:')
        # print('Cannot load sound:', fullname)
        raise SystemExit(message)
    return sound




      
def setText(background, cnt):
    if pygame.font:
        font = pygame.font.Font(None, 36)
        tmp = "You've pummeled the Tarheel " + str(cnt)+" times"
        text = font.render(tmp, 1, (255, 255, 255))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)
        pygame.display.flip()

def setTimer(background, cnt):
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render(str(cnt/1000), 1, (255, 255, 255))
        textpos = text.get_rect(centerx=background.get_width() - 10, centery=background.get_height() - 65)
        background.blit(text, textpos)
        pygame.display.flip()


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Punch the Tarheel')
    pygame.mouse.set_visible(0)

#Create The Backgound
    cameron_image = os.path.join("data","cameron.bmp")
    my_image = pygame.image.load(cameron_image)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.blit(my_image, (0,0))

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Prepare Game Objects
    clock = pygame.time.Clock()
    whiff_sound = load_sound('doh.wav')
    punch_sound = load_sound('girlscream.wav')
    chimp = Chimp()
    fist = Fist()
    allsprites = pygame.sprite.RenderPlain((fist, chimp))
    timeOld = 0
#Main Loop
    while 1:
        #clock.tick(600)
        time = pygame.time.get_ticks()


        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    return
                elif event.key == K_r:
                    return
                    #return

                elif event.key == K_e:
                    chimp.init()
                    timeOld = pygame.time.get_ticks()
                    #replay
                    

            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    chimp.counter()
                    background.blit(my_image, (0,0))
                    #setText(background, chimp.cnt)
                    punch_sound.play() #punch
                    chimp.punched()
                else:
                    whiff_sound.play() #miss
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()


        if (time-timeOld)/1000 > 180:
            return

        allsprites.update()
        background.blit(my_image, (0,0))
        setTimer(background, time-timeOld)
        setText(background, chimp.cnt)
                    
    #Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
