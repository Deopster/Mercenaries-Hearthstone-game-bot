from PIL import ImageGrab
import os
import time
import cv2
import numpy as np
from matplotlib import pyplot as plt
from ahk import AHK
from mss import mss
import mss
from ahk.window import Window
ahk = AHK()
global xm
global ym
def screen():
    sct = mss.mss()
    filename = sct.shot(mon=1, output='files/screen.png')
def findgame():
     global win
     win = ahk.win_get(title='Hearthstone')
     if win.exist:
         print("Игра найдена")
         return True
     else:
         print("Игра не найдена")
         return False

def where():
    find_ellement('join_button.png')
    time.sleep(1)
    find_ellement('group.png')
    find_ellement('back.png')
    return True
def group_create():
    if find_ellement('group_find.png') ==6:
        find_ellement('create.png')
        time.sleep(1)
        find_ellement('rename.png')
        ahk.send_input('Botwork')
        if find_ellement('deff.png'):
            find_ellement('drop.png')
        find_ellement('page_2.png')
        find_ellement('next.png')
        if find_ellement('tiranda.png'):
            find_ellement('drop.png')
        find_ellement('page_3.png')
        if find_ellement('milhaus.png'):
            find_ellement('drop.png')
        find_ellement('ready.png')
        find_ellement('continue.png')
        find_ellement('page_1.png')
        group_create()
    else:
        i=0
        while i<3:
            if find_ellement('one.png') !=5:
                find_ellement('drop.png')
                i+=1
            else:
                find_ellement('next.png')

        find_ellement('ready.png')

def find_ellement(file):
    time.sleep(0.5)
    screen()
    img = cv2.imread('files/screen.png')  # картинка, на которой ищем объект
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # преобразуем её в серуюш
    template = cv2.imread("files/"+file,cv2.IMREAD_GRAYSCALE)  # объект, который преобразуем в серый, и ищем его на gray_img
    w, h = template.shape[::-1]  # инвертируем из (y,x) в (x,y)

    result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= 0.8)
    # рисует прямоугольник вокруг объекта
    if len(loc[0]) !=0:
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 1, 0), 3)
        x=(pt[0]*2+w)/2
        y=(pt[1]*2+h)/2
        print("Обнаружен "+file,x,y)
        if (file == "deff.png" or file == 'tiranda.png' or file == 'milhaus.png' or file == 'one.png'):
            global xm
            global ym
            xm=x
            ym=y
            return True
        if file == "drop.png":
            ahk.mouse_move(xm, ym, speed=10)
            time.sleep(1)
            ahk.mouse_drag(x, y, relative=False)
            return True
        ahk.mouse_move(x, y, speed=10)  # Moves the mouse instantly to absolute screen position
        ahk.click()  # Click the primary mouse button
        if file == 'group_find.png':
            return True
        if file == 'group.png':
            group_create()
    else:
        print("объект не обнаружен"+file)
        if file == 'group_find.png':
            return 6
        if file == 'one.png':
            return 5


def main():
    findgame()
    win.show()
    win.restore()
    win.maximize()
    win.to_top()
    win.maximize()
    while True:
        if findgame():
            where()

if __name__ == '__main__':
    main()



