import time
import cv2
import numpy as np
from ahk import AHK
from mss import mss
import mss
import configparser
import random

ahk = AHK()
global xm
xm=0
global ym
ym=0
global monik
global speed
global sens
global zipp
global zipchek
zipp=False
zipchek =False
sens=0.75
#for_future=['','','','','','','','','','','','','','','','','','','',]
#Ui-ellements
Ui_Ellements=['battle','blue','green','group','next','one','page_1','page_2','page_3','red','prev','sob','noclass']
#buttons
buttons=['back','continue','create','del','join_button','num','ok','play','ready','sec','sta','start','start1','submit','allready','startbattle','startbattle1']
#chekers
chekers=['30lvl','empty_check','find','goto','group_find','level_check','rename','shab','drop','301','302','taken','text']
#levels
levels=['level15']
#heroes
hero=['','','']
hero_colour=['','','']
pages=['','','']
heroNUM=['','','']
#for battle
herobattle=[]
#damp
enemywiz=[0,0,0]
heroTEMP=[]
#img list
picparser=['/1.png','/2.png','/3.png','/4.png']

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
    if Resolution=='2560*1440':
        Resolution='2560x1440'
    if Resolution=='1920*1080':
        Resolution='1920x1080'

    print(pages[0],pages[1],pages[2])


    print(monik,speed,hero)
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
        hero[i]="heroes/"+hero[i]
        i += 1
    return 0
def screen():
    global Resolution
    sct = mss.mss()
    filename = sct.shot(mon=monik, output='files/'+Resolution+'/screen.png')
def partscreen(x,y,top,left):
    global Resolution
    import mss.tools
    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": x, "height": y}
        output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output='files/'+Resolution+'/part.png')
def findgame():
     global win
     win = ahk.win_get(title='Hearthstone')
     if win.exist:
         print("Игра найдена")
         return True
     else:
         print("Игра не найдена")
         return False


def battlefind(file,coll):
    global sens
    global top
    global left
    global Resolution
    img = cv2.imread('files/' + Resolution + '/part.png')
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # преобразуем её в серуюш
    template = cv2.imread('files/' + Resolution + '/' + file,
                          cv2.IMREAD_GRAYSCALE)  # объект, который преобразуем в серый, и ищем его на gray_img
    w, h = template.shape[::-1]  # инвертируем из (y,x) в (x,y)`
    result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)

    loc = np.where(result >= sens)
    if len(loc[0]) != 0:
        j = 0
        for pt in zip(*loc[::-1]):
            Flag = False
            for num in range(3):
                if pt[0] < enemywiz[num] + 10 and pt[0] > enemywiz[num] - 10:
                    Flag = True
                    pass
            if not Flag:
                for num in range(3):
                    if enemywiz[num] == 0:
                        enemywiz[num] = pt[0]
                        x = ((pt[0] * 2 + w) / 2)+60
                        y = (((pt[1] * 2 + h) / 2) + (win.rect[3]/2))
                        herobattle.append([coll,x,y])
                        j += 1
                        break
        for i in range(2):
            enemywiz[i] = 0
        return 0




def move(index):
    if index!= (0, 0):
        ahk.mouse_drag(index[0]+60,index[1]-30, relative=False)
        ahk.click()
        return False
    else:
        return True
def rand(enemyred, enemygreen ,enemyblue ,enemynoclass):
    while True:
        a = random.randint(0, 3)
        if a == 0:
            if not move(enemygreen):
                break
        if a == 1:
            if not move(enemyred):
                break
        if a == 2:
            if not move(enemyblue):
                break
        if a == 3:
            if not move(enemynoclass):
                break

def abilicks(index):
    heroTEMP.clear()
    for i in range(3):
        if hero_colour[i] == index:
            heroTEMP.append(hero[i])
    print(index)
    print( heroTEMP)
    for obj in heroTEMP:
        if obj=='heroes/1' and raund>1:
                find_ellement(obj + '/abilics/2.png', 9)
        elif obj=='heroes/3':
            find_ellement(obj + '/abilics/2.png', 9)
        else:
            find_ellement(obj + '/abilics/1.png', 9)

