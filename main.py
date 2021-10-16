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

def screen():
    sct = mss.mss()
    filename = sct.shot(mon=1, output='files/screen.png')
def findgame():
     global win
     win = ahk.find_window(title=b'Hearthstone')
     print(win.rect)
def find_ellement(file):
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
    else:
        print("объект не обнаружен")
    #plt.plot(122), plt.imshow(img, cmap='gist_ncar'),
    #plt.title('Results'), plt.axis('off')
    plt.show()
def main():
    findgame()
    #while True:
        #time.sleep(3)
    find_ellement('join_button.png')
    #find_ellement('green.png')

if __name__ == '__main__':
    main()



