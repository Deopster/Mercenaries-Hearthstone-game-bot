import time
import cv2
import numpy as np
from mss import mss
import mss
import configparser
import random
from tkinter import *
import threading
import keyboard
from tkinter.ttk import *
from PIL import Image
import os
import sys
import pyautogui

## try to detect the OS (Windows, Linux, Mac, ...)
## to load specific libs
if sys.platform in ['Windows', 'win32', 'cygwin']:
    myOS = 'windows'
    try:
        from ahk import AHK
        ahk = AHK()
    except ImportError:
        print("ahk not installed")
elif sys.platform in ['linux', 'linux2']:
    myOS = 'linux'
    try:
        import gi
        gi.require_version("Wnck", "3.0")
        from gi.repository import Wnck, Gtk
    except ImportError:
        print("gi.repository not installed")
else:
    myOS = 'unknown'
    print("sys.platform='{platform}' is unknown.".format(platform=sys.platform))
    exit(1)


global xm
xm = 0
global ym
ym = 0
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
                'presents', 'travel', 'startbat', 'pick', 'Winterspring', 'Felwood', 'normal',
                'heroic','replace_grey', 'presents3','presents_thing', 'free_battle']  # noclass 12, bat5-17
# buttons
buttons = ['back', 'continue', 'create', 'del', 'join_button', 'num', 'ok', 'play', 'ready', 'sec', 'sta', 'start',
           'start1', 'submit', 'allready', 'startbattle', 'startbattle1', 'take', 'take1', 'yes', 'onedie', 'reveal',
           'done', 'finishok', 'confirm', 'visit','fir','replace', 'keep']  # last take -17
# chekers
chekers = ['30lvl', 'empty_check', 'find', 'goto', 'group_find', 'level_check', 'rename', 'shab', 'drop', '301', '302',
           'taken', 'text', 'win', 'ifrename', 'levelstarted', 'nextlvlcheck', 'cords-search', '303', '30lvl1',
           '30lvl2', 'menu', 'party','lose']
# Settings
setings = []
# heroes
hero = []
hero_colour = []
pages = ['', '', '']
heroNUM = ['', '', '', '', '', '']
# for battle
herobattle = []
herobattlefin = []
# damp
enemywiz = [0, 0, 0, 0, 0, 0]
heroTEMP = []
# img list
picparser = ['/1.png', '/2.png', '/3.png', '/4.png']

debug_mode=False
def debug(*message):
    if debug_mode :
        print("[DEBUG] ", message)

# window multi-platorm (Windows & Linux support)
def windowMP() :
    if(myOS=='windows'):
        retour=win.rect
    elif(myOS=='linux'):
        retour=win.get_client_window_geometry()
    else:
        retour=None
    return retour

# define function to use mouse on Windows & Linux
def mouse_random_movement():
    return random.choices([pyautogui.easeInQuad, pyautogui.easeOutQuad, pyautogui.easeInOutQuad])[0]

def configread():
    global Resolution
    global speed
    config = configparser.ConfigParser()
    config.read("settings.ini")
    speed = float((config["BotSettings"]["bot_speed"]).split("#")[0])
    n = 0
    for i in ['Red', 'Green', 'Blue']:
        pages[n] = [i, int((config["NumberOfPages"][i]).split("#")[0])]
        n += 1

    setings.append(config["BotSettings"]["Monitor Resolution"].replace('*', 'x'))
    for i in ["level", "location", "mode", "GroupCreate", "heroesSet"]:
        setings.append(config["BotSettings"][i])
    setings.append(int(config["BotSettings"]["monitor"]))
    setings.append(float(config["BotSettings"]["MouseSpeed"]))
    print(setings)
    files = os.listdir('./files/1920x1080/heroes')
    for obj in files:
        for i in range(6):
            rt = (config["Heroes"]["hero" + str(i + 1) + "_Number"]).split("#")[0]
            print(rt)
            if rt != 'auto' and rt != '-':
                if rt == obj.split(".")[0] or rt in obj.split(".")[1]:
                    hero.append(obj)
                    hero_colour.append(obj.split(".")[2])
    for n in range(2):
        for i in range(6):
            rt = (config["Heroes"]["hero" + str(i + 1) + "_Number"]).split("#")[0]
            if rt == 'auto' and n==0:
                hero.append(rt)
                hero_colour.append(rt)
            if rt == '-' and n==1:
                hero.append(rt)
                hero_colour.append(rt)

    print(setings)


def filepp(name, strname):
    try:
        i = 0
        while i < len(name):
            name[i] = strname + "/" + name[i] + ".png"
            i += 1
    except:
        print(strname, "file list got error")


def parslist():
    filepp(Ui_Ellements, "UI_ellements")
    filepp(buttons, "buttons")
    filepp(chekers, "chekers")
    i = 0
    while i < len(hero):
        hero[i] = "heroes/" + hero[i]
        i += 1
    return 0


