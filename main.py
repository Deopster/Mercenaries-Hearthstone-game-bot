from PIL import ImageGrab
import os
import time
import cv2
import numpy as np
from matplotlib import pyplot as plt
import win32gui

hwnd = win32gui.FindWindow("notepad", None)
rect = win32gui.GetWindowRect(hwnd)
w = rect[2] - rect[0]
h = rect[3] - rect[1]
print("Window %s:" % win32gui.GetWindowText(hwnd))
print("\t    Size: (%d, %d)" % (w, h))

def find_mana():
    img = cv2.imread("first.png")  # картинка, на которой ищем объект
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # преобразуем её в серуюш
    template = cv2.imread("second.png",
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

    plt.subplot(122), plt.imshow(img,cmap='gist_ncar'),
    plt.title('Detected Point'), plt.axis('off')

    plt.show()

def main():
    # делает скриншот игры, закоментируйте, если понадобится, так как скриншот я выложил снизу, как и сам объект
    gameWindow = (0, 31, 1280, 747)
    im = ImageGrab.grab(gameWindow)
    output = im.save(os.getcwd() + '\\screenshot' + '.png', 'PNG')
    print('\nСкриншот сделан и сохранён\n')

    find_mana()


if __name__ == '__main__':
    main()