import cv2
import time
import HandTrackingModule as htm
import pygame
import math
import random
from PIL import Image, ImageDraw

# chuyen tu cvimage sang pygame image
def cvimage_to_pygame(image):
    return pygame.image.frombuffer(image.tostring(), image.shape[1::-1], "BGR")

# chuyen tu PIL sang pygame image
def PIL_to_pygame(image):
    return pygame.image.fromstring(image.tobytes(), image.size, image.mode)

# tinh khoang cach giua 2 diem
def distance(point0, point1):
    return math.sqrt((point1[0] - point0[0]) ** 2 + (point1[1] - point0[1]) ** 2)

# chieu rong va chieu cao cua so
wCam = 640
hCam = 480

# khoi tao pygame
pygame.init()
screen = pygame.display.set_mode((wCam,hCam))

# khoi tao camera cua opencv
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

# hand dectector
dectector = htm.handDetector()

# danh sach dich
enemies = []
genTime = 0
enemyRad = 10
enemySpeed = 300
points = 0

random.seed(time.time())

running = True
while running:

    # ------ opencv ------
    # chup hinh tu camera
    success, img = cap.read()
    dectector.findHands(img)

    # ve hinh chu nhat trang
    # img = cv2.rectangle(img, (0, 0), (wCam, hCam), (255, 255, 255), -1)

    # tim vi tri cac diem cua tay
    lmList, bbox = dectector.findPosition(img, draw=False)
    wide = 0
    x4 = y4 = x8 = y8 = 0
    mouth_opened = False
    if len(lmList):
        # print(lmList[4], lmList[8])
        
        # lay cac diem quan trong
        x3, y3 = lmList[3][1], lmList[3][2]
        x4, y4 = lmList[4][1], lmList[4][2]
        x7, y7 = lmList[7][1], lmList[7][2]
        x8, y8 = lmList[8][1], lmList[8][2]

        # vec hinh tron o dinh ngon tro va ngon cai
        cv2.circle(img, (x4, y4), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x8, y8), 15, (255, 0, 255), cv2.FILLED)

        # tinh ti le
        ratio = distance((x3, y3), (x4, y4)) + distance((x7, y7), (x8, y8))

        # tinh khoang cach mieng
        wide = distance((x4, y4), (x8, y8)) / ratio

        # kiem tra mo mieng
        if wide > 1.5:
            mouth_opened = True

    # do fps cua chuong trinh
    cTime = time.time()
    passedTime = cTime - pTime
    fps = 1 / passedTime

    # spawn dich
    genTime -= passedTime
    if genTime <= 0:
        genTime = random.uniform(0.5, 2)
        enemies.append([enemyRad, random.randint(enemyRad + 100, hCam - enemyRad - 100)])

    # gan lai gio
    pTime = cTime

    # dao anh va ghi fps len anh
    img_v = cv2.flip(img, 1)
    cv2.putText(img_v, f'POINTS: {int(points)}', (10, 35), cv2.FONT_HERSHEY_COMPLEX, 1, (109, 55, 25), 2)
    # cv2.putText(img_v, f'FPS: {int(fps)}', (10, 35), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    # ------ PIL ------
    canvas_size = 200
    pil_size = 75

    pil_image = Image.new("RGBA", (canvas_size, canvas_size))
    pil_draw = ImageDraw.Draw(pil_image)
    tmp = wide / 5 * 90

    BLUE = (87, 108, 188)
    PINK = (11, 36, 71)
    LWIDTH = 10

    if y4 != 0 and y8 != 0:
        # ve dau ca
        pil_draw.pieslice(((0, pil_size / 3), (pil_size, pil_size + pil_size / 3)), start = -180 + tmp, end = 180 - tmp, fill=BLUE, outline=PINK, width=LWIDTH)
        # ve than ca
        pil_draw.pieslice(((-pil_size, pil_size / 3), (pil_size * 2, pil_size + pil_size / 3)), start = -90, end = 90, fill=BLUE, outline=PINK, width=LWIDTH)
        # ve duoi ca
        pil_draw.pieslice(((pil_size * 2 - pil_size / 10, pil_size * 2 / 10 + pil_size / 3), (pil_size * 3 - pil_size / 10, pil_size * 8 / 10 + pil_size / 3)), start = -290, end = -70, fill=BLUE, outline=PINK, width=LWIDTH)
        # ve cai phan tam giac phia tren than
        pil_draw.pieslice(((pil_size * 2 / 3, 0), (pil_size * 2 / 3 + pil_size, pil_size)), start = -180, end = -70, fill=BLUE, outline=PINK, width=LWIDTH)
        # ve dau ca
        pil_draw.pieslice(((0, pil_size / 3), (pil_size, pil_size + pil_size / 3)), start = -180 + tmp, end = 180 - tmp, fill=BLUE)
        # ve than ca
        pil_draw.pieslice(((-pil_size, pil_size / 3), (pil_size * 2, pil_size + pil_size / 3)), start = -90, end = 90, fill=BLUE)
        # ve duoi ca
        pil_draw.pieslice(((pil_size * 2 - pil_size / 10, pil_size * 2 / 10 + pil_size / 3), (pil_size * 3 - pil_size / 10, pil_size * 8 / 10 + pil_size / 3)), start = -290, end = -70, fill=BLUE)
        # ve cai phan tam giac phia tren than
        pil_draw.pieslice(((pil_size * 2 / 3, 0), (pil_size * 2 / 3 + pil_size, pil_size)), start = -180, end = -70, fill=BLUE)
        # ve mat ca
        pil_draw.pieslice(((pil_size / 2, pil_size / 2), (pil_size / 2 + pil_size / 10, pil_size / 2 + pil_size / 10)), start = 0, end = 360, fill=PINK)

    # ------ pygame ------
    # hien thi anh cua cam len man hinh game
    screen.blit(cvimage_to_pygame(img_v), (0, 0))
    screen.blit(PIL_to_pygame(pil_image), (wCam - canvas_size, (y4 + y8) / 2 - pil_size / 2 - pil_size / 3))

    BULLET = (165, 215, 232)

    # duyet qua tung dich
    cur_enemies = []
    for enemy in enemies:
        enemy[0] += passedTime * enemySpeed
        pygame.draw.circle(screen, BULLET, enemy, enemyRad)
        if enemy[0] < wCam and \
            not (mouth_opened and enemy[0] > wCam - canvas_size and enemy[0] < wCam - canvas_size + pil_size and \
                enemy[1] > (y4 + y8) / 2 - pil_size / 2 and enemy[1] < (y4 + y8) / 2 - pil_size / 2 + pil_size):
                    cur_enemies.append(enemy)
        elif enemy[0] < wCam:
            points += 1
    enemies = cur_enemies

    # duyet qua cac su kien cua game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # update man hinh game
    pygame.display.update()

    cv2.waitKey(1)

pygame.quit()
