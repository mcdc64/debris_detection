import cv2
import numpy as np
import time

def center_of_mass(image): # calculate center of mass (or center of intensity more accurately) in an image
    # Wikipedia gives a nice formula for the center of mass based on the "moments" of the image - implement this
    m_00 = np.sum(image)
    #print(np.shape(image))
    y_summed_image = np.sum(image,axis=0)
    weighted_x_sum = 0
    #print("Y Summed Image has length "+str(len(y_summed_image)))
    x_summed_image = np.sum(image, axis=1)
    weighted_y_sum = 0
    #print("X Summed Image has length "+str(len(x_summed_image)))
    for i in range(0,len(y_summed_image)):
        weighted_x_sum += i*y_summed_image[i]
    for j in range(0,len(x_summed_image)):
        weighted_y_sum += j*x_summed_image[j]
    if(m_00 == 0):
        return np.asarray([-1, -1]) # indicates black image
    return np.asarray([weighted_x_sum/m_00,weighted_y_sum/m_00])

def display_com(image): #displays the center of mass of an image (be sure the image is in grayscale format or it will crash)
    com = center_of_mass(image)
    img_shape = np.shape(image)
    img_scale = int(np.sqrt(img_shape[0]*img_shape[1]))
    #print("Center of Mass: "+str(com))
    keypoint = cv2.KeyPoint(com[0], com[1], size=0.035*img_scale)
    image_with_com = cv2.drawKeypoints(image, [keypoint], np.array([]), (0, 0, 255),
                                        cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return image_with_com

def get_diff_image(img1,img2,stationary,threshold=20,stat_threshold = 100):
    # returns difference of images 1 and 2, with some Gaussian blur added in
    # img1, img2 must have same dimensions and be OpenCV "Image" type
    

    # blur the inputs by an amount proportional to the geometric mean of their x and y dimensions
    gauss_sigma = int(0.015*np.sqrt(np.shape(img1)[0]*np.shape(img1)[1]))
    if (gauss_sigma % 2 == 0):
        gauss_sigma += 1
        
        

    img1_blur = cv2.GaussianBlur(img1,(gauss_sigma,gauss_sigma),0)
    img2_blur = cv2.GaussianBlur(img2, (gauss_sigma, gauss_sigma), 0)

    grey_img1 = cv2.cvtColor(img1_blur,cv2.COLOR_BGR2GRAY)
    grey_img2 = cv2.cvtColor(img2_blur, cv2.COLOR_BGR2GRAY)


    diff_img = cv2.absdiff(grey_img1,grey_img2)
    ret, diff_img = cv2.threshold(diff_img,20,255,cv2.THRESH_BINARY)
    if stationary:
        ret, diff_img = cv2.threshold(grey_img1,stat_threshold,255,cv2.THRESH_BINARY)
    return diff_img

def get_com(img1,img2):
    # returns (x,y) position of the center of Mass of the Difference, in pixels
    diff_img = get_diff_image(img1,img2)
    com = center_of_mass(diff_img)

    return com

