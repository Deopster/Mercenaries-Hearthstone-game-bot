import time
import cv2
import numpy as np
from ahk import AHK
from mss import mss
import mss
import configparser
import random
from tkinter import *
import threading
import keyboard
from tkinter.ttk import *
from PIL import Image

ahk = AHK()
global xm
xm = 0
global ym
ym = 0
global monik
global speed
global sens
global zipp
global zipchek
global road
road = False
zipp = False
zipchek = False
global open
open = False
sens = 0.75
# for_future=['','','','','','','','','','','','','','','','','','','',]
# Ui-ellements

Ui_Ellements = ['battle', 'blue', 'green', 'group', 'next', 'one', 'page_1', 'page_2', 'page_3', 'red', 'prev', 'sob',
                'noclass', 'bat1', 'bat2', 'bat3', 'bat4', 'bat5', 'findthis', 'sombody', 'pack_open',
                'presents', 'travel', 'startbat','pick']  # noclass 12, bat5-17
# buttons
buttons = ['back', 'continue', 'create', 'del', 'join_button', 'num', 'ok', 'play', 'ready', 'sec', 'sta', 'start',
           'start1', 'submit', 'allready', 'startbattle', 'startbattle1', 'take', 'take1', 'yes', 'onedie', 'reveal',
           'done', 'finishok', 'confirm']  # last take -17
# chekers
chekers = ['30lvl', 'empty_check', 'find', 'goto', 'group_find', 'level_check', 'rename', 'shab', 'drop', '301', '302',
           'taken', 'text', 'win', 'ifrename', 'levelstarted', 'nextlvlcheck', 'cords-search', '303', '30lvl1',
           '30lvl2','menu','party']
# levels
levels = ['level15']
# heroes
hero = ['', '', '']
hero_colour = ['', '', '']
pages = ['', '', '']
heroNUM = ['', '', '']
# for battle
herobattle = []
herobattlefin = []
# damp
enemywiz = [0, 0, 0, 0, 0, 0]
heroTEMP = []
# img list
picparser = ['/1.png', '/2.png', '/3.png', '/4.png']


def configread():
    global Resolution
    global speed
    global monik
    config = configparser.ConfigParser()
    config.read("settings.ini")
    monik = int((config["BotSettings"]["monitor"]).split("#")[0])
    speed = float((config["BotSettings"]["bot_speed"]).split("#")[0])
    hero[0] = (config["Hero1"]["number"]).split("#")[0]
    hero_colour[0] = (config["Hero1"]["colour"]).split("#")[0]

    hero[1] = (config["Hero2"]["number"]).split("#")[0]
    hero_colour[1] = (config["Hero2"]["colour"]).split("#")[0]

    hero[2] = (config["Hero3"]["number"]).split("#")[0]
    hero_colour[2] = (config["Hero3"]["colour"]).split("#")[0]

    pages[0] = int((config["NumberOfPages"]["Red"]).split("#")[0])
    pages[1] = int((config["NumberOfPages"]["Green"]).split("#")[0])
    pages[2] = int((config["NumberOfPages"]["Blue"]).split("#")[0])

    Resolution = (config["Resolution"]["Monitor Resolution"]).split("#")[0]
    if Resolution == '2560*1440':
        Resolution = '2560x1440'
    if Resolution == '1920*1080':
        Resolution = '1920x1080'
    if Resolution == '3840*2160':
        Resolution = '3840x2160'

    print(pages[0], pages[1], pages[2])

    print(monik, speed, hero)


def filepp(name, strname):
    try:
        i = 0
        while i < len(name):
            name[i] = strname + "/" + name[i] + ".png"
            i += 1
    except:
        print(strname, "file list got error")


def parslist():
    filepp(Ui_Ellements, "Ui_Ellements")
    filepp(buttons, "Buttons")
    filepp(chekers, "Chekers")
    filepp(levels, "Levels")
    i = 0
    while i < len(hero):
        hero[i] = "heroes/" + hero[i]
        i += 1
    return 0


def screen():
    global Resolution
    sct = mss.mss()
    filename = sct.shot(mon=monik, output='files/' + Resolution + '/screen.png')


