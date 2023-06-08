import RPi.GPIO as GPIO
import time
import numpy as np
import board
import adafruit_bh1750
import adafruit_bno055

def stabilise_adcs(target_attitude, omega, stiffness):
    output_speed = 0;
    forward = True;
    i2c = board.I2C();
    imu = adafruit_bno055.BNO055_I2C(i2c)
    curr_attitude = imu.euler[0] # degrees
    curr_rate = imu.gyro[0] # degrees per second
    # use a PD controller to decide motor current needed, and in which direction
    output_speed = omega*(target_attitude-curr_attitude) - stiffness*curr_rate
    max_speed = omega*180 + 10*stiffness
    output_speed = (output_speed/max_speed)*100 # normalise output speed to duty cycles of motor
    return output_speed

def control_motor(output_speed): # apply control law to motor if needed
    in1 = 24
    in2 = 23
    en = 25
    temp1 = 1

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(en, GPIO.OUT)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    p = GPIO.PWM(en, 1000)
    p.start(25)
    if(output_speed>=0): # forwards
        p.ChangeDutyCycle(output_speed)
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
    if(output_speed<0): # backwards motion required
        p.ChangeDutyCycle(-output_speed)
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
