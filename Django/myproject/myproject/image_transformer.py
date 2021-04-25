from .util import *
import numpy as np
import cv2

class ImageTransformer(object):
    def __init__(self, image):
        print(type(image))
        self.image = image
        self.height = self.image.size[1]
        self.width = self.image.size[0]

    def rotate_along_axis(self, theta=0, phi=0, gama=0, dx=0, dy=0, dz=0):
        rtheta,rphi,rgama = get_rad(theta,phi,gama)
        d = np.sqrt(self.height**2+self.width**2)
        self.focal = d/(2*np.sin(rgama) if np.sin(rgama)!=0 else 1)
        dz = self.focal
        mat = self.get_M(rtheta,rphi,rgama,dx,dy,dz)
        self.image=np.array(self.image)
        # print(type(self.image))
        return cv2.warpPerspective(self.image.copy(), mat, (self.width, self.height))

    def get_M(self, theta, phi, gama, dx, dy, dz):
        w = self.width
        h = self.height
        f = self.focal

        A1 = np.array([ [1,0,-w/2],
                        [0,1,-h/2],
                        [0,0,1],
                        [0,0,1]])

        RX = np.array([[1,0,0,0],
                        [0,np.cos(theta),np.sin(theta),0],
                        [0,np.sin(theta),np.cos(theta),0],
                        [0,0,0,1]])

        RY = np.array([[np.cos(phi),0,np.sin(phi),0],
                        [0,1,0,0],
                        [np.sin(phi),0,np.cos(phi),0],
                        [0,0,0,1]])

        RZ = np.array([[np.cos(gama),np.sin(gama),0,0],
                        [np.sin(gama),np.cos(gama),0,0],
                        [0,0,1,0],
                        [0,0,0,1]])

        R = np.dot(np.dot(RX,RY),RZ)
        
        T = np.array([[1,0,0,dx],
                      [0,1,0,dy],
                      [0,0,1,dz],
                      [0,0,0,1]])
                    
        A2 = np.array([[f,0,w/2,0],
                        [0,f,h/2,0],
                        [0,0,1,0]])

        return np.dot(A2, np.dot(T, np.dot(R,A1)))
        