def partscreen(x, y, top, left):
    print("entered screenpart")
    global Resolution
    import mss.tools
    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": x, "height": y}
        output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output='files/' + Resolution + '/part.png')


def findgame():
    global win
    try:
        win = ahk.win_get(title='Hearthstone')
    except:
        print("Not found game.")
    if win.exist:
        return True
    else:
        return False


def battlefind(file, coll):
    if road == True:
        print("back battlefind")
        return
    global sens
    global top
    global left
    global Resolution
    herobattle.clear()
    img = cv2.imread('files/' + Resolution + '/part.png')
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # преобразуем её в серуюш
    template = cv2.imread('files/' + Resolution + '/' + file,
                          cv2.IMREAD_GRAYSCALE)  # объект, который преобразуем в серый, и ищем его на gray_img
    w, h = template.shape[::-1]  # инвертируем из (y,x) в (x,y)`
    result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)

    loc = np.where(result >= 0.75)
    num = 0
    if len(loc[0]) != 0:
        j = 0
        for pt in zip(*loc[::-1]):
            x = int(((pt[0] * 2 + w) / 2) + 60)
            y = int((((pt[1] * 2 + h) / 2) + (win.rect[3] / 2)))

            herobattle.append([coll, x, y])
        print("Unsort Data of our heroes", herobattle)

        for i in herobattle:
            print(i)
            for n in range(6):
                if i[1] < enemywiz[n] + 20 and i[1] > enemywiz[n] - 20:
                    print("first num:", i[1], "second num:", enemywiz[n])
                    if enemywiz[n] != 0:
                        print('then stoped')
                        break
                else:
                    if enemywiz[n] == 0:
                        print("it wrote ", i[1], "in ", enemywiz[num])
                        enemywiz[num] = i[1]
                        print("enemiwiz now", enemywiz)
                        num += 1
                        herobattlefin.append(i)
                        print("herobattle now", herobattlefin)
                        break
        print(enemywiz)
        print("Sort Data of our heroes", herobattlefin)
        for i in range(2):
            enemywiz[i] = 0
        return 0


def move(index):
    if index != (0, 0):
        time.sleep(0.1)
        ahk.mouse_drag(index[0] + 40, index[1] - 30, speed=3, relative=False)
        ahk.click()
        return False
    else:
        return True


def rand(enemyred, enemygreen, enemyblue, enemynoclass):
    count = 0
    while True:
        a = random.randint(0, 2)
        if a == 0:
            if not move(enemygreen):
                break
            else:
                count += 1
        if a == 1:
            if not move(enemyred):
                break
            else:
                count += 1
        if a == 2:
            if not move(enemyblue):
                break
            else:
                count += 1
        if count > 5:
            x = int(win.rect[2] / 2)
            y = int(win.rect[2] / 6)
            ahk.mouse_drag(x, y, speed=3, relative=False)
            ahk.click()
            break


def collect():
    global road
    while True:
        if road == True:
            print("back collect")
            break
        if not find_ellement(buttons[22], 14):
            ahk.mouse_move(win.rect[2] / 2.5, win.rect[3] / 3.5, speed=3)
            ahk.click()
            ahk.mouse_move(win.rect[2] / 1.5, win.rect[3] / 3.5, speed=3)
            ahk.click()
            ahk.mouse_move(win.rect[2] / 2.7, win.rect[3] / 1.4, speed=3)
            ahk.click()
            ahk.mouse_move(win.rect[2] / 1.7, win.rect[3] / 1.3, speed=3)
            ahk.click()
            time.sleep(1)
        else:
            while True:
                if find_ellement(buttons[23], 14):
                    for i in range(2):
                        time.sleep(0.5)
                        find_ellement(buttons[0], 0)
                        road = True
                    break


