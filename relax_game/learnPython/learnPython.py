import pygame
pygame.init()

win = pygame.display.set_mode((500,480))
pygame.display.set_caption("learn Python")

#load sound
#bulletSound = pygame.mixer.Sound("Game/bullet.wav")
#hitSound = pygame.mixer.Sound("Game/hit.wav")

music = pygame.mixer.music.load("Game/music.mp3")
pygame.mixer.music.play(-1)


bg = pygame.image.load('Game/bg.jpg')
char = pygame.image.load('Game/standing.png')
walkRight = [pygame.image.load('Game/R1.png') , pygame.image.load('Game/R2.png'), pygame.image.load('Game/R3.png'), pygame.image.load('Game/R4.png'), pygame.image.load('Game/R5.png'), pygame.image.load('Game/R6.png'), pygame.image.load('Game/R7.png'), pygame.image.load('Game/R8.png'), pygame.image.load('Game/R9.png') ]
walkLeft = [pygame.image.load('Game/L1.png') , pygame.image.load('Game/L2.png'), pygame.image.load('Game/L3.png'), pygame.image.load('Game/L4.png'), pygame.image.load('Game/L5.png'), pygame.image.load('Game/L6.png'), pygame.image.load('Game/L7.png'), pygame.image.load('Game/L8.png'), pygame.image.load('Game/L9.png') ]

dem =0
class projectile(object): # ddanj
    def __init__(self,x,y,radius,color,facing):     #radius = ban kinh
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)

class enemy(object):
    walkRight = [pygame.image.load('Game/R1E.png'), pygame.image.load('Game/R2E.png'), pygame.image.load('Game/R3E.png'),pygame.image.load('Game/R4E.png'), pygame.image.load('Game/R5E.png'), pygame.image.load('Game/R6E.png'),pygame.image.load('Game/R7E.png'), pygame.image.load('Game/R8E.png'), pygame.image.load('Game/R9E.png'),pygame.image.load('Game/R10E.png'), pygame.image.load('Game/R11E.png')]
    walkLeft = [pygame.image.load('Game/L1E.png'), pygame.image.load('Game/L2E.png'), pygame.image.load('Game/L3E.png'),pygame.image.load('Game/L4E.png'), pygame.image.load('Game/L5E.png'), pygame.image.load('Game/L6E.png'),pygame.image.load('Game/L7E.png'), pygame.image.load('Game/L8E.png'), pygame.image.load('Game/L9E.png'),pygame.image.load('Game/L10E.png'), pygame.image.load('Game/L11E.png')]

    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x,end]     # This will define where our enemy starts(at x) and finishes(at end) their path.
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 5, 31 , 55)
        #heath bar
        self.heath = 10
        self.visible = True

    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:        # If we are moving to the right we will display our walkRight images
                win.blit(self.walkRight[self.walkCount//3] , (self.x, self.y))
                self.walkCount +=1
            else:               # Otherwise we will display the walkLeft images
                win.blit(self.walkLeft[self.walkCount //3] , (self.x , self.y))
                self.walkCount +=1
            #draw two rectangle to dai dien cho thnah mau'
            pygame.draw.rect(win,(255,0,0),(self.hitbox[0], self.hitbox[1] - 20,50,10))
            pygame.draw.rect(win,(0,128,0),(self.hitbox[0], self.hitbox[1] - 20, 50 -(5 * (10 -self.heath)), 10))
            #ve mau xanh de len mau do => moi lan bi hit thi thanh mau xanh se ngan di
            self.hitbox = (self.x + 17, self.y + 5, 31 , 55)
            #pygame.draw.rect(win ,(255,0,0),self.hitbox,2)

    def move(self):
        if self.vel > 0:         # If we are moving right
            if self.x < self.path[1] + self.vel:    # # If we have not reached the furthest right point on our path.
                self.x += self.vel
            else:    # Change direction and move back the other way
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:       # If we are moving left
            if self.x > self.path[0] - self.vel:    ## If we have not reached the furthest left point on our path
                self.x += self.vel
            else:
                self.vel = self.vel*-1
                self.x += self.vel
                self.walkCount = 0

    def hit(self):
        global dem
        dem += 1
        if self.heath > 0:
            self.heath -= 1
        else:
            self.visible = False
        print(str(dem) + ' Hit\n')

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.jumpCount = 10
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17 , self.y +11 , 29, 52)   #x,y,width, height
    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not (self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x , self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))    #draw image at x,y
            else:
                win.blit(walkLeft[0],(self.x,self.y))

        self.hitbox = (self.x + 17, self.y + 13, 29, 50)  # NEW
        #pygame.draw.rect(win,(0,0,0),self.hitbox,2) # 2 = viền của HCN. nếu = 0 thì fill  đầy hình

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 100
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255,0,0))
        win.blit(text, (250 - (text.get_width()/2),200))
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 201
                    pygame.quit()

def re_Drawn():
    win.blit(bg,(0,0)) #draw background at 0,0
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    text = font.render("Score: " + str(dem), 1, (0,0,0)) ## Arguments are: text, anti-aliasing, color
    win.blit(text,(10,10))
    pygame.display.update()

clock = pygame.time.Clock()

run = True
man = player(200,400,100,64)
goblin = enemy(0,410,64,64,450)
bullets = []
shootLoop = 0

font = pygame.font.SysFont("comicsnas",30, True)

while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if goblin.visible:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                dem -= 5

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for bullet in bullets:
        if goblin.visible:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:      #check bullet.y co trong hitbox ko
                if bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2] and bullet.x + bullet.radius > goblin.hitbox[0]:  #check bullet.x co trong hitbox ko
                    goblin.hit()
                    bullets.pop(bullets.index(bullet))
        # move bullets
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))   ## This will remove the bullet if it is off the screen

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:        #cannot shoot 5 bullet at once
            bullets.append(projectile(round(man.x + man.width//2),round(man.y + man.height//2), 6, (0,0,0), facing))
            ## This will create a bullet starting at the middle of the character
        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_RIGHT] and man.x <500 - man.vel - man.width:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False

    else: # nhan vat dung yen
        man.standing = True
        man.walkCount = 0

    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if  man.jumpCount >= -10:
            man.y -= (man.jumpCount * abs(man.jumpCount)) * 0.5
            man.jumpCount -= 1
        else:
            man.jumpCount = 10
            man.isJump = False

    re_Drawn()

pygame.quit()