import wiringpi as pi, time

LED1_PIN = 5
LED2_PIN = 13
LED3_PIN = 26
LED4_PIN = 20
SW1_PIN = 4
SW2_PIN = 27
SW1_flag = 0

def of(sw1):
    global SW1_flag
    SW1_flsg = 1

def on(sw1):
    global SW1_flag
    SW1_flsg = 0
    
pi.wiringPiSetupGpio()
pi.pinMode(LED1_PIN,pi.OUTPUT)
pi.pinMode(LED2_PIN,pi.OUTPUT)
pi.pinMode(LED3_PIN,pi.OUTPUT)
pi.pinMode(SW1_PIN,pi.INPUT)
pi.pinMode(SW2_PIN,pi.INPUT)
pi.pullUpDnControl(SW1_PIN,pi.PUD_UP)
pi.pullUpDnControl(SW2_PIN,pi.PUD_UP)

a = 1
while True:
   pi.digitalWrite(LED1_PIN,pi.HIGH)
   time.sleep(1)  
   pi.digitalWrite(LED1_PIN,pi.LOW)
   time.sleep(1)

   pi.digitalWrite(LED2_PIN,pi.HIGH)
   time.sleep(1)
   pi.digitalWrite(LED2_PIN,pi.LOW)
   time.sleep(1)

   pi.digitalWrite(LED3_PIN,pi.HIGH)
   time.sleep(1)
   pi.digitalWrite(LED3_PIN,pi.LOW)
   time.sleep(1)
   
   pi.digitalWrite(LED4_PIN,pi.HIGH)
   time.sleep(1)
   pi.digitalWrite(LED4_PIN,pi.LOW)
   time.sleep(1)
   
