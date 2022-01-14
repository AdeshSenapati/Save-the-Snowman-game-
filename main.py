import time
import cv2
import HandTrackingModule as htm
import pygame
import random
from pygame import mixer

# initialize pygame always for creating a game
pygame.init()

# screen size
size = width, height = 640, 480
screen = pygame.display.set_mode(size)

##############################
wCam, hCam = 1080, 940
##############################
pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)  # video object created
cap.set(3, wCam)
cap.set(4, hCam)

# background
background = pygame.image.load('scenery.jpg').convert_alpha()

# background song
mixer.music.load('background_song.mp3')
mixer.music.play(-1)
game_over_sound = mixer.Sound('Game_Over.mp3')
game_over_sound.set_volume(0.5)

# screen/window name and icon
pygame.display.set_caption("Save the Snowman")
icon = pygame.image.load('snowman.png').convert_alpha()
pygame.display.set_icon(icon)
pixel = 32
score_value = 0
textX = 10
textY = 10
endX = 100
endY = 200
font = pygame.font.Font(None, 32)
end_font = pygame.font.Font(None, 80)
# player
playerImg = pygame.image.load('snowman.png').convert_alpha()
playerX = 300
playerY = 400
playerX_change = 0

num = 10
enemy1Img = []
enemy1X = []
enemy1Y = []
enemy1Y_change = []

enemy2Img = []
enemy2X = []
enemy2Y = []
enemy2Y_change = []

enemy3Img = []
enemy3X = []
enemy3Y = []
enemy3Y_change = []

saviorImg = []
saviorX = []
saviorY = []
saviorY_change = []
# enemy
for i in range(num):
    random_value = random.randint(0, 200)
    enemy1Img.append(pygame.image.load('missile.png').convert_alpha())
    enemy1X.append(random.randint(0, 608))
    enemy1Y.append(-random_value)
    enemy1Y_change.append(4)

    enemy2Img.append(pygame.image.load('nuclear-bomb.png').convert_alpha())
    enemy2X.append(random.randint(0, 608))
    enemy2Y.append(-random_value)
    enemy2Y_change.append(2)

    enemy3Img.append(pygame.image.load('torpedo.png').convert_alpha())
    enemy3X.append(random.randint(0, 608))
    enemy3Y.append(-random_value)
    enemy3Y_change.append(3)

    saviorImg.append(pygame.image.load('savior_missile.png').convert_alpha())
    saviorX.append(random.randint(0, 608))
    saviorY.append(-random_value)
    saviorY_change.append(2)


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy1(x, y, i):
    screen.blit(enemy1Img[i], (x, y))


def enemy2(x, y ,i):
    screen.blit(enemy2Img[i], (x, y))


def enemy3(x, y, i):
    screen.blit(enemy3Img[i], (x, y))


def savior(x, y, i):
    screen.blit(saviorImg[i], (x, y))


def score_board(x, y):
    score = font.render('Score:' + str(int(score_value)), True, (0, 0, 255))
    screen.blit(score, (x, y))


def game_end(x, y):
    over = end_font.render('GAME OVER', True, (0, 0, 255))
    screen.blit(over, (x, y))


def enemy1_crash(i):
    # check conditions
    if playerY < (enemy1Y[i] + pixel):
        if (enemy1X[i] < playerX < (enemy1X[i] + pixel)) or (enemy1X[i] < (playerX + pixel) < (enemy1X[i] + pixel)):
            return True


def enemy2_crash(i):
    # check conditions
    if playerY < (enemy2Y[i] + pixel):
        if (enemy2X[i] < playerX < (enemy2X[i] + pixel)) or (enemy2X[i] < (playerX + pixel) < (enemy2X[i] + pixel)):
            return True


def enemy3_crash(i):
    # check conditions
    if playerY < (enemy3Y[i] + pixel):
        if (enemy3X[i] < playerX < (enemy3X[i] + pixel)) or (enemy3X[i] < (playerX + pixel) < (enemy3X[i] + pixel)):
            return True