def screen():
    sct = mss.mss()
	# setings 0: 'MonitorResolution(ex:1920x1080)'
    filename = sct.shot(mon=setings[6], output='files/' + setings[0] + '/screen.png')


def partscreen(x, y, top, left):
    print("entered screenpart")
    import mss.tools
    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": x, "height": y}
        output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
        sct_img = sct.grab(monitor)
	# setings 0: 'MonitorResolution(ex:1920x1080)'
        mss.tools.to_png(sct_img.rgb, sct_img.size, output='files/' + setings[0] + '/part.png')


def findgame():
    global win
    retour = False

    try:
        if(myOS=='linux'):
            screenHW = Wnck.Screen.get_default()
            while Gtk.events_pending():
                Gtk.main_iteration()
            windows = screenHW.get_windows()

            for w in windows:
                if(w.get_name() == 'Hearthstone'):
                    win = w
                    win.activate(int(time.time()))
                    win.make_above()
                    retour = True
        elif(myOS=='windows'):
            win = ahk.win_get(title='Hearthstone')
            retour = True
        else:
            print("OS not supported.")
    except:
        print("No game found.")
    return retour

def battlefind(file, coll):
    if road == True:
        print("back battlefind")
        return
    global sens
    global top
    global left
    herobattle.clear()
	# setings 0: 'MonitorResolution(ex:1920x1080)'
    img = cv2.imread('files/' + setings[0] + '/part.png')
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # преобразуем её в серуюш
	# setings 0: 'MonitorResolution(ex:1920x1080)'
    template = cv2.imread('files/' + setings[0] + '/' + file,
                          cv2.IMREAD_GRAYSCALE)  # объект, который преобразуем в серый, и ищем его на gray_img
    w, h = template.shape[::-1]  # инвертируем из (y,x) в (x,y)`
    result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)

    loc = np.where(result >= 0.75)
    num = 0
    if len(loc[0]) != 0:
        j = 0
        for pt in zip(*loc[::-1]):
            x = int(((pt[0] * 2 + w) / 2) + 60)
            y = int((((pt[1] * 2 + h) / 2) + (windowMP()[3] / 2)))

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
        time.sleep(0.2)
        pyautogui.dragTo(index[0] + 40, index[1] - 30, 0.6, mouse_random_movement())
        pyautogui.click()
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
            x = int(windowMP()[2] / 2)
            y = int(windowMP()[2] / 6)
            pyautogui.dragTo(x, y, 0.6, mouse_random_movement())
            pyautogui.click()
            break


def collect():
    global road
    while True:
        if road == True:
            print("back collect")
            break
	# buttons 22: 'done'
        if not find_ellement(buttons[22], 14):
            pyautogui.moveTo(windowMP()[2] / 2.5, windowMP()[3] / 3.5, setings[7], mouse_random_movement())
            pyautogui.click()
            pyautogui.moveTo(windowMP()[2] / 2, windowMP()[3] / 3.5, setings[7], mouse_random_movement())
            pyautogui.click()
            pyautogui.moveTo(windowMP()[2] / 1.5, windowMP()[3] / 3.5, setings[7], mouse_random_movement())
            pyautogui.click()
            pyautogui.moveTo(windowMP()[2] / 2.7, windowMP()[3] / 1.4, setings[7], mouse_random_movement())
            pyautogui.click()
            pyautogui.moveTo(windowMP()[2] / 1.7, windowMP()[3] / 1.3, setings[7], mouse_random_movement())
            pyautogui.click()
            pyautogui.moveTo(windowMP()[2] / 1.6, windowMP()[3] / 1.3, setings[7], mouse_random_movement())
            pyautogui.click()
            pyautogui.moveTo(windowMP()[2] / 1.8, windowMP()[3] / 1.3, setings[7], mouse_random_movement())
            pyautogui.click()
            pyautogui.moveTo(windowMP()[2] / 1.9, windowMP()[3] / 1.3, setings[7], mouse_random_movement())
            pyautogui.click()
            pyautogui.moveTo(windowMP()[2] / 1.4, windowMP()[3] / 1.3, setings[7], mouse_random_movement())
            pyautogui.click()
            time.sleep(1)
        else:
            while True:
	# buttons 23: 'finishok'
                if find_ellement(buttons[23], 14):
                    for i in range(2):
                        time.sleep(0.5)
	# buttons 0: 'back'
                        find_ellement(buttons[0], 0)
                        time.sleep(0.5)
	# buttons 0: 'back'
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
	# buttons 7: 'play'
    if find_ellement(buttons[7], 14):
        seth()
        print("back nextlevel1")
        return
    tm = int(windowMP()[3] / 3.1)
	# setings 0: 'MonitorResolution(ex:1920x1080)'
    partscreen(int(setings[0].split('x')[0]), tm, tm, 0)
    x = windowMP()[2] / 3.7
    y = windowMP()[3] / 2.2
    temp = speed
    speed = 0
    sens = 0.7
    for n in range(8):
        pyautogui.moveTo(x, y, setings[7])
        pyautogui.click()
        x += windowMP()[2] / 25
    speed = temp
    sens = 0.65
    for i in range(4):
        # Ui_Ellements 13 to 16 : 'bat1' 'bat2' 'bat3' 'bat4'
        x, y = find_ellement(Ui_Ellements[13 + i], 12)
        if x != 0:
            pyautogui.moveTo(x, y + windowMP()[3] / 2.5, setings[7], mouse_random_movement())
            pyautogui.click()
            break
    sens = 0.7
	# buttons 21: 'reveal'
    if find_ellement(buttons[21], 14):
        time.sleep(1)
        pyautogui.moveTo(windowMP()[2] / 2, windowMP()[3] - windowMP()[3] / 4.8, setings[7], mouse_random_movement())
        pyautogui.click()
        nextlvl()
        print("back nextlevel2")
        return
	# buttons 7: 'play'
    find_ellement(buttons[7], 2)
	# buttons 25: 'visit'
    if find_ellement(buttons[25], 14):
        time.sleep(0.5)
        pyautogui.click()
        nextlvl()
        print("call1")
        return
	# Ui_Ellements 19: 'sombody'
    if find_ellement(Ui_Ellements[19], 1):
        temp = random.randint(0, 2)
        if temp == 0:
            x = windowMP()[2] / 2.3
            pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
        if temp == 1:
            x = windowMP()[2] / 1.7
            pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
        if temp == 2:
            x = windowMP()[2] / 1.4
            pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
        pyautogui.click()
	# buttons 18: 'take1'
        find_ellement(buttons[18], 9)
        time.sleep(1)
	# buttons 7: 'play'
        find_ellement(buttons[7], 2)
    while True:
	# Ui_Ellements 24: 'pick'
        if find_ellement(Ui_Ellements[24], 14):
            time.sleep(0.5)
            pyautogui.click()

            nextlvl()
            print("back nextlevel3")
            return 0
	# Ui_Ellements 23: 'startbat'
        if find_ellement(Ui_Ellements[23], 14):
            seth()
            print("back nextlevel4")
            break
        else:
            pyautogui.moveTo(windowMP()[2] / 2, windowMP()[3] - windowMP()[3] / 4.8, setings[7], mouse_random_movement())
            pyautogui.click()
	# buttons 7: 'play'
            find_ellement(buttons[7], 14)
        if road == True:
            print("back nextlevel5")
            return


