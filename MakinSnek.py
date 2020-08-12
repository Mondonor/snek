import pygame
import random
from random import seed
from random import randint

pygame.init()
key2 = 0
W = 500
H = 500
win = pygame.display.set_mode((W,H))

pygame.display.set_caption("Snek :)")

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

font = pygame.font.Font('freesansbold.ttf', 8)
font2 = pygame.font.Font('freesansbold.ttf', 20)


b = False
x = 40
y = 40
width = 18
height = 18
vel = 20
rate = 17
length = 1
dire = "R"
diretemp = "R"
count = -5
countcond = 10
score = 0
run = True
level = 1
prestige = 0
text = font.render(f'SCORE: {score}  PRESTIGE: {prestige}', True, white)
text1win = font2.render('Congratulations, you beat the game!', True, green)
text2win = font2.render("To play again, press 'space'. To quit, press 9.", True, green)
text1lose = font2.render("You are as likely to be struck by lightning", True, red)
text2lose = font2.render("as you are to achieve your dreams.", True, red)
text3lose = font2.render("Try again with space, 9 to quit.", True, red)
textPause = font2.render("Press 'u' to unpause.", True, white)
textRect = text.get_rect()
textw1 = text1win.get_rect()
textw2 = text2win.get_rect()
textl1 = text1lose.get_rect()
textl2 = text2lose.get_rect()
textl3 = text3lose.get_rect()
textp = textPause.get_rect()
textRect.center = (80, 8)
textw1.center = (int(W/2) , int(H/2) - 75)
textw2.center = (int(W/2) , int(H/2) + 75)
textl1.center = (int(W/2) , int(H/2) - 100)
textl2.center = (int(W/2) , int(H/2))
textl3.center = (int(W/2) , int(H/2) + 100)
textp.center = (int(W/2) , int(H/2))

#To Update GameState:
gamebool = True
winbool = False

#count is used to make sure the square doesn't move every update. it would be way too quick.
#dire is direction, diretemp accepts input from keyboard and updates dire upon refresh of screen.

memlist = [[]]*103
memlist[0] = [x,y]

#this is for storing positions.

xf = 240
yf = 260

#food position
def gamestatereset():
    global x
    global y
    global rate
    global length
    global dire
    global diretemp
    global count
    global countcond
    global score
    global run
    global level
    global gamebool
    global winbool
    global memlist
    global xf
    global yf
    global prestige
    x = 40
    y = 40
    rate = 17
    length = 1
    dire = "R"
    diretemp = "R"
    count = -5
    countcond = 10
    score = 0
    run = True
    level = 1
    gamebool = True
    if winbool == True:
        prestige = prestige + 1
    else:
        prestige = 0
    winbool = False
    memlist = [[]]*103
    memlist[0] = [x,y]
    xf = 240
    yf = 260

def wincond():
    global winbool
    global gamebool
    winbool = True
    gamebool = False

def winScreen():
    global text1win
    global text2win
    global textw1
    global textw2
    win.blit(text1win, textw1)
    win.blit(text2win, textw2)

def losecond():
    global gamebool
    gamebool = False

def loseScreen():
    global text1lose
    global text2lose
    global text3lose
    global textl1
    global textl2
    global textl3
    win.blit(text1lose, textl1)
    win.blit(text2lose, textl2)
    win.blit(text3lose,textl3)

def eat():
    global rate
    global length
    global memlist
    global xf
    global yf
    global score
    global level
    global countcond
    if score == 100:
        wincond()
    length = length + 1
    memlist[length-1] = [x , y]
    xf = randint(1,24) * 20
    yf = randint(1,24) * 20
    while [xf,yf] in memlist:
        xf = randint(1,24) * 20
        yf = randint(1,24) * 20
    score = score + 1
    if score % 10 == 0:
        level = level + 1
        rate = rate - 1
    if score % 20 == 0:
        countcond = countcond - 1

def move():
    global x, y
    #global y
    if dire == "R":
        if x >= 480:
            losecond()
        else:
            x += vel
    if dire == "L":
        if x <= 0:
            losecond()
        else:
            x -= vel
    if dire == "U":
        if y <= 0:
            losecond()
        else:
            y -= vel
    if dire == "D":
        if y >= 480:
            losecond()
        else:
            y += vel

    for i in range(length):
        if i == length - 1:
            memlist[0] = [x,y]
        if i != length - 1:
            memlist[length - i - 1] = memlist[length - i - 2]
    collcheck()


def collcheck():
    global memlist
    for i in range(length):
        if memlist[0] == memlist[i] and i != 0:
            losecond()
            
def dispTEXT():
    global text
    global score
    text = font.render(f'SCORE: {score}  PRESTIGE: {prestige}', True, white)
    win.blit(text,textRect)

def PauseScreen():
    global textPause
    global textp
    global b
    global key2
    win.blit(textPause,textp)
    pygame.display.update()
    key2 = pygame.key.get_pressed()


while run:
    pygame.time.delay(rate)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_p]:
        gamebool = False
        b = True
        PauseScreen()
    
    if keys[pygame.K_u]:
        gamebool = True
        b = False

    if b == True:
        continue
    
    if gamebool == True:
        if keys[pygame.K_LEFT]:
            if dire == "R":
                pass
            else:
                diretemp = "L"
        if keys[pygame.K_RIGHT]:
            if dire == "L":
                pass
            else:
                diretemp = "R"
        if keys[pygame.K_UP]:
            if dire == "D":
                pass
            else:
                diretemp = "U"
        if keys[pygame.K_DOWN]:
            if dire == "U":
                pass
            else:
                diretemp = "D"

    
        if  count <= countcond:
            count = count + 1
        else:
            if memlist[0][0] == xf and memlist[0][1] == yf:
                eat()
            dire = diretemp
            move()
            count = 1
            
        win.fill((0,0,0))
        dispTEXT()
        pygame.draw.rect(win, (255,255,255), (xf + 4, yf + 4,10,10))
        
        for i in range(length):
            if i <= 10:
                A = 255 - 10 * i
                B = 0
                C = 10 * i
            if i > 10 and i <= 20:
                A = 155 - 5 * (i - 10)
                B = 5 * (i - 10)
                C = 100
            if i > 20 and i <= 30:
                A = 105 + (i - 20) * 2
                B = 50 + (i - 20) * 10
                C = 100 + (i - 20) * 10
            if i > 30 and i <= 50:
                A = 125 - (i - 30) * 5
                B = 150 + (i - 30) * 5
                C = 200 + (i - 30) * 1
            if i > 50 and i <= 70:
                A = 24 + (i - 50) * 9
                B = 244 - (i - 50) * 2
                C = 224 - (i - 50)
            if i > 70:
                A = 204 + (i - 70)
                B = A
                C = A
            pygame.draw.rect(win, (A,B,C), (memlist[i][0],memlist[i][1],width,height))
            
    elif winbool == True:
        winScreen()
    else:
        loseScreen()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_y]:
        losecond()
    elif keys[pygame.K_z]:
        wincond()
    
    pygame.display.update()
            
    keys = pygame.key.get_pressed()
    if gamebool == False:
        if keys[pygame.K_9]:
            quit()
        if keys[pygame.K_SPACE]:
            gamestatereset()
        
        

    

pygame.quit()
