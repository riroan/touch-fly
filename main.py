import pygame, sys
import random, json

BLACK = (  0,  0,  0)
WHITE = (255,255,255)
RED   = (255,  0,  0)
BLUE  = (  0,  0,255)
GREEN = (  0,255,  0)
RED   = (255,  0,  0)
GREY  = (100,100,100)

WIDTH = 750
HEIGHT = 1000
size = [WIDTH, HEIGHT]

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("touch_fly")
clock = pygame.time.Clock()

FPS = 60
cam_y = 0

fonts = {"maple":"asset/Maplestory Bold.ttf",\
         "cookie":"asset/CookieRun Bold.ttf",\
         "Arial":"Arial",\
         "tmon":"asset/TmonMonsori.ttf",\
}

images = {\
    "sky":pygame.image.load("images/sky.png").convert_alpha(),\
    "night_sky":pygame.image.load("images/night_sky.png").convert_alpha(),\
    "l0":pygame.image.load("images/l0.png").convert_alpha(),\
    "l1":pygame.image.load("images/l1.png").convert_alpha(),\
    "l2":pygame.image.load("images/l2.png").convert_alpha(),\
    "l3":pygame.image.load("images/l3.png").convert_alpha(),\
    "r0":pygame.image.load("images/r0.png").convert_alpha(),\
    "r1":pygame.image.load("images/r1.png").convert_alpha(),\
    "r2":pygame.image.load("images/r2.png").convert_alpha(),\
    "r3":pygame.image.load("images/r3.png").convert_alpha(),\
    "thunder0": pygame.image.load("images/thunder0.png").convert_alpha(),\
    "thunder1": pygame.image.load("images/thunder1.png").convert_alpha(),\
    "title":pygame.image.load("images/title.png").convert_alpha(),\
    "play":pygame.image.load("images/play.png").convert_alpha(),\
    "rank":pygame.image.load("images/rank.png").convert_alpha(),\
    "alert":pygame.image.load("images/alert.png").convert_alpha(),\
    "select_level":pygame.image.load("images/select_level.png").convert_alpha(),\
    "easy":pygame.image.load("images/easy.png").convert_alpha(),\
    "normal":pygame.image.load("images/normal.png").convert_alpha(),\
    "hard":pygame.image.load("images/hard.png").convert_alpha(),\
    "crazy":pygame.image.load("images/crazy.png").convert_alpha(),\
    "small_exit":pygame.image.load("images/small_exit.png").convert_alpha(),\
    "small_regame":pygame.image.load("images/small_regame.png").convert_alpha(),\
}
    
level_info = {\
    "easy":[0.025, 8],\
    "normal":[0.03, 10],\
    "hard":[0.06, 10],\
    "crazy":[0.08, 20],\
    }

def p(x):
    return random.random() <= x
    
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

def drawObject(obj,x,y, a = True):
    screen.blit(obj,(x,y - cam_y * a))
    
def drawText(text, path, size, x = 0, y = 0, color = BLACK, align = True):
    font = pygame.font.SysFont(path, size)
    text = font.render(text, 1, color)
    if align:
        pos = text.get_rect(center = (x, y))
        screen.blit(text, pos)
    else:
        screen.blit(text, (x, y))

def updateFPS():
    fps = clock.get_fps()
    drawText("FPS : " + str(fps), fonts["Arial"], 18, align = False)
    