def nextlvl():
    if road == True:
        print("back nextlevel")
        return
    global speed
    global sens
    time.sleep(1.5)
    if find_ellement(buttons[7], 14):
        seth()
        print("back nextlevel1")
        return 0
    tm = int(win.rect[3] / 3.1)
    partscreen(2560, tm, tm, 0)
    x = win.rect[2] / 3.7
    y = win.rect[3] / 2.2
    temp = speed
    speed = 0
    sens = 0.7
    for n in range(8):
        ahk.mouse_position = (x, y)
        ahk.click()
        x += win.rect[2] / 25
    speed = temp
    sens = 0.65
    for i in range(4):
        x, y = find_ellement(Ui_Ellements[13 + i], 12)
        if x != 0:
            ahk.mouse_move(x, y + win.rect[3] / 2.5, speed=3)
            ahk.click()
            break
    sens = 0.7
    if find_ellement(buttons[21], 14):
        time.sleep(1)
        ahk.mouse_move(win.rect[2] / 2, win.rect[3] - win.rect[3] / 4.8, speed=3)
        ahk.click()
        nextlvl()
        print("back nextlevel2")
        return 0
    find_ellement(buttons[7], 2)
    if find_ellement(Ui_Ellements[19], 1):
        temp = random.randint(0, 2)
        if temp == 0:
            x = win.rect[2] / 2.3
            ahk.mouse_move(x, y, speed=3)
        if temp == 1:
            x = win.rect[2] / 1.7
            ahk.mouse_move(x, y, speed=3)
        if temp == 2:
            x = win.rect[2] / 1.4
            ahk.mouse_move(x, y, speed=3)
        ahk.click()
        find_ellement(buttons[18], 9)
        time.sleep(1)
        find_ellement(buttons[7], 2)
    while True:
        if find_ellement(Ui_Ellements[24], 14):
            time.sleep(0.5)
            ahk.click()

            nextlvl()
            print("back nextlevel3")
            return 0
        if find_ellement(Ui_Ellements[23], 14):
            seth()
            print("back nextlevel4")
            break
        else:
            ahk.mouse_move(win.rect[2] / 2, win.rect[3] - win.rect[3] / 4.8, speed=3)
            ahk.click()
            find_ellement(buttons[7], 14)
        if road == True:
            print("back nextlevel5")
            return


def Tres():
    y = win.rect[3] / 2
    temp = random.randint(0, 2)
    if temp == 0:
        x = win.rect[2] / 2.3
        ahk.mouse_move(x, y, speed=3)
    if temp == 1:
        x = win.rect[2] / 1.7
        ahk.mouse_move(x, y, speed=3)
    if temp == 2:
        x = win.rect[2] / 1.4
        ahk.mouse_move(x, y, speed=3)
    ahk.click()
    while True:
        if find_ellement(buttons[17], 14):
            time.sleep(1)
            nextlvl()
            print("back Tres")
            return


def resize():
    for i in range(3):
        image_path = './files/' + Resolution + '/' + hero[i] + '/set.png'
        img = Image.open(image_path)
        # получаем ширину и высоту
        width, height = img.size
        print(width, height)
        # открываем картинку в окне
        new_image = img.resize((int(width * 0.65), int(height * 0.65)))
        new_image1 = img.resize((int(width * 0.75), int(height * 0.75)))
        new_image.save('./files/' + Resolution + '/' + hero[i] + '/main.png')
        new_image1.save('./files/' + Resolution + '/' + hero[i] + '/group.png')


def abilicks(index):
    heroTEMP.clear()
    for i in range(3):
        if hero_colour[i] == index:
            heroTEMP.append(hero[i])
    print(index)
    print(heroTEMP)
    for obj in heroTEMP:
        if obj == 'heroes/1':
            if raund >1 and raund %2==0:
                if find_ellement(obj + '/abilics/2.png', 14):
                    return False
            if raund ==1:
                if find_ellement(obj + '/abilics/1.png', 14):
                    return True
            ahk.mouse_move(int(win.rect[2] / 2.5), int(win.rect[2] / 4), speed=3)
            ahk.click()
            return True

        elif obj == 'heroes/3':
            if raund==1:
                if find_ellement(obj + '/abilics/1.png', 14):
                    return False
            if raund==3:
                if find_ellement(obj + '/abilics/3.png', 14):
                    return False
            if raund>1:
                if find_ellement(obj + '/abilics/2.png', 14):
                    return True
            ahk.mouse_move(int(win.rect[2] / 2.5), int(win.rect[2] / 4), speed=3)
            ahk.click()
            return True

        elif obj == 'heroes/2':
            if raund %2==1:
                if find_ellement(obj + '/abilics/1.png', 14):
                    return True
            if raund %2==0:
                if find_ellement(obj + '/abilics/3.png', 14):
                    return False
            ahk.mouse_move(int(win.rect[2] / 2.5), int(win.rect[2] / 4), speed=3)
            ahk.click()
            return True


