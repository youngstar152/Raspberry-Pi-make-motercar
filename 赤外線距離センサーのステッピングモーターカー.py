import smbus
import time
import mcp3424

import wiringpi as pi, time

OUTPUT1 = [6, 13, 19, 26]
OUTPUT2 = [4, 17, 27, 22]
SW_PIN = [24, 20, 21, 12, 5]
TIME_SLEEP = 0.002
pi.wiringPiSetupGpio()

for i in range(4):
    pi.pinMode(OUTPUT1[i], pi.OUTPUT)
    pi.pinMode(OUTPUT2[i], pi.OUTPUT)

for i in range(5):
    pi.pinMode(SW_PIN[i], pi.INPUT)
    pi.pullUpDnControl(SW_PIN[i], pi.PUD_UP)

mae_press = [False, False, False, False, False]
ima_press = [False, False, False, False, False]


def check():
    for i in range(5):
        mae_press[i] = ima_press[i]
        ima_press[i] = pi.digitalRead(SW_PIN[i]) == 0


def push_once(i):
    return not mae_press[i] and ima_press[i]


def light1(i, b):
    if b:
        pi.digitalWrite(OUTPUT1[i], pi.HIGH)
    else:
        pi.digitalWrite(OUTPUT1[i], pi.LOW)


def light2(i, b):
    if b:
        pi.digitalWrite(OUTPUT2[i], pi.HIGH)
    else:
        pi.digitalWrite(OUTPUT2[i], pi.LOW)


stop = False
hantai1 = False
hantai2 = False
now1 = 0
now2 = 0


def idou1():
    global now1
    if hantai1:
        now1 -= 1
        if now1 < 0:
            now1 = 3
    else:
        now1 += 1
        if now1 > 3:
            now1 = 0


def idou2():
    global now2
    if hantai2:
        now2 -= 1
        if now2 < 0:
            now2 = 3
    else:
        now2 += 1
        if now2 > 3:
            now2 = 0


def only_light1(n):
    for i in range(4):
        if i == n:
            light1(i, True)
        else:
            light1(i, False)


def only_light2(n):
    for i in range(4):
        if i == n:
            light2(i, True)
        else:
            light2(i, False)


def two_light1(n):
    for i in range(4):
        if i == n:
            light1(i, True)
        elif i == (n + 1) % 4 or i == (n - 3) % 4:
            light1(i, True)
        else:
            light1(i, False)


def two_light2(n):
    for i in range(4):
        if i == n:
            light2(i, True)
        elif i == (n + 1) % 4 or i == (n - 3) % 4:
            light2(i, True)
        else:
            light2(i, False)


i2c = smbus.SMBus(1)
addr = 0x68

configs = []
configs.append([mcp3424.cfg_read | mcp3424.cfg_ch1 | mcp3424.cfg_once | mcp3424.cfg_12bit | mcp3424.cfg_PGAx1])
configs.append([mcp3424.cfg_read | mcp3424.cfg_ch2 | mcp3424.cfg_once | mcp3424.cfg_12bit | mcp3424.cfg_PGAx1])
configs.append([mcp3424.cfg_read | mcp3424.cfg_ch3 | mcp3424.cfg_once | mcp3424.cfg_12bit | mcp3424.cfg_PGAx1])

datas = [None, None, None]

n = len(configs)

vs = [0, 0, 0]

# check[i] = (datas[i][2] >> 7) == 0

ima_kakunin_siteru_yatsu = 0
kakunin_siteru = False

magatteru = time.time()

while True:

    if kakunin_siteru:
        datas[ima_kakunin_siteru_yatsu] = i2c.read_i2c_block_data(addr, configs[ima_kakunin_siteru_yatsu][0], 3)
        if datas[ima_kakunin_siteru_yatsu][2] >> 7 == 0:
            vs[ima_kakunin_siteru_yatsu] = mcp3424.to_volt(datas[ima_kakunin_siteru_yatsu], 12)
            ima_kakunin_siteru_yatsu += 1
            if ima_kakunin_siteru_yatsu > 2:
                ima_kakunin_siteru_yatsu = 0
            kakunin_siteru = False

    else:
        i2c.write_i2c_block_data(addr, 0, configs[ima_kakunin_siteru_yatsu])
        kakunin_siteru = True

    idou1()
    idou2()
    if vs[0] <= 1.9 and vs[1] <= 1.9 and vs[2] <= 1.65:
        hantai1 = False
        hantai2 = False

    if vs[2] >= 1.5:
        magatteru = time.time()

    if vs[0] >= 1.9:
        hantai1 = True
        if vs[1] <= 1.9:
            hantai2 = False
        if vs[1] >= 1.9:
            hantai2 = True

    if vs[1] >= 1.9:
        hantai2 = True
        if vs[0] <= 1.9:
            hantai1 = False
        if vs[0] >= 1.9:
            hantai1 = True

    if vs[2] >= 1.65:
        if vs[0] <= 1.9 and vs[0] > vs[1]:
            hantai1 = True
            hantai2 = False
        if vs[1] <= 1.9 and vs[0] < vs[1]:
            hantai1 = False
            hantai2 = True
        if vs[0] >= 1.9 and vs[1] >= 1.9:
            hantai1 = True
            hantai2 = True

    only_light1(now1)

    only_light2(now2)

    if time.time()-magatteru>0.1:
        time.sleep(0.002)
    else:
        time.sleep(0.004)
