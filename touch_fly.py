import pygame
import sys

BLACK = (  0,  0,  0)
WHITE = (255,255,255)
BLUE  = (  0,  0,255)
GREEN = (  0,255,  0)
RED   = (255,  0,  0)
GREY  = (128,128,128)

WIDTH = 750
HEIGHT = 1000
size = [WIDTH, HEIGHT]

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("touch_fly")
clock = pygame.time.Clock()

FPS = 60

images = {\
    "sky":pygame.image.load("images/sky.png"),\
    "l0":pygame.image.load("images/l0.png"),\
    "l1":pygame.image.load("images/l1.png"),\
    "l2":pygame.image.load("images/l2.png"),\
    "l3":pygame.image.load("images/l3.png"),\
    "r0":pygame.image.load("images/r0.png"),\
    "r1":pygame.image.load("images/r1.png"),\
    "r2":pygame.image.load("images/r2.png"),\
    "r3":pygame.image.load("images/r3.png")\
}

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y
    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False

def getHitMask(img):
    mask = []
    for x in range(img.get_width()):
        mask.append([])
        for y in range(img.get_height()):
            mask[x].append(bool(img.get_at((x,y))[3]))
    return mask

def drawObject(obj,x,y):
    screen.blit(obj,(x,y))

class ball:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.v_x = 0
        self.v_y = 0
        self.a_x = 0
        self.a_y = -0.98
        self.h = 0
        self.die = False
        self.ix = 0
        
    def move(self):
        self.v_x += self.a_x
        self.v_y += self.a_y
        self.x += self.v_x
        self.y -= self.v_y
        
        if self.x + 100 > WIDTH or self.x < 0:
            #self.v_x *= -1
            self.die = True
        
        self.y += 5
            
    def render(self):
        #pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), self.r)
        if self.v_x > 0:
            drawObject(images["r"+str(self.ix)], self.x, self.y)
        else:
            drawObject(images["l"+str(self.ix)], self.x, self.y)
        self.ix = (self.ix + 1) % 4

b = ball()
v = 15
start = False
back_y1 = 0
back_y2 = -HEIGHT
back1 = images["sky"]
back2 = back1.copy()
 

while not b.die:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_LEFT:
                b.v_x, b.v_y = -v, v
            if event.key == pygame.K_RIGHT:
                b.v_x, b.v_y = v, v
            if event.key == pygame.K_z:
                start = True
    back_y1 += 2
    back_y2 += 2
    screen.fill(WHITE)
    drawObject(back1, 0, back_y1)
    drawObject(back2, 0, back_y2)
    if back_y1 > HEIGHT:
        back_y1 = 0
    if back_y2 == 0:
        back_y2 = -HEIGHT
    if not start:
        continue
    
    b.move()
    b.render()
            
    pygame.display.update()
    clock.tick(FPS)

print("gameover")
pygame.quit()
sys.exit()