def atack(i, enemyred, enemygreen, enemyblue, enemynoclass, mol):
    x = int(i[1])
    y = int(i[2])
    print("Attack function")
    if i[0] == 'Red':
        print("open Red")
        ahk.mouse_move(x, y, speed=3)
        ahk.click()
        time.sleep(0.2)
        if abilicks('Red'):
            if move(enemygreen):
                if move(mol):
                    if move(enemynoclass):
                        rand(enemyred, enemygreen, enemyblue, enemynoclass)
    if i[0] == 'Green':
        print("open Green")
        ahk.mouse_move(x, y, speed=3)
        ahk.click()
        time.sleep(0.2)
        if abilicks('Green'):
            if move(enemyblue):
                if move(mol):
                    if move(enemynoclass):
                        rand(enemyred, enemygreen, enemyblue, enemynoclass)
    if i[0] == 'Blue':
        print("open blue")
        ahk.mouse_move(x, y, speed=3)
        ahk.click()
        time.sleep(0.2)
        if abilicks('Blue'):
            if move(enemyred):
                if move(mol):
                    if move(enemynoclass):
                        rand(enemyred, enemygreen, enemyblue, enemynoclass)


def battle():
    global raund
    global sens
    global zipchek
    global speed
    if road == True:
        print("back battle1")
        return
    raund = 1
    while True:
        if road == True:
            break
        ahk.mouse_move(win.rect[2] / 2, win.rect[3] - win.rect[3] / 4.6, speed=3)
        speed = 0
        sens = 0.85
        find_ellement(buttons[20], 14)
        if find_ellement(chekers[13], 1):
            ahk.mouse_move(win.rect[2] / 2, win.rect[3] - win.rect[3] / 4.6, speed=3)
            while True:
                if not find_ellement(Ui_Ellements[18], 1):
                    ahk.click()
                    time.sleep(0.5)
                else:
                    Tres()
                    break
                if find_ellement(Ui_Ellements[21], 1):
                    collect()
                    break

        if find_ellement(buttons[15], 1) or find_ellement(buttons[16], 1):  # finds startbattle.png
            print(win.rect)
            herobattlefin.clear()
            tmp = int(win.rect[3] / 2)
            tmp = int(win.rect[3] / 2)
            partscreen(2560, tmp, 0, 0)
            temp = speed
            sens = 0.8
            # поиск врага
            enemyred = find_ellement(Ui_Ellements[9], 12)
            enemygreen = find_ellement(Ui_Ellements[2], 12)
            enemyblue = find_ellement(Ui_Ellements[1], 12)
            enemynoclass = find_ellement(Ui_Ellements[12], 12)
            print("red: ", enemyred)
            print("green: ", enemygreen)
            print("blue: ", enemyblue)
            print("noclass: ", enemynoclass)
            mol = find_ellement(Ui_Ellements[11], 12)
            ahk.mouse_move(win.rect[2] / 2, win.rect[3] - win.rect[3] / 4.8, speed=3)
            ahk.click()
            time.sleep(1)
            partscreen(2560, tmp, tmp, 0)
            print("enter serch Red")
            battlefind(Ui_Ellements[9], 'Red')  # find all yr Red
            if len(herobattlefin) != 3:
                print("enter serch Green")
                battlefind(Ui_Ellements[2], 'Green')  # find all yr Green
            if len(herobattlefin) != 3:
                print("enter serch Blue")
                battlefind(Ui_Ellements[1], 'Blue')  # find all yr Blue
            print("cords of my heroes ")
            print(herobattlefin)
            for i in herobattlefin:
                ahk.mouse_move(win.rect[2] / 2, win.rect[3] - win.rect[3] / 4.8, speed=3)
                ahk.click()
                print("print index", i)
                atack(i, enemyred, enemygreen, enemyblue, enemynoclass, mol)
                time.sleep(0.1)
            sens = 0.75
            speed = temp
            i = 0
            while True:
                if not find_ellement(buttons[14], 2):
                    break
                if i > 10:
                    ahk.show_warning_traytip("Battle", "Battle error,please write what happend on github issue")
                    find_ellement(buttons[15], 2)
                    break
                i += 1
            time.sleep(3)
            raund += 1


