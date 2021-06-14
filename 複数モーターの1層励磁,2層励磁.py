import wiringpi as pi,time

OUTPUT1 = [6,13,19,26]
OUTPUT2 = [22,27,17,4]
SW_PIN =[23,24]
TIME_SLEEP = 0.002
pi.wiringPiSetupGpio()

for i in range(4):
    pi.pinMode(OUTPUT1[i],pi.OUTPUT)
    pi.pinMode(OUTPUT2[i],pi.OUTPUT)

for i in range(2):
    pi.pinMode(SW_PIN[i],pi.INPUT)

mae_press =[False,False]
ima_press =[False,False]

def check():
    for i in range(2):
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
hantai = False
now=0

def idou():
    global now
    if hantai:
        now -= 1
        if now < 0:
            now = 3
    else:
        now += 1
        if now > 3:
            now = 0

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
            idou()    

    if push_once(0):
        stop=not stop

    if push_once(1):
        hantai= not hantai

    only_light1(now)
    only_light2(now)