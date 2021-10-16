from PIL import ImageGrab
import os
import time
import cv2
import numpy as np
from matplotlib import pyplot as plt
from ahk import AHK
from mss import mss
import mss
ahk = AHK()
def screen_record_efficient():
    sct = mss.mss()
    filename = sct.shot(mon=1, output='files/screen.png')
    print(filename)
def findgame():
    win = ahk.find_window(title=b'Hearthstone')
    win.maximize()
def find_ellement():
    img = cv2.imread("files/screen.png")  # картинка, на которой ищем объект
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # преобразуем её в серуюш
    template = cv2.imread("files/join_button.png",
                          cv2.IMREAD_GRAYSCALE)  # объект, который преобразуем в серый, и ищем его на gray_img
    w, h = template.shape[::-1]  # инвертируем из (y,x) в (x,y)

    result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= 0.8)
    # рисует прямоугольник вокруг объекта
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 1, 0), 3)
    x=(pt[0]*2+w)/2
    y=(pt[1]*2+h)/2
    print(x,y)

    #cv2.imshow("img", img)  # выводит на экран результат


def main():

    # делает скриншот игры, закоментируйте, если понадобится, так как скриншот я выложил снизу, как и сам объект
    #gameWindow = (10, 10, 2420, 1320)
    print("MSS:", screen_record_efficient())

    print('\nСкриншот сделан и сохранён\n')
    find_ellement()



if __name__ == '__main__':
    main()



