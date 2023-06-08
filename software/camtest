import time
import board
import adafruit_bno055
import adafruit_bh1750
import RPi.GPIO as GPIO
import cv2
import frame_difference
import spin
import numpy as np
from debris_class import Debris
from absolut_position import position_calculation

# Initiate debris records
debris_list = []

# at beginning of loop, define cameras and images to be differenced
cam_bottom = cv2.VideoCapture(0)
cam_top = cv2.VideoCapture(1)