def seth():
    if road == True:
        print("back set1")
        return
    global speed
    global sens
    while True:
        if find_ellement(buttons[5], 1):
            break
    print(win.rect)
    x = win.rect[2] / 2.85
    y = win.rect[3] - win.rect[3] / 10
    i = 0
    temp = speed
    speed = 0
    sens = 0.85
    i = 0
    while not find_ellement(buttons[14], 1):
        print('вход')
        sens = 0.75
        ahk.mouse_position = (x, y)
        for n in range(3):
            if i >= 7:
                ahk.mouse_drag(x, y - 600, speed=3, relative=False)
            if find_ellement(hero[n] + '/set.png', 6):
                time.sleep(0.2)
                ahk.mouse_drag(x, y - 600, speed=3, relative=False)
            x += win.rect[2] / 57
        if x > win.rect[2] / 1.5:
            x = win.rect[2] / 2.85
        i += 1
    print('выход')
    speed = temp
    sens = 0.7
    ahk.mouse_move(200, 200, speed=3)
    time.sleep(1)
    find_ellement(buttons[14], 9)
    time.sleep(5)
    battle()
    return


def battlego():
    if road == True:
        print("back battlgo")
        return
    global sens
    print("Битва")
    time.sleep(1)
    find_ellement(Ui_Ellements[0], 0)
    while True:
        find_ellement(Ui_Ellements[22], 14)
        if find_ellement(chekers[15], 14):
            time.sleep(1)
            nextlvl()
            break
        if find_ellement(buttons[7], 14):
            find_ellement(buttons[7], 14)
            seth()
        if not find_ellement(buttons[10], 2):
            time.sleep(2)
            find_ellement(buttons[9], 2)
            break
    while True:
        if not find_ellement(levels[0], 2):
            if not find_ellement(buttons[11], 2):
                break
    while True:
        if not find_ellement(chekers[2], 2):
            find_ellement(buttons[12], 2)
            break
    while True:
        time.sleep(0.2)
        if find_ellement(buttons[7], 0):
            time.sleep(0.5)
            break
        else:
            find_ellement(buttons[13], 2)
    seth()
    print("back set2")
    return


def where():
    if road == True:
        print("back where")
        return True
    find_ellement(buttons[4], 0)
    find_ellement(Ui_Ellements[3], 0)
    find_ellement(buttons[0], 0)
    return True


def pagech(page, coll):
    if int(pages[coll]) > 1:
        if page != pages[coll]:
            find_ellement(Ui_Ellements[4], 0)
            time.sleep(1)
            page += 1
        else:
            while page != 1:
                find_ellement(Ui_Ellements[10], 0)
                page -= 1
                time.sleep(1)
    return page


def find(n):
    global speed
    temp=speed
    speed=0
    change(n)
    page = 1
    while True:
        for num in range(2):
            if find_ellement(hero[n] + "/main.png", 6):
                print('нашёл')
                find_ellement(chekers[8], 0)
                return True
        page = pagech(page, n)
    speed=temp


def change(index):
    if hero_colour[index] == 'Red':
        find_ellement(Ui_Ellements[6], 9)
    if hero_colour[index] == 'Green':
        find_ellement(Ui_Ellements[7], 9)
    if hero_colour[index] == 'Blue':
        find_ellement(Ui_Ellements[8], 9)
    time.sleep(1)


def test(n):
    global sens
    sens=0.65
    if find_ellement(hero[n] + "/group.png", 6):
        print('нашёл')

