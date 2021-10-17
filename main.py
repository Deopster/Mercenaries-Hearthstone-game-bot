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
chekers=['30lvl','empty_check','find','goto','group_find','level_check','rename','shab','drop']
#levels
levels=['level15']
#heroes
hero=['deff','milhaus','tiranda']


def configread():
    global speed
    global monik
    config = configparser.ConfigParser()
    config.read("settings.ini")
    monik = int((config["BotSettings"]["monitor"]).split("#")[0])
    speed = float((config["BotSettings"]["bot_speed"]).split("#")[0])
    print(monik,speed)
def parslist():
    i=0
    while i<len(Ui_Ellements):
        Ui_Ellements[i]="UI_ellements/"+Ui_Ellements[i]+".png"
        i+=1
    print("1 блок")
    i = 0
    while i<len(buttons):
        buttons[i]="buttons/"+buttons[i]+".png"
        i += 1
    print("2 блок")
    i = 0
    while i<len(chekers):
        chekers[i]="chekers/"+chekers[i]+".png"
        i += 1
    i = 0
    print("3 блок")
    while i<len(levels):
        levels[i]="levels/"+levels[i]+".png"
        i += 1
    i = 0
    print("4 блок")
    while i<len(hero):
        hero[i]="heroes/"+hero[i]+".png"
        i += 1
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
        if find_ellement(buttons[5],1):
            break
    print(win.rect)
    x = win.rect[2]/2.85
    y = win.rect[3]-win.rect[3]/10
    i=0
    while i<3:
        ahk.mouse_position = (x, y)
        if find_ellement(chekers[7],1):
            ahk.mouse_drag(x, y-500, relative=False)
            i+=1
        x += win.rect[2] / 23
        if x>1700:
            x=1031

def battlego():
    print("Битва")
    time.sleep(1)
    find_ellement(Ui_Ellements[0],0)
    time.sleep(0.5)
    if find_ellement(buttons[7],1):
        set()
    time.sleep(0.5)
    find_ellement(buttons[10],0)
    time.sleep(1)
    find_ellement(buttons[9],2)
    time.sleep(0.5)
    find_ellement(levels[0],0)
    time.sleep(0.5)
    find_ellement(buttons[11],0)
    time.sleep(0.5)
    find_ellement(chekers[2],0)
    time.sleep(0.5)
    find_ellement(buttons[12],0)
    time.sleep(0.5)
    if find_ellement(buttons[13],1)!=False:
        time.sleep(0.5)
    time.sleep(5)
    find_ellement(buttons[7],0)
    set()

def where():
    find_ellement(buttons[4],0)
    time.sleep(0.5)
    find_ellement(Ui_Ellements[3],0)
    find_ellement(buttons[0],0)
    return True
def group_create():
    time.sleep(1)
    if find_ellement(chekers[4],3) ==6:
        find_ellement(buttons[2],0)
        time.sleep(1)
        find_ellement(chekers[6],0)
        ahk.send_input('Botwork',0)
        if find_ellement(hero[0],0):
            find_ellement(chekers[8],0)
        find_ellement(Ui_Ellements[7],0)
        find_ellement(Ui_Ellements[4],0)
        if find_ellement(hero[2],0):
            find_ellement(chekers[8],0)
        find_ellement(Ui_Ellements[8],0)
        if find_ellement(hero[1],0):
            find_ellement(chekers[8],0)
        find_ellement(buttons[8],0)
        find_ellement(buttons[1],0)
        find_ellement(Ui_Ellements[6],0)
        group_create()
    else:
        time.sleep(1)
        if find_ellement(chekers[1],2) == True:
            find_ellement(chekers[5],0)
            if find_ellement(chekers[0],1) == True:
                find_ellement(buttons[8],0)
                find_ellement(buttons[8],0)
                time.sleep(0.5)
                find_ellement(chekers[3],0)
                time.sleep(0.5)
                find_ellement(buttons[3],0)
                find_ellement(buttons[6],0)
                group_create()
            else:
                find_ellement(buttons[8],0)
                time.sleep(1)
                find_ellement(buttons[8],0)
                time.sleep(1)
                find_ellement(buttons[0],0)
                battlego()


        else:
            i=0
            while i<3:
                if find_ellement(Ui_Ellements[5],3) !=6:
                    find_ellement(chekers[8],0)
                    i+=1
                else:
                    find_ellement(Ui_Ellements[4],0)

        find_ellement(buttons[8],0)
        time.sleep(1)
        find_ellement(buttons[0], 0)
        time.sleep(2)
        battlego()
def text():
    img = cv2.imread('files/screen.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Будет выведен весь текст с картинки
    config = r'--oem 3 --psm 6'
    print(pytesseract.image_to_string(img, config=config))

def find_ellement(file,index):
    time.sleep(speed)
    screen()
    if index=="text":
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
        if (file == hero[0] or file == hero[1] or file == hero[2] or file == Ui_Ellements[5] or file == chekers[7]):
            global xm
            global ym
            xm=x
            ym=y
            return True
        if file == chekers[8]:
            ahk.mouse_move(xm, ym, speed=5)
            time.sleep(1)
            ahk.mouse_drag(x, y, relative=False)
            return True
        if file == chekers[5]:
            ahk.mouse_move(x, y+70, speed=3)  # Moves the mouse instantly to absolute screen position
            ahk.click()
            return True
        if file ==buttons[5]:
            ahk.mouse_move(x, y, speed=5)
            return True
        if index == 1:
            return True
        ahk.mouse_move(x, y, speed=5)  # Moves the mouse instantly to absolute screen position
        ahk.click()  # Click the primary mouse button
        if file ==buttons[7]:
            return True
        if file == Ui_Ellements[3]:
            group_create()
    else:
        print("объект не обнаружен "+file)
        if index== 3:
            return 6
        if index==2:
            return True
        if index ==1 :
            return False
        if (file !=buttons[4] and file !=Ui_Ellements[3] and file !=buttons[0]):
            where()


def main():
    ahk.show_info_traytip("Started", "loading files", slient=False, blocking=True)
    configread()
    findgame()
    parslist()
    ahk.show_info_traytip("started", "all files loaded sucsessfuly", slient=False, blocking=True)
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



