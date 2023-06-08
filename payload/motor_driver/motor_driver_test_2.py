import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
p=GPIO.PWM(16,100)
while True:
    p.start(20) #Motor will run at slow speed
    GPIO.output(21,True)
    GPIO.output(20,False)
    GPIO.output(16,True)
    time.sleep(3)
    p.ChangeDutyCycle(100) #Motor will run at High speed
    GPIO.output(21,True)
    GPIO.output(20,False)
    GPIO.output(16,True)
    time.sleep(3)
    GPIO.output(16,False)
    p.stop()