def atack(i,enemyred, enemygreen ,enemyblue ,enemynoclass,mol):
    x=int(i[1])
    y=int(i[2])
    if i[0]=='Red':
        ahk.mouse_move(x,y, speed=3)
        ahk.click()
        ahk.mouse_move(x, y+300, speed=3)
        time.sleep(0.2)
        abilicks('Red')
        if move(enemygreen):
            if move(mol):
                rand(enemyred, enemygreen ,enemyblue ,enemynoclass)
    if i[0] == 'Green':
        ahk.mouse_move(x, y, speed=3)
        ahk.click()
        ahk.mouse_move(x, y +300, speed=3)
        time.sleep(0.2)
        abilicks('Green')
        if move(enemyblue):
            if move(mol):
                rand(enemyred, enemygreen ,enemyblue ,enemynoclass)
    if i[0] == 'Blue':
        ahk.mouse_move(x, y, speed=3)
        ahk.click()
        ahk.mouse_move(x, y +300, speed=3)
        time.sleep(0.2)
        abilicks('Blue')
        if move(enemyred):
            if move(mol):
                rand(enemyred, enemygreen ,enemyblue ,enemynoclass)


def battle():
    global raund
    global sens
    global zipchek
    global speed
    raund = 1
    while True:
        speed = 0
        if find_ellement(buttons[15], 1) or find_ellement(buttons[16], 1) :
            herobattle.clear()
            ahk.mouse_move(100, 100, speed=3)  # Moves the mouse instantly to absolute screen position
            ahk.click()
            tmp=int(win.rect[3] / 2)
            partscreen(2560, tmp, 0, 0)
            temp = speed

            sens=0.75
            # поиск врага
            enemyred = find_ellement(Ui_Ellements[9], 12)
            enemygreen =find_ellement(Ui_Ellements[2], 12)
            enemyblue=find_ellement(Ui_Ellements[1], 12)
            enemynoclass=find_ellement(Ui_Ellements[12], 12)
            mol = find_ellement(Ui_Ellements[11], 12)
            partscreen(2560, tmp, tmp, 0)
            if 'Red' in hero_colour:
                battlefind(Ui_Ellements[9], 'Red')
            if 'Green' in hero_colour:
                battlefind(Ui_Ellements[2], 'Green')
            if 'Blue' in hero_colour:
                battlefind(Ui_Ellements[1], 'Blue')
            for i in herobattle:
                print(i)
                atack(i,enemyred, enemygreen ,enemyblue ,enemynoclass,mol)
            sens = 0.75
            speed = temp

            time.sleep(1)
            find_ellement(buttons[14], 9)
            time.sleep(5)
            raund+=1

def set():
    global speed
    global sens
    while True:
        if find_ellement(buttons[5],1):
            break
    print(win.rect)
    x = win.rect[2]/2.85
    y = win.rect[3]-win.rect[3]/10
    i=0
    temp = speed
    speed = 0
    sens=0.6
    while i<3:
        ahk.mouse_position = (x, y)
        for n in range(3):
            if find_ellement(hero[n] + '/set.png', 6):
                ahk.mouse_drag(x, y - 500, relative=False)
                i+=1
            x += win.rect[2] / 57
        if x>1700:
            x= win.rect[2]/2.85
    speed = temp
    sens = 0.7
    ahk.mouse_move(200, 200, speed=3)
    time.sleep(1)
    find_ellement(buttons[14], 9)
    time.sleep(5)
    battle()
def battlego():
    print("Битва")
    time.sleep(1)
    find_ellement(Ui_Ellements[0],0)
    time.sleep(2.5)
    if find_ellement(buttons[7],0):
        set()
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
    find_ellement(buttons[13],9)
    time.sleep(5)
    find_ellement(buttons[7],0)
    set()

def where():
    find_ellement(buttons[4],0)
    time.sleep(0.5)
    find_ellement(Ui_Ellements[3],0)
    find_ellement(buttons[0],0)

    return True
def pagech(page,coll):
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
    change(n)
    page = 1
    while True:
        for num in range(2):
            for index in range(4):
                if find_ellement(hero[n] + picparser[index], 6):
                    find_ellement(chekers[8], 0)
                    heroNUM[n]=picparser[index]
                    return True
        page =pagech(page,n)



def change(index):
    if hero_colour[index] == 'Red':
        find_ellement(Ui_Ellements[6], 9)
    if hero_colour[index] =='Green':
        find_ellement(Ui_Ellements[7], 9)
    if hero_colour[index] =='Blue':
        find_ellement(Ui_Ellements[8], 9)
    time.sleep(1)