def Tres():
    y = windowMP()[3] / 2
    temp = random.randint(0, 2)
    if temp == 0:
        x = windowMP()[2] / 2.3
        pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
    if temp == 1:
        x = windowMP()[2] / 1.7
        pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
    if temp == 2:
        x = windowMP()[2] / 1.4
        pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
    pyautogui.click()
    while True:
	# buttons 17: 'take'
        if find_ellement(buttons[17], 14):
            time.sleep(1)
            nextlvl()
            print("back Tres")
            return
	# buttons 28: 'keep'
        if find_ellement(buttons[28], 14):
            time.sleep(1)
            nextlvl()
            print("call2")
            return

	# buttons 27: 'replace'
        if find_ellement(buttons[27], 14):
            time.sleep(1)
            nextlvl()
            print("call3")
            return


def resize():
    for i in range(6):
        if hero[i] != 'heroes/auto' and hero[i] != 'heroes/-':
	# setings 0: 'MonitorResolution(ex:1920x1080)'
            image_path = './files/' + setings[0] + '/' + hero[i] + '/set.png'
            img = Image.open(image_path)
            # получаем ширину и высоту
            width, height = img.size
            print(width, height)
            # открываем картинку в окне
            new_image = img.resize((int(width * 0.65), int(height * 0.65)))
            new_image1 = img.resize((int(width * 0.75), int(height * 0.75)))
	# setings 0: 'MonitorResolution(ex:1920x1080)'
            new_image.save('./files/' + setings[0] + '/' + hero[i] + '/main.png')
	# setings 0: 'MonitorResolution(ex:1920x1080)'
            new_image1.save('./files/' + setings[0] + '/' + hero[i] + '/group.png')