def savior_crash(i):
    # check conditions
    if playerY < (saviorY[i] + pixel):
        if (saviorX[i] < playerX < (saviorX[i] + pixel)) or (saviorX[i] < (playerX + pixel) < (saviorX[i] + pixel)):
            return True


# game loop
detector = htm.handDetector(detectionCon=0.7)
running = True
gg = int(time.time())
while running:
    success, img = cap.read()  # this will give frame
    img = detector.findHands(img)
    hand_type, img = detector.get_label(img)
    screen.fill(color=(255, 255, 255))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():  # events
        if event.type == pygame.QUIT:  # quitting event makes the close window of the program work
            running = False

    # when key is pressed on keyboard
    if hand_type == 'Left':
        playerX_change = -15
    elif hand_type == 'Right':
        playerX_change = 15
    else:
        playerX_change = 0


# boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    if playerX >= 608:
        playerX = 608

    for lm in range(num):
        enemy1Y[lm] += enemy1Y_change[lm]
        if enemy1Y[lm] >= 400:
            enemy1X[lm] = random.randint(0, 608)
            enemy1Y[lm] = -32
            score_value = score_value + 1

        enemy2Y[lm] += enemy2Y_change[lm]
        if enemy2Y[lm] >= 400:
            enemy2X[lm] = random.randint(0, 608)
            enemy2Y[lm] = -32
            score_value = score_value + 1

        enemy3Y[lm] += enemy3Y_change[lm]
        if enemy3Y[lm] >= 400:
            enemy3X[lm] = random.randint(0, 608)
            enemy3Y[lm] = -32
            score_value = score_value + 1

        saviorY[lm] += saviorY_change[lm]
        if saviorY[lm] >= 400:
            saviorX[lm] = random.randint(0, 608)
            saviorY[lm] = -32

        enemy1_collision = enemy1_crash(lm)
        enemy2_collision = enemy2_crash(lm)
        enemy3_collision = enemy3_crash(lm)
        savior_collision = savior_crash(lm)
        if enemy1_collision:
            print('enemy1')
            score_value = score_value - 0.1
        elif enemy2_collision:
            print('enemy2')
            score_value = score_value - 0.5
        elif enemy3_collision:
            print('enemy3')
            score_value = score_value - 0.2
        if savior_collision:
            enemy1X[lm] = random.randint(0, 608)
            enemy1Y[lm] = -32
            enemy2X[lm] = random.randint(0, 608)
            enemy2Y[lm] = -32
            enemy3X[lm] = random.randint(0, 608)
            enemy3Y[lm] = -32
            saviorX[lm] = random.randint(0, 608)
            saviorY[lm] = -32
            score_value = score_value + 5
            # print('savior')
        if score_value == 500:
            enemy1Y_change[lm] = enemy1Y_change[lm] + 0.003
            enemy2Y_change[lm] = enemy2Y_change[lm] + 0.003
            enemy3Y_change[lm] = enemy3Y_change[lm] + 0.003
            saviorY_change[lm] = saviorY_change[lm] + 0.002

        if score_value == 1000:
            enemy1Y_change[lm] = enemy1Y_change[lm] + 0.001
            enemy2Y_change[lm] = enemy2Y_change[lm] + 0.001
            enemy3Y_change[lm] = enemy3Y_change[lm] + 0.001
            saviorY_change[lm] = saviorY_change[lm] + 0.001

        enemy1(enemy1X[lm], enemy1Y[lm], lm)
        enemy2(enemy2X[lm], enemy2Y[lm], lm)
        enemy3(enemy3X[lm], enemy3Y[lm], lm)
        savior(saviorX[lm], saviorY[lm], lm)

    ctime = int(time.time())
    if ctime == gg + 6000:
        game_end(endX, endY)
        running = False
# changing positions
    player(playerX, playerY)
    score_board(textX, textY)
    pygame.display.update()
    # on the screen with inbuilt parameters
    # cv2.imshow("Image", img)  # for showing in the webcam to run it
    cv2.waitKey(1)



