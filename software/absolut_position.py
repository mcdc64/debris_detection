import numpy as np
import math as m 

def debris_abs_cart_pos (rot_mat_sat, debris_horiz_angle, debris_vert_angle, d_debris_cam_bottom):
    """Transpose the positon of the debris in the bottom camera referentiel to
    the absolute position of the debris in the earth referentiel

    Args:
        rot_mat_sat (np.array(3,3)): rotation matrix to go from the earth referentiel to the satellite one
        debris_horiz_angle (float): [rad] angle between the centre of the picture and the debris in the horizontal plan from the point of view of the bottom camera
        debris_vert_angle (float): [rad] angle between the centre of the picture and the debris in the vertical plan from the point of view of the bottom camera
        d_debris_cam_bottom (float): [m] distance between the debris and the bottom camera 
            
    Returns:
        np.array(3): position vector of the debris in the earth referentiel
    """
    z_debris_sat = d_debris_cam_bottom*np.sin(debris_vert_angle)
    d_horiz_debris_cam_bottom = d_debris_cam_bottom*np.cos(debris_vert_angle)
    x_debris_sat = d_horiz_debris_cam_bottom*np.cos(debris_horiz_angle)
    y_debris_sat = d_horiz_debris_cam_bottom*np.sin(debris_horiz_angle)
    debris_sat_pos = np.array([x_debris_sat,y_debris_sat,z_debris_sat])
    debris_abs_pos = np.matmul(np.invert(rot_mat_sat),debris_sat_pos)
    return(debris_abs_pos)

def position_calculation(cam_bottom_com, cam_top_com, rot_matrix, cam_param):
    """Compute the position of the debris in the earth referential
    given the position in the pictures

    Args:
        cam_bottom_com (np.array(2)): [pix,pix] position of the debris in the picture of the bottom camera from the top left corner
        cam_top_com (np.array(2)): [pix,pix] position of the debris in the picture of the top camera from the top left corner
        rot_matrix (np.array(3,3)): rotation matrix to go from the earth referentiel to the satellite one
        cam_param (np.array(5)): Parameter of the cameras :
            - [rad] angle of view in the horizontal (longer side) direction
            - [rad] angle of view in the vertical (shorter side) direction
            - [pix] numbre of pixels in the long side
            - [pix] numbre of pixels in the short side
            - [m] distance between the two cameras
            
    Returns:
        np.array(3): position vector of the debris in the earth referentiel
    """
    debris_horiz_angle = (cam_bottom_com[0]-cam_param[2])*cam_param[0]/cam_param[2]
    debris_vert_angle = (cam_bottom_com[1]-cam_param[3])*cam_param[1]/cam_param[3]
    theta_cam_bottom = debris_vert_angle
    theta_cam_top = (cam_top_com[1]-cam_param[3])*cam_param[1]/cam_param[3]
    d_debris_cam_bottom = parallax(cam_param[4], theta_cam_top, theta_cam_bottom)
    return(debris_abs_cart_pos (rot_matrix, debris_horiz_angle, debris_vert_angle, d_debris_cam_bottom))


def parallax(d_cameras, theta_cam_top, theta_cam_bottom):
    """This function compute the distance between the bottom camera and the debris based and its angular position relatif to the horizon in the point of view of the two onboard cameras.

    Args:
        d_cameras (float): distance between the two cameras
        theta_cam_top (float): angle between the debris and the horizon view from the top camera in radians
        theta_cam_bottom (float): angle between the debris and the horizon view from the bottom camera in radians

    Returns:
        float: distance between the bottom camera and the debris in meters
    """
    x_debris = (d_cameras)/(np.tan(theta_cam_bottom)-np.tan(theta_cam_top))
    z_debris = x_debris*np.tan(theta_cam_bottom)
    d_debris_cam_bottom = np.sqrt(x_debris**2+z_debris**2)
    return (d_debris_cam_bottom)

def test_parallax_simu():
    """This function is there to verify that the function 'parallax' is working as expected based on simulation in a CAD model."""
    d_cameras = 0.28        # [m] distance between the two cameras
    theta_cam_top = 10.1330236*m.pi/180     # [rad] angle between the debris and the horizon view from the top camera
    theta_cam_bottom = 4.8347494*m.pi/180 # [rad] angle between the debris and the horizon view from the bottom camera
    d_debris_cam_bottom = parallax(d_cameras, theta_cam_top, theta_cam_bottom)
    CAD_value = 2.98495528 # [m] distance between the debris and the bottom camera 
    print(f'The expected value (computed with a CAD model) is {CAD_value} m.\n')
    print(f'The computed value is {d_debris_cam_bottom} m.\n')
    print(f'That gives an error of {abs(d_debris_cam_bottom-CAD_value)*1000} mm and a relative error of {abs(d_debris_cam_bottom-CAD_value)*100/CAD_value}%\n')
    