def abilicks(index):
    heroTEMP.clear()
    for i in range(3):
        if hero_colour[i] == index:
            heroTEMP.append(hero[i])
    print(index)
    print("Hero dump",heroTEMP)
    for obj in heroTEMP:
        if obj == 'heroes/1.Cariel Roame.Red':
            if raund > 1 and raund % 2 == 0:
                if find_ellement(obj + '/abilics/2.png', 14):
                    return False
            if raund == 1:
                if find_ellement(obj + '/abilics/1.png', 14):
                    return True
            pyautogui.moveTo(int(windowMP()[2] / 2.5), int(windowMP()[2] / 4), setings[7], mouse_random_movement())
            pyautogui.click()
            return True

        elif obj == 'heroes/3.Milhous Manashtorm.Blue':
            if raund == 1:
                if find_ellement(obj + '/abilics/1.png', 14):
                    return False
            if raund == 3:
                if find_ellement(obj + '/abilics/3.png', 14):
                    return False
            if raund > 1:
                if find_ellement(obj + '/abilics/2.png', 14):
                    return True
            pyautogui.moveTo(int(windowMP()[2] / 2.5), int(windowMP()[2] / 4), setings[7], mouse_random_movement())
            pyautogui.click()
            return True

        elif obj == 'heroes/2.Tirande.Green':
            if raund % 2 == 1:
                if find_ellement(obj + '/abilics/1.png', 14):
                    return True
            if raund % 2 == 0:
                if find_ellement(obj + '/abilics/3.png', 14):
                    return False
            pyautogui.moveTo(int(windowMP()[2] / 2.5), int(windowMP()[2] / 4), setings[7], mouse_random_movement())
            pyautogui.click()
            return True
        elif obj == 'heroes/38':
            if raund == 1:
                if find_ellement(obj + '/abilics/1.png', 14):
                    return False
            if raund == 3:
                if find_ellement(obj + '/abilics/3.png', 14):
                    return False
            if raund > 1:
                if find_ellement(obj + '/abilics/2.png', 14):
                    return True
            pyautogui.moveTo(int(windowMP()[2] / 2.5), int(windowMP()[2] / 4), setings[7], mouse_random_movement())
            pyautogui.click()
            return True
        elif obj == 'heroes/40':
            if raund == 1:
                if find_ellement(obj + '/abilics/1.png', 14):
                    return False
            if raund == 3:
                if find_ellement(obj + '/abilics/3.png', 14):
                    return False
            if raund > 1:
                if find_ellement(obj + '/abilics/2.png', 14):
                    return True
            pyautogui.moveTo(int(windowMP()[2] / 2.5), int(windowMP()[2] / 4), setings[7], mouse_random_movement())
            pyautogui.click()
            return True
        elif obj == 'heroes/42':
            if raund == 1:
                if find_ellement(obj + '/abilics/1.png', 14):
                    return False
            if raund == 3:
                if find_ellement(obj + '/abilics/3.png', 14):
                    return False
            if raund > 1:
                if find_ellement(obj + '/abilics/2.png', 14):
                    return True
    pyautogui.moveTo(int(windowMP()[2] / 2.5), int(windowMP()[2] / 4), setings[7], mouse_random_movement())
    pyautogui.click()
    return True