class player:
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
        self.l_images = [images["l" + str(i)] for i in range(4)]
        self.r_images = [images["r" + str(i)] for i in range(4)]
        self.l_mask = [getHitMask(i) for i in self.l_images]
        self.r_mask = [getHitMask(i) for i in self.r_images]
        
    def move(self):
        self.v_x += self.a_x
        self.v_y += self.a_y
        self.x += self.v_x
        self.y -= self.v_y
        
        if self.x + 100 > WIDTH or self.x < 0 or self.y > HEIGHT:
            self.die = True
        
        self.y += 3
        if self.y <= cam_y:
            self.y = cam_y
            
    def render(self):
        if self.v_x > 0:
            drawObject(self.r_images[self.ix], self.x, self.y)
        else:
            drawObject(self.l_images[self.ix], self.x, self.y)
        self.ix = (self.ix + 1) % 4
        drawText(str(-int(self.y) + HEIGHT // 2 + 505) + "m",fonts["maple"], 40, WIDTH / 2.2, 10, (50,50,50), False)

class thunder:
    def __init__(self):
        self.x = random.randrange(25, WIDTH - 25)
        self.y = cam_y
        self.ix = 0
        self.v = 10
        self.images = [images["thunder0"], images["thunder1"]]
        self.mask = [getHitMask(i) for i in self.images]
    
    def move(self):
        self.y += self.v
        
    def render(self):
        drawObject(self.images[self.ix], self.x, self.y)
        self.ix = (self.ix + 1) % 2
        
    def collision(self, bird):
        if bird.v_x > 0:
            b_mask = bird.r_mask[bird.ix]
        else:
            b_mask = bird.l_mask[bird.ix]
        t_mask = self.mask[self.ix]
        rect_b = pygame.Rect(bird.x, bird.y, 100,100)
        rect_t = pygame.Rect(self.x, self.y, 50, 66)
        return pixelCollision(rect_b, rect_t, b_mask, t_mask)
        
    def isOut(self):
        return self.y - cam_y > HEIGHT
    
def index():
    level = None
    flag = False
    l_flag = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[0] >= 150 and pos[0] <= 350 and pos[1] >= 850 and pos[1] <= 950:
                    flag = True
                if pos[0] >= 400 and pos[0] <= 600 and pos[1] >= 850 and pos[1] <= 950:
                    l_flag = True

        drawObject(images["sky"], 0, 0)
        drawObject(images["title"], 100, 120)
        drawObject(images["play"], 150, 850)
        drawObject(images["rank"], 400, 850)
               
        if l_flag:
            l = select_level()
            if l:
                show_score(level = l)
            else:
                l_flag = False
                continue
        
        if flag:
            if not level:
                level = select_level()
                if not level:
                    flag = False
                    continue
            score = play(level)
            flag = show_score(True, score, level)
        if not flag:
            level = None
        
        pygame.display.update()

def play(level):
    global cam_y
    back1 = images["sky"]
    back2 = back1.copy()
    cam_y = 0
    b = player()
    v = 15
    start = False
    back_y1 = 0
    back_y2 = -HEIGHT
    enemys = []
    while not b.die:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    b.v_x, b.v_y = -v, v
                if event.key == pygame.K_RIGHT:
                    b.v_x, b.v_y = v, v
                if event.key == pygame.K_UP:
                    b.v_x, b.v_y = b.v_x / 10000, v
                if not start:
                    start = True
        if not start:
            drawObject(back1, 0, 0)
            drawText("press any key to start!!", fonts["tmon"], 70, WIDTH / 2, HEIGHT / 2, (102, 38, 21))
            pygame.display.update()
            clock.tick()
            continue
        
        cam_y += (b.y - cam_y - HEIGHT / 2) / 60
        
        back_y1 += 2
        back_y2 += 2
        if back_y1 - cam_y > HEIGHT:
            back_y1 = cam_y
        if back_y2 > cam_y:
            back_y2 = -HEIGHT + cam_y
        drawObject(back1, 0, back_y1)
        drawObject(back2, 0, back_y2)
    
        if p(level_info[level][0]) and len(enemys) < level_info[level][1]:
            enemys.append(thunder())
        
        for e in enemys:
            e.move()
            e.render()
            if e.collision(b):
                print("you die")
                b.die = True
            if e.isOut():
                try:
                    enemys.remove(e)
                except:
                    pass
        
        b.move()
        b.render()
        updateFPS()
        pygame.display.update()
        clock.tick(FPS)
    
    print("your height is " + str(-int(b.y) + HEIGHT // 2 + 505))
    print("gameover")
    return -int(b.y) + HEIGHT // 2 + 505

def select_level():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[0] >= 275 and pos[0] <= 475 and pos[1] >= 300 and pos[1] <= 400:
                    return "easy"
                if pos[0] >= 275 and pos[0] <= 475 and pos[1] >= 450 and pos[1] <= 550:
                    return "normal"
                if pos[0] >= 275 and pos[0] <= 475 and pos[1] >= 600 and pos[1] <= 700:
                    return "hard"
                if pos[0] >= 275 and pos[0] <= 475 and pos[1] >= 750 and pos[1] <= 850:
                    return "crazy"
                if pos[0] >= 550 and pos[0] <= 700 and pos[1] >= 900 and pos[1] <= 975:
                    return False
        
        drawObject(images["sky"], 0, 0)
        drawObject(images["select_level"], 225, 150)
        drawObject(images["easy"], 275, 300)
        drawObject(images["normal"], 275, 450)
        drawObject(images["hard"], 275, 600)
        drawObject(images["crazy"], 275, 750)
        drawObject(images["small_exit"], 550, 900)
        pygame.display.update()
        
def show_score(summary = False, score = 0, level = "easy"):
    global cam_y
    cam_y = 0
    with open("scores.json", "r") as f:
        data = json.load(f)
        best_scores = [i[1] for i in data[level].items()]
    best_scores.append(score)
    best_scores.sort(reverse=True)
    best_scores = best_scores[:5]
    for i, v in enumerate(best_scores):
        data[level][str(i + 1)] = v
    with open("scores.json","w", encoding = "utf-8") as f:
        json.dump(data, f)
    while True:
        color = BLACK
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[0] >= 370 and pos[0] <= 520 and pos[1] >= 900 and pos[1] <= 975 and summary:
                    return True
                if pos[0] >= 550 and pos[0] <= 700 and pos[1] >= 900 and pos[1] <= 975:
                    return False
        
        drawObject(images["sky"], 0, 0)
        drawText("Best Score",fonts["maple"],70, WIDTH / 2, HEIGHT / 6.5, color)
        drawText("(" + level + ")", fonts["maple"], 30, WIDTH / 2, HEIGHT / 5.5, (100,100,100))
        drawText("Rank",fonts["cookie"], 40, WIDTH / 5.3,  HEIGHT / 3.5, color)
        drawText("Score",fonts["cookie"], 40, WIDTH / 1.7, HEIGHT / 3.5, color)
        pygame.draw.line(screen, (100,100,100), [WIDTH * 0.1, HEIGHT / 3], [WIDTH * 0.9, HEIGHT / 3], 2)
        pygame.draw.line(screen, (100,100,100), [WIDTH * 0.3, HEIGHT / 4], [WIDTH * 0.3, HEIGHT / 1.4], 2)
        
        for i in range(5):
            color = BLACK
            if score == best_scores[i] and score:
                color = RED
            drawText(str(i + 1),fonts["cookie"],40, WIDTH / 5.3, 390 + 70 * i, color)
            drawText(str(best_scores[i]) + "m",fonts["cookie"],40, WIDTH / 1.7, 390 + 70 * i, color)
            
        if summary:
            drawText("Your Score : ", fonts["maple"], 60, WIDTH / 3, HEIGHT / 1.25, BLACK)
            drawText(str(score) + "m", fonts["maple"], 60, WIDTH / 1.6, HEIGHT / 1.25, BLACK)
            drawObject(images["small_regame"], 370, 900)
            
        drawObject(images["small_exit"], 550, 900)
        pygame.display.update()
      
if __name__ == "__main__":
    index()