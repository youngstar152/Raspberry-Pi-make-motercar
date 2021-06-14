import wiringpi as pi,time

OUTPUT1 = [6,13,19,26]
OUTPUT2 = [4,17,27,22]
SW_PIN =[24,20,21,12,5]
TIME_SLEEP = 0.002
pi.wiringPiSetupGpio()

for i in range(4):
    pi.pinMode(OUTPUT1[i],pi.OUTPUT)
    pi.pinMode(OUTPUT2[i],pi.OUTPUT)

for i in range(5):
    pi.pinMode(SW_PIN[i],pi.INPUT)
    pi.pullUpDnControl(SW_PIN[i],pi.PUD_UP)

mae_press =[False,False,False,False,False]
ima_press =[False,False,False,False,False]

def check():
    for i in range(5):
        mae_press[i]= ima_press[i]
        ima_press[i]=pi.digitalRead(SW_PIN[i]) ==0

def push_once(i):
   return not mae_press[i] and ima_press[i]

def light1(i,b):
    if b:
        pi.digitalWrite(OUTPUT1[i],pi.HIGH)
    else:
        pi.digitalWrite(OUTPUT1[i],pi.LOW)

def light2(i,b):
    if b:
        pi.digitalWrite(OUTPUT2[i],pi.HIGH)
    else:
        pi.digitalWrite(OUTPUT2[i],pi.LOW)

stop = False
hantai1 = False
hantai2 = False
now1=0
now2=0

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
        if i==n:
            light1(i,True)
        else:
            light1(i,False)

def only_light2(n):
    for i in range(4):
        if i==n:
            light2(i,True)
        else:
            light2(i,False)

def two_light1(n):
    for i in range(4):
        if i==n:
            light1(i,True)
        elif i==(n+1)%4 or i==(n-3)%4:
            light1(i,True)
        else:
            light1(i,False)

def two_light2(n):
    for i in range(4):
        if i==n:
            light2(i,True)
        elif i==(n+1)%4 or i==(n-3)%4:
            light2(i,True)
        else:
            light2(i,False)

mae_time = time.time()
while True:
    check()
    if time.time() - mae_time > 0.002:
        mae_time=time.time()
        if not stop:
            idou1()
            idou2()

    if push_once(0):
        stop = True

    if push_once(1):
        stop = False
        hantai1 = True
        hantai2 = True
    
    if push_once(2):
        stop = False
        hantai1 = False
        hantai2 = False
        
    if push_once(3):
        stop = False
        hantai1 = True
        hantai2 = False
        
    if push_once(4):
        stop = False
        hantai1 = False
        hantai2 = True
    only_light1(now1)
    only_light2(now2)