def atack(i, enemyred, enemygreen, enemyblue, enemynoclass, mol):
    x = int(i[1])
    y = int(i[2])
    print("Attack function")
    if i[0] == 'Red':
        print("open Red")
        pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
        pyautogui.click()
        time.sleep(0.2)
        if abilicks('Red'):
            if move(enemygreen):
                if move(mol):
                    if move(enemynoclass):
                        rand(enemyred, enemygreen, enemyblue, enemynoclass)
    if i[0] == 'Green':
        print("open Green")
        pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
        pyautogui.click()
        time.sleep(0.2)
        if abilicks('Green'):
            if move(enemyblue):
                if move(mol):
                    if move(enemynoclass):
                        rand(enemyred, enemygreen, enemyblue, enemynoclass)
    if i[0] == 'Blue':
        print("open blue")
        pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
        pyautogui.click()
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
        pyautogui.moveTo(windowMP()[2] / 2, windowMP()[3] - windowMP()[3] / 4.6, setings[7], mouse_random_movement())
        speed = 0
        sens = 0.85
	# buttons 20: 'onedie'
        find_ellement(buttons[20], 14)
	# chekers 13: 'win'
        if find_ellement(chekers[13], 1):
            pyautogui.moveTo(windowMP()[2] / 2, windowMP()[3] - windowMP()[3] / 4.6, setings[7], mouse_random_movement())
            while True:
	# Ui_Ellements 18: 'findthis'
                if not find_ellement(Ui_Ellements[18], 1):
                    pyautogui.click()
                    time.sleep(0.5)
                else:
                    Tres()
                    break
	# Ui_Ellements 29: 'replace_grey'
                if not find_ellement(Ui_Ellements[29], 1):
                    pyautogui.click()
                    time.sleep(0.5)
                else:
                    Tres()
                    break
	# Ui_Ellements 31: 'presents_thing'
                if find_ellement(Ui_Ellements[31], 1):
                    collect()
                    break

	# buttons 15: 'startbattle'
	# buttons 16: 'startbattle1'
        if find_ellement(buttons[15], 1) or find_ellement(buttons[16], 1):  # finds startbattle.png
            print(windowMP())
            herobattlefin.clear()
            tmp = int(windowMP()[3] / 2)
            tmp = int(windowMP()[3] / 2)
	# setings 0: 'MonitorResolution(ex:1920x1080)'
            partscreen(int(setings[0].split('x')[0]), tmp, 0, 0)
            temp = speed
            sens = 0.8
            # поиск врага
	# Ui_Ellements 9: 'red'
            enemyred = find_ellement(Ui_Ellements[9], 12)
	# Ui_Ellements 2: 'green'
            enemygreen = find_ellement(Ui_Ellements[2], 12)
	# Ui_Ellements 1: 'blue'
            enemyblue = find_ellement(Ui_Ellements[1], 12)
	# Ui_Ellements 12: 'noclass'
            enemynoclass = find_ellement(Ui_Ellements[12], 12)
            print("red: ", enemyred)
            print("green: ", enemygreen)
            print("blue: ", enemyblue)
            print("noclass: ", enemynoclass)
	# Ui_Ellements 11: 'sob'
            mol = find_ellement(Ui_Ellements[11], 12)
            pyautogui.moveTo(windowMP()[2] / 2, windowMP()[3] - windowMP()[3] / 4.8, setings[7], mouse_random_movement())
            pyautogui.click()
            time.sleep(1)
	# setings 0: 'MonitorResolution(ex:1920x1080)'
            partscreen(int(setings[0].split('x')[0]), tmp, tmp, 0)
            print("enter serch Red")
	# Ui_Ellements 9: 'red'
            battlefind(Ui_Ellements[9], 'Red')  # find all yr Red
            if len(herobattlefin) != 3:
                print("enter serch Green")
	# Ui_Ellements 2: 'green'
                battlefind(Ui_Ellements[2], 'Green')  # find all yr Green
            if len(herobattlefin) != 3:
                print("enter serch Blue")
	# Ui_Ellements 1: 'blue'
                battlefind(Ui_Ellements[1], 'Blue')  # find all yr Blue
            print("cords of my heroes ")
            print(herobattlefin)
            for i in herobattlefin:
                pyautogui.moveTo(windowMP()[2] / 2, windowMP()[3] - windowMP()[3] / 4.8, setings[7], mouse_random_movement())
                pyautogui.click()
                print("print index", i)
                atack(i, enemyred, enemygreen, enemyblue, enemynoclass, mol)
                time.sleep(0.1)
            sens = 0.75
            speed = temp
            i = 0
            while True:
	# buttons 14: 'allready'
                if not find_ellement(buttons[14], 2):
                    break
                if i > 10:
                    pyautogui.rightClick()
                    if(myOS=='windows'):
                        ahk.show_warning_traytip("Battle", "Battle error,please write what happend on github issue")
                    else :
                        print("Battle error,please write what happend on github issue")
	# buttons 15: 'startbattle'
                    find_ellement(buttons[15], 2)
                    break
                i += 1
            time.sleep(3)
            raund += 1


def seth():
    debug("[ SETH - START]")
    if road == True:
        print("back set1")
        return
    global speed
    global sens
    while True:
        time.sleep(0.5)
        # buttons 5: 'num'
    # buttons 5: 'num'
        if find_ellement(buttons[5], 1):
            break
    debug("windowsMP() : ", windowMP())
    x = windowMP()[0] + (windowMP()[2] / 2.6)
    y = windowMP()[1] + (windowMP()[3] * 0.92)
    i = 0
    temp = speed
    speed = 0
    sens = 0.85
    i = 0
    # setings 5: 'heroSet(ex:True)'
    if setings[5] == "True":
    # buttons 14: 'allready'
        while not find_ellement(buttons[14], 1):
            print('Entrance')
            sens = 0.75
            pyautogui.moveTo(x, y, setings[7])
            #debug("mouse move to : ", x, y, setings[7])
            for n in range(3):
                if i >= 7:
                    pyautogui.moveTo(windowMP()[0] + (windowMP()[2] / 2), windowMP()[1] + (windowMP()[3] * 0.92), setings[7], mouse_random_movement())
                    pyautogui.dragTo(windowMP()[0] + (windowMP()[2] / 2), (windowMP()[1] + (windowMP()[3] * 0.92)) - windowMP()[3] / 3, 0.6, mouse_random_movement())
                    break
                if find_ellement(hero[n] + '/set.png', 6):
                    time.sleep(0.2)
                    pyautogui.dragTo(x, y - windowMP()[3] / 3, 0.6, mouse_random_movement())
                    time.sleep(0.5)
                    break
            else :
                x += windowMP()[2] / 22.5
                if x > windowMP()[2] / 1.5:
                    x = windowMP()[0] + (windowMP()[2] / 2.85)
            i += 1
        print('Optout')
        speed = temp
        sens = 0.7
        pyautogui.moveTo(windowMP()[0] + (windowMP()[2]*0.1), windowMP()[1] + (windowMP()[3]*0.1), setings[7], mouse_random_movement())
        time.sleep(1)
    # buttons 14: 'allready'
    find_ellement(buttons[14], 9)
    time.sleep(1)
    battle()
    debug("[ SETH - END]")
    return