def group_create():
    if road == True:
        print("back group")
        return
    global speed
    global left
    global top
    global sens
    time.sleep(1)
    while not find_ellement(chekers[4], 1):
        where()
    if find_ellement(chekers[4], 3) == 6:
        find_ellement(buttons[2], 0)
        time.sleep(1.5)
        print(win.rect)
        x = int(win.rect[2] / 1.3)
        y = int(win.rect[3] / 9)
        # while not find_ellement(chekers[14], 14):
        ahk.mouse_move(x, y, speed=3)
        time.sleep(0.5)
        ahk.click()
        temp = speed
        speed = 0
        ahk.send_input('Botwork', 0)
        find_ellement(Ui_Ellements[10], 0)
        time.sleep(1)
        for i in range(3):
            if hero[i] != '-':
                find(i)
        speed = temp
        find_ellement(buttons[8], 0)
        time.sleep(0.2)
        find_ellement(buttons[1], 0)
        time.sleep(0.2)
        find_ellement(Ui_Ellements[6], 2)
        group_create()
    else:
        time.sleep(1)
        if find_ellement(chekers[1], 2) == True:
            x, y = find_ellement(chekers[17], 15)
            x = x - int(win.rect[2] / 9)
            y = y + int(win.rect[3] / 18.5)
            add = 0
            for i in range(6):
                temp = sens
                sens = 0.65
                ahk.mouse_move(x, y, speed=3)  # Moves the mouse instantly to absolute screen position
                ahk.click()
                if i < 3:
                    bool_check = False
                    time.sleep(0.5)
                    if find_ellement(hero[i] + "/group.png", 1):
                        bool_check = True
                    if bool_check is False:
                        sens = temp
                        find_ellement(buttons[8], 0)
                        time.sleep(0.2)
                        find_ellement(buttons[1], 0)
                        time.sleep(0.2)
                        find_ellement(buttons[8], 0)
                        while True:
                            time.sleep(0.2)
                            if find_ellement(chekers[3], 1):
                                time.sleep(0.5)
                                if find_ellement(buttons[3], 14):
                                    time.sleep(0.5)
                                    find_ellement(buttons[24], 14)
                                    group_create()
                                    break
                    y = y + int(win.rect[3] / 19)
                    sens = temp
                if i >= 3:
                    temp = sens
                    sens = 0.85
                    time.sleep(0.5)
                    if find_ellement(chekers[0], 1) or find_ellement(chekers[19], 1) or find_ellement(chekers[20], 1):
                        ahk.mouse_drag(x - 600, y, speed=5, relative=False)
                        add += 1
                    else:
                        y = y + int(win.rect[3] / 17.2)
            sens = 0.75
            while True:
                if find_ellement(buttons[8], 14):
                    break
            time.sleep(0.5)
            if add != 0:
                print("Add heroes")
                find_ellement(Ui_Ellements[6], 14)
                time.sleep(0.5)
                find_merc(add)
            sens = temp
            time.sleep(0.5)
        else:
            find_merc(3)
        while True:
            if road == True:
                print("back group menu")
                return
            if find_ellement(chekers[21], 1):
                break
            find_ellement(buttons[8], 14)
            time.sleep(0.5)
            ahk.click()
            time.sleep(0.2)
            if find_ellement(buttons[1], 14):
                pass
            else:
                ahk.mouse_move(1000, 1000, speed=3)  # Moves the mouse instantly to absolute screen position
                time.sleep(0.2)
            find_ellement(buttons[0], 14)
            ahk.mouse_move(1000, 1000, speed=3)
            time.sleep(1.5)
            if find_ellement(chekers[21], 1):
                break
        battlego()
        print("back group3")
        return




def find_merc(n):
    time.sleep(0.5)
    global left
    global top
    global speed
    global sens
    i = 0
    temp1=sens
    sens = 0.9
    temp = speed
    speed = 0
    while i < n:
        print("enter iteration loop")
        x = int(win.rect[2] / 7.5)
        y = int(win.rect[3] / 3.5)
        top = int(win.rect[3] / 5.76)
        left = int(win.rect[2] / 5.2)
        h = 0
        while h < 2:
            print("enter height loop")
            left = int(win.rect[2] / 5.2)
            j = 0
            while j < 3:
                print("enter width loop")
                partscreen(x, y, top, left)
                if find_ellement(chekers[12], 7):
                    print(xm, ym)
                    if find_ellement(chekers[9], 7) is False and find_ellement(chekers[10], 7) is False and find_ellement(chekers[18], 7) is False:
                        print("found object")
                        if not find_ellement(chekers[11], 7):
                            find_ellement(chekers[8], 7)
                            i += 1
                            print("droped the object")
                j += 1
                left += int(win.rect[2] / 7)
                print("go next element on line")
            top += int(win.rect[3] / 3)
            print("go next line")
            h += 1
        find_ellement(Ui_Ellements[4], 0)
    speed = temp
    sens=temp1

