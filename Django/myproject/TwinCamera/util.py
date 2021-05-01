from math import pi
import cv2

def get_rad(theta, phi, gama):
    return (deg_to_rad(theta), deg_to_rad(phi), deg_to_rad(gama))

def get_deg(rtheta, rphi, rgama):
    return (rad_to_deg(rtheta), rad_to_deg(rphi), rad_to_deg(rgama))

def deg_to_rad(deg):
    return deg*pi/180.0

def rad_to_deg(rad):
    return deg*180/pi