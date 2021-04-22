import cv2
import numpy as np
from scipy import ndimage

background = cv2.imread("images/bg.jpg")
background = cv2.resize(background,(background.shape[1]//10,background.shape[0]//10))
cv2.imshow("background",background)

background = cv2.cvtColor(background , cv2.COLOR_BGR2GRAY)
print(background.shape)

_,mask_orig = cv2.threshold(background , 1, 255 ,cv2.THRESH_BINARY_INV)
x = 30
y = 30
theta = 4
background_temp = ndimage.shift(background , shift = [x , y] )
mask_orig_temp = ndimage.shift(mask_orig , shift = [x,y])

#rotate
background_temp = ndimage.rotate(background_temp, angle = theta , reshape = False)
mask_orig_temp = ndimage.rotate(mask_orig_temp , angle = theta, reshape = False)

_,mask_background = cv2.threshold(background_temp , 1 , 255 , cv2.THRESH_BINARY)

mask = mask_background + mask_orig_temp
cv2.imshow("background", background_temp)
cv2.imshow("mask",mask)

print(np.unique(mask_orig))
print(np.count_nonzero(mask_orig))
print(mask_orig.shape)

cv2.imshow("mask_orig",mask_orig)
cv2.waitKey(0)