def find_ellement(file, index):
    if road == True:
        return
    global sens
    global top
    global left
    global Resolution
    time.sleep(speed)
    if index == 12:
        img = cv2.imread('files/' + Resolution + '/part.png')
    elif index == 7 and file != chekers[8]:
        img = cv2.imread('files/' + Resolution + '/part.png')
    else:
        screen()
        img = cv2.imread('files/' + Resolution + '/screen.png')  # картинка, на которой ищем объект
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # преобразуем её в серуюш
    template = cv2.imread('files/' + Resolution + '/' + file,
                          cv2.IMREAD_GRAYSCALE)  # объект, который преобразуем в серый, и ищем его на gray_img
    w, h = template.shape[::-1]  # инвертируем из (y,x) в (x,y)`
    result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)

    loc = np.where(result >= sens)
    if len(loc[0]) != 0:
        for pt in zip(*loc[::-1]):
            pt[0] + w
            pt[1] + h
        x = int((pt[0] * 2 + w) / 2)
        y = int((pt[1] * 2 + h) / 2)
        print("Found " + file, x, y)
        if index == 12 or index == 15:
            return (x, y)
        if (index == 6 or file == Ui_Ellements[5] or file == chekers[7]):
            global xm
            global ym
            xm = x
            ym = y
            return True
        if file == chekers[8]:
            if index == 7:
                xm += left
                ym += top
            ahk.mouse_move(xm, ym, speed=2)
            time.sleep(0.5)
            ahk.mouse_drag(x, y, speed=3, relative=False)
            return True
        if file == chekers[5]:
            ahk.mouse_move(x, y + 70, speed=3)
            ahk.click()
            return True
        if file == buttons[5]:
            ahk.mouse_move(x, y, speed=5)
            return True
        if file == chekers[3]:
            ahk.mouse_move(x, y, speed=5)
        if index == 1:
            return True
        if index == 7:
            xm = x
            ym = y
            return True
        p = random.randint(-2, 2)
        s = random.randint(-2, 2)
        ahk.mouse_move(x + p, y + s, speed=5)  # Moves the mouse instantly to absolute screen position
        ahk.click()  # Click the primary mouse button
        if file == buttons[7]:
            return True
        if file == Ui_Ellements[3]:
            time.sleep(0.5)
            ahk.click()
            group_create()
        if index == 14:
            return True
    else:
        print("Not found  " + file)
        if index == 14:
            return False
        if index == 12 or index == 15:
            return 0, 0
        if index == 6:
            return False
        if index == 7:
            return False
        if index == 3:
            return 6
        if index == 2:
            return True
        if index == 1 or index == 9 or index == 12:
            return False
        if file == buttons[7]:
            return False
        if file != buttons[4] and file != Ui_Ellements[3] and file != buttons[0]:
            where()


def inter():
    window = Tk()
    label = Label(
        text="Resolution",
        fg="white",
        bg="black",
        width=20,
        height=20
    )
    combo = Combobox(window)
    window.title("HsBot v1.0")
    combo['values'] = ("1920x1080", "2560x1440", "not ready")
    combo.current(1)  # set the selected item
    combo.grid(column=0, row=0)
    label.pack()
    window.mainloop()


def main():
    global road
    print("start")
    try:
        ahk.show_info_traytip("Starting", "loading files", slient=False, blocking=True)
        configread()
        findgame()
        parslist()
        resize()
        ahk.show_info_traytip("started", "all files loaded successfully", slient=False, blocking=True)
        win.show()
        win.restore()
        win.maximize()
        win.to_top()
        win.maximize()
        win.to_top()
        win.activate()
        # thr1 = threading.Thread(target=inter)
        # thr1.start()
        while True:
            print("Loop start")
            if findgame():
                road = False
                where()
            else:
                print("Not found Game window.")
    except Exception as E:
        print("Error", E)


if __name__ == '__main__':
    main()
