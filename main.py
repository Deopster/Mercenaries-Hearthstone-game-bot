import time
import cv2
import numpy as np
from ahk import AHK
from mss import mss
import mss
import pytesseract
from ahk.window import Window
import configparser
import os



ahk = AHK()
global xm
global ym
global monik
global speed
#for_future=['','','','','','','','','','','','','','','','','','','',]
#Ui-ellements
Ui_Ellements=['battle','blue','green','group','next','one','page_1','page_2','page_3','red']
#buttons
buttons=['back','continue','create','del','join_button','num','ok','play','ready','sec','sta','start','start1','submit']
#chekers
chekers=['30lvl','empty_check','find','goto','group_find','level_check','rename','shab']
#levels
levels=['level15']
#heroes
hero=['deff','milhaus','tiranda']


def configread():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    monik = (config["BotSettings"]["monitor"]).split("#")[0]
    speed = (config["BotSettings"]["bot_speed"]).split("#")[0]
    print(monik,speed)
def parslist():
    i=0
    while i<len(Ui_Ellements):
        Ui_Ellements[i]="UI_ellements/"+Ui_Ellements[i]+".png"
    i = 0
    while i<len(buttons):
        buttons[i]="buttons/"+buttons[i]+".png"
    i = 0
    while i<len(chekers):
        chekers[i]="chekers/"+chekers[i]+".png"
    i = 0
    while i<len(levels):
        levels[i]="levels/"+levels[i]+".png"
    i = 0
    while i<len(hero):
        hero[i]="heroes/"+hero[i]+".png"
    return 0
def screen():
    sct = mss.mss()
    filename = sct.shot(mon=monik, output='files/screen.png')
def findgame():
     global win
     win = ahk.win_get(title='Hearthstone')
     if win.exist:
         print("Игра найдена")
         return True
     else:
         print("Игра не найдена")
         return False
def set():
    while True:
        if find_ellement('num.png',0):
            break
    print(win.rect)
    x = win.rect[2]/2.85
    y = win.rect[3]-win.rect[3]/10
    i=0
    while i<3:
        ahk.mouse_position = (x, y)
        if find_ellement('shab.png',0):
            ahk.mouse_drag(x, y-500, relative=False)
            i+=1
        x += win.rect[2] / 23
        if x>1700:
            x=1031

def battlego():
    print("Битва")
    time.sleep(1)
    find_ellement('UI-ellements/battle.png',0)
    time.sleep(0.5)
    if find_ellement('play.png',0):
        set()
    time.sleep(0.5)
    find_ellement('sta.png',0)
    time.sleep(1)
    find_ellement('sec.png',0)
    time.sleep(0.5)
    find_ellement('level.png',0)
    time.sleep(0.5)
    find_ellement('start.png',0)
    time.sleep(0.5)
    find_ellement('find.png',0)
    time.sleep(0.5)
    find_ellement('start1.png',0)
    time.sleep(0.5)
    if find_ellement('submit.png',0)!=False:
        time.sleep(0.5)
    time.sleep(5)
    find_ellement('play.png',0)
    set()

def where():
    find_ellement('join_button.png',0)
    time.sleep(0.5)
    find_ellement('group.png',0)
    find_ellement('back.png',0)
    return True
def group_create():
    time.sleep(1)
    if find_ellement('group_find.png',0) ==6:
        find_ellement('create.png',0)
        time.sleep(1)
        find_ellement('rename.png',0)
        ahk.send_input('Botwork',0)
        if find_ellement('deff.png',0):
            find_ellement('drop.png',0)
        find_ellement('page_2.png',0)
        find_ellement('next.png',0)
        if find_ellement('tiranda.png',0):
            find_ellement('drop.png',0)
        find_ellement('page_3.png',0)
        if find_ellement('milhaus.png',0):
            find_ellement('drop.png',0)
        find_ellement('ready.png',0)
        find_ellement('continue.png',0)
        find_ellement('page_1.png',0)
        group_create()
    else:
        time.sleep(1)
        if find_ellement('empty_check.png',0) == True:
            find_ellement('level_check.png',0)
            if find_ellement('30lvl.png',0) == False:
                find_ellement('ready.png',0)
                find_ellement('ready.png',0)
                time.sleep(0.5)
                find_ellement('goto.png',0)
                time.sleep(0.5)
                find_ellement('del.png',0)
                find_ellement('ok.png',0)
                group_create()
            else:
                find_ellement('ready.png',0)
                find_ellement('ready.png',0)
                time.sleep(0.5)
                find_ellement('back.png',0)
                battlego()


        else:
            i=0
            while i<3:
                if find_ellement('one.png',0) !=6:
                    find_ellement('drop.png',0)
                    i+=1
                else:
                    find_ellement('next.png',0)

        find_ellement('ready.png',0)
def text():
    img = cv2.imread('files/screen.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Будет выведен весь текст с картинки
    config = r'--oem 3 --psm 6'
    print(pytesseract.image_to_string(img, config=config))

def find_ellement(file,index):
    time.sleep(speed)
    screen()
    if index==3:
        text()
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
        if (file == "deff.png" or file == 'tiranda.png' or file == 'milhaus.png' or file == 'one.png'or file == 'shab.png'):
            global xm
            global ym
            xm=x
            ym=y
            return True
        if file == "drop.png":
            ahk.mouse_move(xm, ym, speed=5)
            time.sleep(1)
            ahk.mouse_drag(x, y, relative=False)
            return True
        if file == 'level_check.png':
            ahk.mouse_move(x, y+70, speed=3)  # Moves the mouse instantly to absolute screen position
            ahk.click()
            return True
        if file =='goto.png':
            ahk.mouse_move(x, y, speed=5)
            return True
        if file == '30lvl.png':
            return False
        if file =='num.png':
            return True
        ahk.mouse_move(x, y, speed=5)  # Moves the mouse instantly to absolute screen position
        ahk.click()  # Click the primary mouse button
        if file =='play.png':
            return True
        if file == 'group.png':
            group_create()
    else:
        print("объект не обнаружен"+file)
        if file == 'group_find.png':
            return 6
        if file == 'one.png':
            return 6
        if file == 'empty_check.png':
            return True

        if file =='30lvl.png':
            return True
        if file =='sec.png':
            return True
        if file == 'num.png':
            return False
        if file == 'shab.png':
            return False
        if file =='play.png':
            return False
        if file =='submit.png':
            return False
        if (file !='join_button.png' and file !='back.png' and file !='group.png'):
            where()


def main():
    configread()
    findgame()
    parslist()
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