def levelchoice():
    global sens
    temp = sens
    sens = 0.65
    time.sleep(0.5)
    pyautogui.moveTo(windowMP()[2] / 1.5, windowMP()[3] / 2, setings[7], mouse_random_movement())
    for i in range(70):
        pyautogui.scroll(1)
	# setings 2: 'location(ex:TheBarrens)'
    if setings[2] == "Felwood":
	# Ui_Ellements 26: 'Felwood'
        find_ellement(Ui_Ellements[26], 14)
	# setings 2: 'location(ex:TheBarrens)'
    if setings[2] == "Winterspring":
	# Ui_Ellements 25: 'Winterspring'
        find_ellement(Ui_Ellements[25], 14)
	# setings 2: 'location(ex:TheBarrens)'
    if setings[2] == "The Barrens":
	# Ui_Ellements 22: 'travel'
        find_ellement(Ui_Ellements[22], 14)
    pyautogui.moveTo(windowMP()[2] / 2, windowMP()[3] / 2, setings[7], mouse_random_movement())
    time.sleep(0.5)
	# setings 3: 'mode(ex:Heroic)'
    if setings[3] == "Normal":
	# Ui_Ellements 27: 'normal'
        find_ellement(Ui_Ellements[27], 14)
	# setings 3: 'mode(ex:Heroic)'
    if setings[3] == "Heroic":
	# Ui_Ellements 28: 'heroic'
        find_ellement(Ui_Ellements[28], 14)
    sens = temp


def battlego():
    if road == True:
        print("back battlgo")
        return
    global sens
    print("Битва")
    time.sleep(1)
    #Find PVE adventure payed and free
	# Ui_Ellements 0: 'battle'
	# Ui_Ellements 32: 'free_battle'
    find_ellement(Ui_Ellements[0], 14) or find_ellement(Ui_Ellements[32],14)
    while True:
        pyautogui.moveTo(windowMP()[2] / 1.5, windowMP()[3] / 2)
        levelchoice()
	# chekers 15: 'levelstarted'
        if find_ellement(chekers[15], 14):
            time.sleep(1)
            nextlvl()
            print("yeh here stops")
            where()
            break
	# buttons 7: 'play'
        if find_ellement(buttons[7], 14):
	# buttons 7: 'play'
            find_ellement(buttons[7], 14)
            seth()
            return
	# buttons 10: 'sta'
        if find_ellement(buttons[10], 14):
            break
    while True:
        time.sleep(1)
	# setings 1: 'level(ex:20)'
        if find_ellement("levels/" + setings[1] + ".png", 14):
            time.sleep(0.5)
	# buttons 11: 'start'
            find_ellement(buttons[11], 14)
            break
	# buttons 9: 'sec'
        if find_ellement(buttons[9], 2):
            pass
        else:
	# buttons 26: 'fir'
            find_ellement(buttons[26], 2)
    while True:
	# chekers 2: 'find'
        if not find_ellement(chekers[2], 2):
	# buttons 12: 'start1'
            find_ellement(buttons[12], 2)
            break
    while True:
        time.sleep(0.2)
	# buttons 7: 'play'
        if find_ellement(buttons[7], 0):
            time.sleep(0.5)
            break
        else:
	# buttons 13: 'submit'
            find_ellement(buttons[13], 2)
    seth()
    print("back set2")
    return


def where():
    if road == True:
        print("back where")
        return True
	# setings 4: 'GroupCreate(ex:True)'
    if setings[4] == 'False':
        time.sleep(1)
	# chekers 21: 'menu'
        if find_ellement(chekers[21], 1):
            battlego()
	# buttons 4: 'join_button'
        find_ellement(buttons[4], 0)
	# buttons 0: 'back'
        find_ellement(buttons[0], 0)
    else:
	# buttons 4: 'join_button'
        find_ellement(buttons[4], 0)
	# Ui_Ellements 3: 'group'
        find_ellement(Ui_Ellements[3], 0)
	# buttons 0: 'back'
        find_ellement(buttons[0], 0)
    return True


def pagech(page, coll):
    print("hero number is", coll)
    print(hero_colour[coll])
    print(pages)
    for i in pages:
        if hero_colour[coll] in i:
            print("color found")
            num = i[1]
            print(num)
    if int(num) > 1:
        if page != num:
	# Ui_Ellements 4: 'next'
            find_ellement(Ui_Ellements[4], 0)
            time.sleep(1)
            page += 1
        else:
            while page != 1:
	# Ui_Ellements 10: 'prev'
                find_ellement(Ui_Ellements[10], 0)
                page -= 1
                time.sleep(1)
    return page


def find(n):
    global speed
    temp = speed
    speed = 0
    change(n)
    page = 1
    attempt = 0
    while True:
        attempt += 1
        if attempt > 4:
            change(n)
        if find_ellement(hero[n] + "/main.png", 6):
            print('нашёл')
	# chekers 8: 'drop'
            find_ellement(chekers[8], 14)
            return True
        else:
            page = pagech(page, n)
    speed = temp


