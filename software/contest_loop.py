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

ret, cam_bottom_img = cam_bottom.read()
ret, cam_top_img = cam_top.read()

### Camera parameters
# /!\ Please update with experimentale values /!\
horiz_angle_of_view = 62 #[deg] angle of view in the horizontal (longer side) direction
vert_angle_of_view = 48#[deg] angle of view in the vertical (shorter side) direction
img_shape = np.shape(cam_bottom_img)
d_cameras = 0.14 #[m] distance between the cameras
cam_param = np.array([horiz_angle_of_view*np.pi/180,vert_angle_of_view*np.pi/180,img_shape[0],img_shape[1],d_cameras])

debris_buffer = []
frame_time = time.time()
while True:
    # Getting the time measurement at the begining of the frame
    last_frame_time = frame_time # time at start of last frame
    # start_frame_time = time.time() # time at start of this frame
    frame_time = time.time() # time at start of this frame
    delta_t = frame_time-last_frame_time # in seconds /!\ it's always 0 because 

    # Getting the position of the debris in the 2 cameras points of view
    old_cam_bottom_img = cam_bottom_img
    old_cam_top_img = cam_top_img
    ret, cam_bottom_img = cam_bottom.read()
    ret,cam_top_img = cam_top.read()


    cam_bottom_diff = frame_difference.get_diff_image(cam_bottom_img,old_cam_bottom_img)
    cam_top_diff = frame_difference.get_diff_image(cam_top_img,old_cam_top_img)
    cam_bottom_com = frame_difference.center_of_mass(cam_bottom_diff)
    cam_top_com = frame_difference.center_of_mass(cam_top_diff)
    
    cv2.imshow('Imagetest',cam_bottom_diff)
    cv2.imshow('Imagetest2',cam_top_diff)
    k = cv2.waitKey(1)
    if(cam_bottom_com[0] ==-1 or cam_top_com[0] == -1): # this means there is no debris in the frame
        
        if(len(debris_buffer)>0): # there were a debris but it's not there anymore
            # output the distance and velocity data for the debris
            debris = debris_buffer[0]
            # compute the minimal distance between the debris and the satellite
            debris.distance = debris.distance_min()
            print("Debris Distance: {} m".format(debris.distance))
            print("Debris Velocity: {} m s^-1".format(np.linalg.norm(debris.velocity)))
            
            # Recording the debris 
            debris_list.append(debris)
            
        # clear the debris buffer
        debris_buffer = []
        continue
    
    ### otherwise, calculate debris distance
    # Computation of the attitude of the satellite
    rot_matrix = np.asarray([[1, 0 , 0],[0,1,0],[0,0,1]])
    # Calculate the position of the debris
    pos = position_calculation(cam_bottom_com,cam_top_com,rot_matrix, cam_param)
    
    # Record the results
    if(len(debris_buffer) == 0):
        # if this is the first appearance of the debris, add it to the buffer and continue to next loop
        debris_buffer.append(Debris(pos,[0,0,0],frame_time,cam_bottom_com,cam_top_com))
        continue

    debris = debris_buffer[0]
    old_cam_bottom_com = cam_bottom_com
    old_cam_top_com = cam_top_com
    debris.positionlist.append(pos)
    debris.timelist.append(frame_time)
    debris.velocity = debris.velocity_calc()
    '''
    #check if ADCS action is needed
    target_attitude = 0 # change later
    omega = 1
    stiffness = 10
    adcs_tol = 1 # no need to take action if the output_speed is smaller than this
    output_speed = spin.stabilise_adcs(target_attitude,omega,stiffness)
    if(np.abs(output_speed)>adcs_tol):
        spin.control_motor()
    '''
    # ...and back to the top of the loop
