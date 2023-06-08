import RPi.GPIO as GPIO  # sudo apt-get install python-rpi.gpio

class Driver:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.R_EN = 21
        self.L_EN = 22
        self.RPWM = 23
        self.LPWM = 24
        GPIO.setup(self.R_EN, GPIO.OUT)
        GPIO.setup(self.RPWM, GPIO.OUT)
        GPIO.setup(self.L_EN, GPIO.OUT)
        GPIO.setup(self.LPWM, GPIO.OUT)
        GPIO.output(self.R_EN, True)
        GPIO.output(self.L_EN, True)

    def neutral(self):
        GPIO.output(self.RPWM, False)  # Stop turning right
        GPIO.output(self.LPWM, False)  # stop turning left

    def right(self):
        GPIO.output(self.LPWM, False)  # stop turning left
        GPIO.output(self.RPWM, True)  # start turning right

    def left(self):
        GPIO.output(self.RPWM, False)  # Stop turning right
        GPIO.output(self.LPWM, True)  # start turning left

    def cleanup(self):
        GPIO.cleanup()