def change(index):
    if hero_colour[index] == 'Red':
	# Ui_Ellements 6: 'page_1'
        find_ellement(Ui_Ellements[6], 9)
    if hero_colour[index] == 'Green':
	# Ui_Ellements 7: 'page_2'
        find_ellement(Ui_Ellements[7], 9)
    if hero_colour[index] == 'Blue':
	# Ui_Ellements 8: 'page_3'
        find_ellement(Ui_Ellements[8], 9)
    print("page change for hero", index)
    time.sleep(1)


def test():
    if find_ellement(hero[0] + "/group.png", 1):
        print("yes")

def group_create():
    if road == True:
        print("back group")
        return
    global speed
    global left
    global top
    global sens
    time.sleep(1)
	# chekers 22: 'party'
    while not find_ellement(chekers[22], 1):
        where()
	# chekers 4: 'group_find'
    if find_ellement(chekers[4], 3) == 6:
	# buttons 2: 'create'
        find_ellement(buttons[2], 0)
        time.sleep(1.5)
        print(windowMP())
        x = int(windowMP()[2] / 1.3)
        y = int(windowMP()[3] / 9)
	# chekers 14: 'ifrename'
        # while not find_ellement(chekers[14], 14):
        pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
        time.sleep(0.5)
        pyautogui.click()
        temp = speed
        speed = 0
        #ahk.send_input('Botwork', 0)
        pyautogui.write('Botwork', interval=0.25)
	# Ui_Ellements 10: 'prev'
        find_ellement(Ui_Ellements[10], 0)
        time.sleep(1)
        fx=0
        for i in range(6):
            if hero[i] != 'heroes/auto' and hero[i] != 'heroes/-':
                print("Starting adding hero ", i)
                find(i)
            if hero[i] == 'heroes/auto':
                fx += 1
        print('how many auto',fx)
        if fx != 0:
            print("Add heroes")
	# Ui_Ellements 6: 'page_1'
            find_ellement(Ui_Ellements[6], 14)
            time.sleep(0.5)
            find_merc(fx)
        speed = temp
	# buttons 8: 'ready'
        find_ellement(buttons[8], 0)
        time.sleep(0.2)
	# buttons 1: 'continue'
        find_ellement(buttons[1], 0)
        time.sleep(0.2)
	# Ui_Ellements 6: 'page_1'
        find_ellement(Ui_Ellements[6], 2)
        battlego()
    else:
        time.sleep(1)
	# chekers 17: 'cords-search'
        x, y = find_ellement(chekers[17], 15)
        x = x - int(windowMP()[2] / 9)
        y = y + int(windowMP()[3] / 18.5)
        add = 0
        herocust = 0
        autoadd = 0
        temphero = []
        for i in range(6):
            if hero[i] != 'heroes/auto' and hero[i] != 'heroes/-':
                herocust += 1
            if hero[i] == 'heroes/auto':
                autoadd += 1
        for i in range(herocust + autoadd):
            temp = sens
            sens = 0.65
            pyautogui.moveTo(x, y, setings[7], mouse_random_movement())  # Moves the mouse instantly to absolute screen position
            pyautogui.click()
            if i <= herocust - 1:
                bool_check = False
                time.sleep(0.2)
                for i in range(herocust):
                    if find_ellement(hero[i] + "/group.png", 1):
                        bool_check = True
                        temphero.append(i)
                        y = y + int(windowMP()[3] / 19)
                print("Temphero is ",temphero)
                if bool_check is False:
                    sens = 0.85
                    pyautogui.dragTo(x - 600, y, 0.6, mouse_random_movement())
                sens = temp
            if i > autoadd - 1:
                temp = sens
                sens = 0.85
                time.sleep(0.5)
	# chekers 0: '30lvl'
	# chekers 19: '30lvl1'
	# chekers 20: '30lvl2'
                if find_ellement(chekers[0], 1) or find_ellement(chekers[19], 1) or find_ellement(chekers[20], 1):
                    pyautogui.dragTo(x - 600, y, 0.6, mouse_random_movement())
                    add += 1
                else:
                    y = y + int(windowMP()[3] / 17.2)
        sens = 0.7
	# buttons 8: 'ready'
        find_ellement(buttons[8], 14)
        time.sleep(0.5)
        for i in range(herocust):
            if i not in temphero:
                print("Find hero with index ", i)
                find(i)
        if add != 0:
            print("Add heroes")
	# Ui_Ellements 6: 'page_1'
            find_ellement(Ui_Ellements[6], 14)
            time.sleep(0.5)
            find_merc(add)
        while True:
	# buttons 8: 'ready'
            if find_ellement(buttons[8], 14):
                time.sleep(0.5)
	# buttons 1: 'continue'
                find_ellement(buttons[1], 14)
                break
	# chekers 21: 'menu'
        while not chekers[21]:
	# buttons 0: 'back'
            find_ellement(buttons[0],14)
            time.sleep(0.5)
        sens = temp
        time.sleep(0.5)
        battlego()

