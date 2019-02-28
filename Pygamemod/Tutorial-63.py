import pygame,pyganim
from pygame.locals import *
import sys
#import os
#sys.path.append(os.path.abspath('..'))


pygame.init()

# set up the window
windowSurface = pygame.display.set_mode((500, 480), 0, 32)
pygame.display.set_caption('Sprite Sheet with Pyganim Demo')

# create the animation objects

bulletSound = pygame.mixer.Sound('pistol.wav')
hitSound = pygame.mixer.Sound('hit.wav')

class player():
    def __init__(self,name,x,y,width,height,end):
        self.name = name
        self.x = x
        self.y= y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.dir = "right"
        self.still = True
        self.totalHit = 0
        self.hp = 10
        self.visible = True
        self.spawn = 0

        self.hitbox = (self.x + 14, self.y, 22, 60)
        self.path = [x, end]

        self.Leftwalk = [(  0, 576, 64, 64),
                      ( 64, 576, 64, 64),
                      (128, 576, 64, 64),
                      (192, 576, 64, 64),
                      (256, 576, 64, 64),
                      (320, 576, 64, 64),
                      (384, 576, 64, 64),
                      (448, 576, 64, 64),
                      (512, 576, 64, 64)]

        self.Rightwalk = [(  0, 704, 64, 64),
                       ( 64, 704, 64, 64),
                       (128, 704, 64, 64),
                       (192, 704, 64, 64),
                       (256, 704, 64, 64),
                       (320, 704, 64, 64),
                       (384, 704, 64, 64),
                       (448, 704, 64, 64),
                       (512, 704, 64, 64)]

        self.Upwalk = [(  0, 512, 64, 64),
                       ( 64, 512, 64, 64),
                       (128, 512, 64, 64),
                       (192, 512, 64, 64),
                       (256, 512, 64, 64),
                       (320, 512, 64, 64),
                       (384, 512, 64, 64),
                       (448, 512, 64, 64),
                       (512, 512, 64, 64)]

        self.Downwalk = [(  0, 640, 64, 64),
                       ( 64, 640, 64, 64),
                       (128, 640, 64, 64),
                       (192, 640, 64, 64),
                       (256, 640, 64, 64),
                       (320, 640, 64, 64),
                       (384, 640, 64, 64),
                       (448, 640, 64, 64),
                       (512, 640, 64, 64)]

        self.StandingRight = [(  0, 704, 64, 64)]
        self.StandingLeft = [(  0, 576, 64, 64)]
        self.StandingUp = [(  0, 512, 64, 64)]
        self.StandingDown = [(  0, 640, 64, 64)]

        self.allplayerLeft = pyganim.getImagesFromSpriteSheet(self.name + '.png', rects=self.Leftwalk)
        self.playerframesLeft = list(zip(self.allplayerLeft, [100] * len(self.allplayerLeft)))
        self.allplayerRight = pyganim.getImagesFromSpriteSheet(self.name + '.png', rects=self.Rightwalk)
        self.playerframesRight = list(zip(self.allplayerRight, [100] * len(self.allplayerRight)))
        self.allplayerUp = pyganim.getImagesFromSpriteSheet(self.name + '.png', rects=self.Upwalk)
        self.playerframesUp = list(zip(self.allplayerUp, [100] * len(self.allplayerUp)))
        self.allplayerDown = pyganim.getImagesFromSpriteSheet(self.name + '.png', rects=self.Downwalk)
        self.playerframesDown = list(zip(self.allplayerDown, [100] * len(self.allplayerDown)))

        #self.allplayerStanding = pyganim.getImagesFromSpriteSheet(self.name + '.png', rects=self.Standing)
        self.allplayerStandingRight = pyganim.getImagesFromSpriteSheet(self.name + '.png', rects=self.StandingRight)
        self.allplayerStandingLeft = pyganim.getImagesFromSpriteSheet(self.name + '.png', rects=self.StandingLeft)
        self.allplayerStandingUp = pyganim.getImagesFromSpriteSheet(self.name + '.png', rects=self.StandingUp)
        self.allplayerStandingDown = pyganim.getImagesFromSpriteSheet(self.name + '.png', rects=self.StandingDown)
        #self.playerframesStanding = list(zip(self.allplayerStanding, [100] * len(self.allplayerStanding)))
        self.playerframesStandingRight = list(zip(self.allplayerStandingRight, [100] * len(self.allplayerStandingRight)))
        self.playerframesStandingLeft = list(zip(self.allplayerStandingLeft, [100] * len(self.allplayerStandingLeft)))
        self.playerframesStandingUp = list(zip(self.allplayerStandingUp, [100] * len(self.allplayerStandingUp)))
        self.playerframesStandingDown = list(zip(self.allplayerStandingDown, [100] * len(self.allplayerStandingDown)))

        self.AnimLeft = pyganim.PygAnimation(self.playerframesLeft)
        self.AnimLeft.play() # there is also a pause() and stop() method
        self.AnimRight = pyganim.PygAnimation(self.playerframesRight)
        self.AnimRight.play() # there is also a pause() and stop() method
        self.AnimUp = pyganim.PygAnimation(self.playerframesUp)
        self.AnimUp.play() # there is also a pause() and stop() method
        self.AnimDown = pyganim.PygAnimation(self.playerframesDown)
        self.AnimDown.play() # there is also a pause() and stop() method

        self.StillRight = pyganim.PygAnimation(self.playerframesStandingRight)
        self.StillLeft = pyganim.PygAnimation(self.playerframesStandingLeft)
        self.StillUp = pyganim.PygAnimation(self.playerframesStandingUp)
        self.StillDown = pyganim.PygAnimation(self.playerframesStandingDown)
        #self.Standing = pyganim.PygAnimation(self.StandingRight)
        self.StillRight.play() # there is also a pause() and stop() method
        self.StillLeft.play() # there is also a pause() and stop() method
        self.StillUp.play() # there is also a pause() and stop() method
        self.StillDown.play() # there is also a pause() and stop() method

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
        else:
            if self.x > self.path[0] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
        
    def draw(self, windowSurface,isEnemy):
        if self.visible:
            if isEnemy:
                self.move()
                if self.vel > 0:
                    self.AnimRight.blit(windowSurface, (self.x,self.y))
                else:
                    self.AnimLeft.blit(windowSurface, (self.x,self.y))
            else:
                if not (self.still):
                    if self.dir == "left":
                        self.AnimLeft.blit(windowSurface, (self.x,self.y))
                    elif self.dir == "right":
                        self.AnimRight.blit(windowSurface, (self.x,self.y))
                    elif self.dir == "up":
                        self.AnimUp.blit(windowSurface, (self.x,self.y))
                    elif self.dir == "down":
                        self.AnimDown.blit(windowSurface, (self.x,self.y))
                else:
                    if self.dir == "right":
                        self.StillRight.blit(windowSurface, (self.x,self.y))
                    elif self.dir == "left":
                        self.StillLeft.blit(windowSurface, (self.x,self.y))
                    elif self.dir == "up":
                        self.StillUp.blit(windowSurface, (self.x,self.y))
                    elif self.dir == "down":
                        self.StillDown.blit(windowSurface, (self.x,self.y))

            pygame.draw.rect(windowSurface, (255,0,0), (self.hitbox[0] - 20, self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(windowSurface, (0,128,0), (self.hitbox[0] - 20, self.hitbox[1] - 20, 50 - ((50/10) * (10 - self.hp)), 10))
            self.hitbox = (self.x + 20, self.y, 28, 60)
            #pygame.draw.rect(windowSurface, (0,255,0), self.hitbox, 2)
    
        pygame.display.update()

    def hit(self):
        if self.hp > 0:
            hitSound.play()
            self.totalHit += 1
            self.hp -= 1
        else:
            self.visible = False


class projectile():
    def __init__(self,x,y,radius,color,facing,direction):
        self.x = x
        self.y= y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,windowSurface):
        if self.direction == "x":
            pygame.draw.circle(windowSurface, self.color, (self.x,self.y),self.radius)
        else:
            pygame.draw.circle(windowSurface, self.color, (self.y,self.x),self.radius)




mainClock = pygame.time.Clock()

bg = pygame.image.load('bg.jpg')

def redrawGameWindow():

    windowSurface.blit(bg, (0,0))
    text=font.render('Score: ' + str(orc.totalHit), 1, (0,0,0))
    windowSurface.blit(text, (190,0))
    #hero.draw(windowSurface)
    hero.draw(windowSurface,False)
    orc.draw(windowSurface,True)
    
    for bullet in bullets:
        bullet.draw(windowSurface)
        
    pygame.display.update()




#mainloop
hero = player("heroarmor",50,400,64,64,0)
orc = player("orcsprite",100,400,64,64,300)
font = pygame.font.SysFont('arial', 30)
isShooting = 0
bullets = []

while True:
    windowSurface.blit(bg, (0,0))

    #text=font.render('Score: ' + str(hero.totalHit), 1, (0,0,0))
    #windowSurface.blit(text, (190,0))

    if isShooting > 0:
        isShooting += 1
    if isShooting > 8:
        isShooting = 0

    #this just checks for quitting
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    for bullet in bullets:
        if bullet.y - bullet.radius < orc.hitbox[1] + orc.hitbox[3] and bullet.y + bullet.radius > orc.hitbox[1]:
            if bullet.x + bullet.radius > orc.hitbox[0] and bullet.x - bullet.radius < orc.hitbox[0] + orc.hitbox[2]:
                orc.hit()
                if orc.hp > 0:
                    bullets.pop(bullets.index(bullet))
                
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
             bullets.pop(bullets.index(bullet))

    if not orc.visible:
        if orc.spawn == 0:
            orc.spawn = 20
        if orc.spawn > 1:
            orc.spawn -= 1
        elif orc.spawn == 1:
            orc.spawn = 0
            orc = player("orcsprite",200,400,64,64,300)

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE] and isShooting == 0:
        if hero.dir == "left":
            direction = "x"
            facing = -1
        elif hero.dir == "right":
            direction = "x"
            facing = 1
        elif hero.dir == "up":
            direction = "y"
            facing = -1
        elif hero.dir == "down":
            direction = "y"
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(hero.x + hero.width //2), round(hero.y + hero.height//2), 6, (0,0,0), facing, direction))
            bulletSound.play()

        isShooting = 1            

    if keys[pygame.K_LEFT] and hero.x > hero.vel:
        hero.x -= hero.vel
        hero.dir = "left"
        hero.still = False


    elif keys[pygame.K_RIGHT] and hero.x < 500 - hero. width - hero.vel:
        hero.x += hero.vel
        hero.dir = "right"
        hero.still = False

    elif keys[pygame.K_UP] and hero.y > 0:
        hero.y -= hero.vel
        hero.dir = "up"
        hero.still = False

    elif keys[pygame.K_DOWN] and hero.y < 480:
        hero.y += hero.vel
        hero.dir = "down"
        hero.still = False

    else:

        hero.still = True


    redrawGameWindow()

    mainClock.tick(30) # Feel free to experiment with any FPS setting.
