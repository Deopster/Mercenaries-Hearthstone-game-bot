import time
from ahk import AHK
import configparser
import ahk_binary
import wheel
ahk = AHK()
# levels
levels = ['level15']
# heroes
hero = ['', '', '']
hero_colour = ['', '', '']
pages = ['', '', '']
heroNUM = ['', '', '']
# for battle
herobattle = []
herobattlefin=[]
# damp
enemywiz = [0, 0, 0, 0, 0, 0]
heroTEMP = []
# img list
picparser = ['/1.png', '/2.png', '/3.png', '/4.png']
def findgame():
    global win
    try:
        win = ahk.win_get(title='Hearthstone')
    except:
        print("Not found game.")
    if win.exist:
        print("найдено")
        return True
    else:
        return False

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
if __name__ == '__main__':
    configread()
    findgame()
    time.sleep(10)