def find_merc(n):
    time.sleep(0.5)
    global left
    global top
    global speed
    global sens
    i = 0
    temp1 = sens
    sens = 0.9
    temp = speed
    speed = 0
    while i < n:
        print("enter iteration loop")
        x = int(windowMP()[2] / 7.5)
        y = int(windowMP()[3] / 3.5)
        top = int(windowMP()[3] / 5.76)
        left = int(windowMP()[2] / 5.2)
        h = 0
        while h < 2:
            print("enter height loop")
            left = int(windowMP()[2] / 5.2)
            j = 0
            while j < 3:
                if i >=n:
                    break
                print("enter width loop")
                partscreen(x, y, top, left)
	# chekers 12: 'text'
                if find_ellement(chekers[12], 7):
                    print(xm, ym)
	# chekers 9: '301'
	# chekers 10: '302'
	# chekers 18: '303'
                    if find_ellement(chekers[9], 7) is False and find_ellement(chekers[10],7) is False and find_ellement(chekers[18], 7) is False:
                        print("found object")
	# chekers 11: 'taken'
                        if not find_ellement(chekers[11], 7):
	# chekers 8: 'drop'
                            find_ellement(chekers[8], 7)
                            i += 1
                            print("droped the object")

                j += 1
                left += int(windowMP()[2] / 7)
                print("go next element on line")
            top += int(windowMP()[3] / 3)
            print("go next line")
            h += 1
	# Ui_Ellements 4: 'next'
        find_ellement(Ui_Ellements[4], 0)
    speed = temp
    sens = temp1


def find_ellement(file, index):
    if road == True:
        return
    global sens
    global top
    global left
    time.sleep(speed)
    if index == 12:
	# setings 0: 'MonitorResolution(ex:1920x1080)'
        img = cv2.imread('files/' + setings[0] + '/part.png')
	# chekers 8: 'drop'
    elif index == 7 and file != chekers[8]:
	# setings 0: 'MonitorResolution(ex:1920x1080)'
        img = cv2.imread('files/' + setings[0] + '/part.png')
    else:
        screen()
	# setings 0: 'MonitorResolution(ex:1920x1080)'
        img = cv2.imread('files/' + setings[0] + '/screen.png')  # картинка, на которой ищем объект
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # преобразуем её в серуюш
	# setings 0: 'MonitorResolution(ex:1920x1080)'
    template = cv2.imread('files/' + setings[0] + '/' + file,
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
	# chekers 7: 'shab'
	# Ui_Ellements 5: 'one'
        if (index == 6 or file == Ui_Ellements[5] or file == chekers[7]):
            global xm
            global ym
            xm = x
            ym = y
            return True
	# chekers 8: 'drop'
        if file == chekers[8]:
            if index == 7:
                xm += left
                ym += top
            pyautogui.moveTo(xm, ym, setings[7], mouse_random_movement())
            time.sleep(0.5)
            if index==14:
                y=y-windowMP()[3]/1.9
            pyautogui.dragTo(x, y, 0.6, mouse_random_movement())
            return True
	# chekers 5: 'level_check'
        if file == chekers[5]:
            pyautogui.moveTo(x, y + 70, setings[7], mouse_random_movement())
            pyautogui.click()
            return True
	# buttons 5: 'num'
        if file == buttons[5]:
            pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
            return True
	# chekers 3: 'goto'
        if file == chekers[3]:
            pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
        if index == 1:
            return True
        if index == 7:
            xm = x
            ym = y
            return True
        p = random.randint(-2, 2)
        s = random.randint(-2, 2)
        pyautogui.moveTo(x + p, y + s, setings[7], mouse_random_movement())  # Moves the mouse instantly to absolute screen position
        pyautogui.click()  # Click the primary mouse button
	# buttons 7: 'play'
        if file == buttons[7]:
            return True
	# Ui_Ellements 3: 'group'
        if file == Ui_Ellements[3]:
            time.sleep(0.5)
            pyautogui.click()
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
	# buttons 7: 'play'
        if file == buttons[7]:
            return False
	# buttons 0: 'back'
	# buttons 4: 'join_button'
	# Ui_Ellements 3: 'group'
        if file != buttons[4] and file != Ui_Ellements[3] and file != buttons[0]:
            where()



def main():
    global road
    print("start")
    try:
        #ahk.show_info_traytip("Starting", "loading files", slient=False, blocking=True)
        configread()
        findgame()
        parslist()
        resize()
        if(myOS=="windows"):
            ahk.show_info_traytip("started", "all files loaded successfully", slient=False, blocking=True)
            win.show()
            win.restore()
            win.maximize()
            win.to_top()
            win.maximize()
            win.to_top()
            win.activate()
        while True:
            print("Loop start")
            if findgame():
                road = False
                where()
            else:
                print("Not found Game window.")
                time.sleep(5)
    except Exception as E:
        print("Error", E)

if __name__ == '__main__':
    main()
