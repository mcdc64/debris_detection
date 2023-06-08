import RPi.GPIO as GPIO  # sudo apt-get install python-rpi.gpio


GPIO.setmode(GPIO.BOARD)
R_EN = 21
L_EN = 22
RPWM = 23
LPWM = 24
GPIO.setup(R_EN, GPIO.OUT)
GPIO.setup(RPWM, GPIO.OUT)
GPIO.setup(L_EN, GPIO.OUT)
GPIO.setup(LPWM, GPIO.OUT)
GPIO.output(R_EN, True)
GPIO.output(L_EN, True)

def neutral():
        GPIO.output(RPWM, False)  # Stop turning right
        GPIO.output(LPWM, False)  # stop turning left

def right():
        GPIO.output(LPWM, False)  # stop turning left
        GPIO.output(RPWM, True)  # start turning right

def left():
        GPIO.output(RPWM, False)  # Stop turning right
        GPIO.output(LPWM, True)  # start turning left

def cleanup():
        GPIO.cleanup()
       
        
right()