def group_create():
    global speed
    global left
    global top
    time.sleep(1)
    if find_ellement(chekers[4],3) ==6:
        find_ellement(buttons[2],0)
        time.sleep(1)
        find_ellement(chekers[6],0)
        temp = speed
        speed = 0
        ahk.send_input('Botwork',0)
        find_ellement(Ui_Ellements[10], 0)
        find(0)
        find(1)
        find(2)
        speed=temp
        find_ellement(buttons[8],0)
        ahk.mouse_move(100, 100, speed=3)
        find_ellement(buttons[1],0)
    else:
        time.sleep(1)
        if find_ellement(chekers[1],2) == True:
            x = win.rect[2] / 1.4
            y = win.rect[3] /2.5 #fix later
            ahk.mouse_move(x, 440, speed=3)  # Moves the mouse instantly to absolute screen position
            ahk.click()
            time.sleep(1)
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
                ahk.mouse_move(100, 100, speed=3)
                find_ellement(buttons[0],0)
                battlego()


        else:
            i=0
            temp = speed
            speed = 0.2
            while i<3:
                x = int(win.rect[2] / 7.5)
                y = int(win.rect[3] / 3.5)
                top =int(win.rect[3] / 5.76)
                left = int(win.rect[2] / 5.2)
                h = 0
                while h < 2:
                    left = int(win.rect[2] / 5.2)
                    j=0
                    while j<3:
                        partscreen(x,y,top,left)
                        if find_ellement(chekers[12],7):
                            print(xm,ym)
                            a=find_ellement(chekers[9], 7)
                            b=find_ellement(chekers[10], 7)
                            if a is False and b is False:
                                if not find_ellement(chekers[11],7):
                                    find_ellement(chekers[8], 7)
                                    i+=1
                        j+=1
                        left+=365
                    top+=480
                    h+=1
                find_ellement(Ui_Ellements[4], 0)
        speed = temp
        find_ellement(buttons[8],0)
        ahk.mouse_move(100, 100, speed=3)
        time.sleep(1)
        find_ellement(buttons[0], 0)
        time.sleep(2)
        battlego()



def find_ellement(file,index):
    global sens
    global top
    global left
    global Resolution
    time.sleep(speed)
    if index ==7 or index ==12 and file != chekers[8] :
        img = cv2.imread('files/'+Resolution+'/part.png')
    else:
        screen()
        img = cv2.imread('files/'+Resolution+'/screen.png')  # картинка, на которой ищем объект
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # преобразуем её в серуюш
    template = cv2.imread('files/'+Resolution+'/'+file,cv2.IMREAD_GRAYSCALE)  # объект, который преобразуем в серый, и ищем его на gray_img
    w, h = template.shape[::-1]  # инвертируем из (y,x) в (x,y)`
    result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)

    loc = np.where(result >= sens)
    if len(loc[0]) !=0:
        for pt in zip(*loc[::-1]):
            pt[0] + w
            pt[1] + h
        x=int((pt[0]*2+w)/2)
        y=int((pt[1]*2+h)/2)
        print("Found "+file,x,y)
        if index==12:
            return (x,y)
        if (index==6 or file == Ui_Ellements[5] or file == chekers[7]):
            global xm
            global ym
            xm=x
            ym=y
            return True
        if file == chekers[8]:
            if index ==7:
                xm+=left
                ym+=top
            ahk.mouse_move(xm, ym, speed=2)
            time.sleep(0.5)
            ahk.mouse_drag(x, y, relative=False)
            return True
        if file == chekers[5]:
            ahk.mouse_move(x, y+70, speed=3)
            ahk.click()
            return True
        if file ==buttons[5]:
            ahk.mouse_move(x, y, speed=5)
            return True
        if index == 1:
            return True
        if index == 7:
            xm = x
            ym = y
            return True
        ahk.mouse_move(x, y, speed=5)  # Moves the mouse instantly to absolute screen position
        ahk.click()  # Click the primary mouse button
        if file ==buttons[7]:
            return True
        if file == Ui_Ellements[3]:
            group_create()
    else:
        print("Not found  "+file)
        if index == 12:
            return 0,0
        if index ==6:
            return False
        if index ==7:
            return False
        if index== 3:
            return 6
        if index==2 or index=='battletag':
            return True
        if index ==1 or index ==9 or index==12 :
            return False
        if file ==buttons[7]:
            return False
        if (file !=buttons[4] and file !=Ui_Ellements[3] and file !=buttons[0]):
            where()


def main():
    ahk.show_info_traytip("Starting", "loading files", slient=False, blocking=True)
    configread()
    findgame()
    parslist()
    ahk.show_info_traytip("started", "all files loaded sucsessfuly", slient=False, blocking=True)



    win.show()
    win.restore()
    win.maximize()
    win.to_top()
    win.maximize()
    win.to_top()
    win.activate()
    while True:
        if findgame():
            where()

if __name__ == '__main__':
    main()



