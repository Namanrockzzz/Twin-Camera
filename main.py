import cv2
import numpy as np
from scipy import ndimage

def x_shift(image, background, mask_orig, minimum=255, rangex=50):
    final_x = 0
    for x in range(-rangex, rangex+1,1):
        #print("x",x)
         #shift
        image_temp = ndimage.shift(image , shift = [x , 0] )
        mask_orig_temp = ndimage.shift(mask_orig , shift = [x,0])
        
        _,mask_image = cv2.threshold(image_temp , 1 , 255 , cv2.THRESH_BINARY)
        #final mask for calculating difference
        mask = mask_image + mask_orig_temp
        size = np.sum(mask)/255
        background_temp = cv2.bitwise_and(background , mask)
        diff = cv2.absdiff(background_temp , image_temp )

        res = np.sum(diff)/size
        if minimum  > res:
            minimum = res
            final_x = x
    print("X done")
    return minimum, final_x

def y_shift(image, background, mask_orig, minimum=255, rangey=50):
    final_y = 0
    for y in range(-rangey , rangey+1,1):
        #print("y",y)
         #shift
        image_temp = ndimage.shift(image , shift = [0, y])
        mask_orig_temp = ndimage.shift(mask_orig , shift = [0,y])
        
        _,mask_image = cv2.threshold(image_temp , 1 , 255 , cv2.THRESH_BINARY)
        #final mask for calculating difference
        mask = mask_image + mask_orig_temp
        size = np.sum(mask)/255
        background_temp = cv2.bitwise_and(background , mask)
        diff = cv2.absdiff(background_temp , image_temp )
        res = np.sum(diff)/size
        if minimum  > res:
            minimum = res
            final_y = y
    print("Y done")
    return minimum, final_y
    
def theta_rotate(image, background, mask_orig, minimum=255, range_deg = 7):
    final_theta = 0
    for theta in range(-range_deg , range_deg+1, 1):
        #print("theta",theta)
        #rotate
        image_temp = ndimage.rotate(image, angle = theta , reshape = False)
        mask_orig_temp = ndimage.rotate(mask_orig, angle = theta, reshape = False) 
        
        _,mask_image = cv2.threshold(image_temp , 1 , 255 , cv2.THRESH_BINARY)
        mask = mask_image + mask_orig_temp
        size = np.sum(mask)/255
        background_temp = cv2.bitwise_and(background , mask)
        diff = cv2.absdiff(background_temp , image_temp )
        res = np.sum(diff)/size
        if minimum  > res:
            minimum = res
            final_theta = theta
    print("Theta done")
    return minimum, final_theta

def find_diff(image, background, rangex=50, rangey=50 , range_deg = 7 ):
    if len(image.shape)==3 :
        image = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
    if len(background.shape)==3 :
        background = cv2.cvtColor(background , cv2.COLOR_BGR2GRAY)
        
    _,mask_orig = cv2.threshold(image , 1, 255 ,cv2.THRESH_BINARY_INV)
    
    MIN = 255
    X = 0
    Y = 0
    THETA = 0
    
    
    ################################# case1  #######################################
    #x,y,theta
    print("CASE 1")
    minimum = 255
    
    temp, final_x = x_shift(image, background, mask_orig, minimum, rangex)
    image1 = ndimage.shift(image , shift = [final_x , 0] )
    mask_orig1 = ndimage.shift(mask_orig , shift = [final_x,0])
    
    temp, final_y = y_shift(image1, background, mask_orig1, temp, rangey) 
    image1 = ndimage.shift(image1 , shift = [0 , final_y] )
    mask_orig1 = ndimage.shift(mask_orig1 , shift = [0,final_y])
    
    temp, final_theta = theta_rotate(image1, background, mask_orig1, temp, range_deg)
    
    if temp<MIN:
        MIN = temp
        X = final_x
        Y = final_y
        THETA = final_theta
        
    ################################# case2 #######################################
    #y,x,theta
    print("CASE 2")
    minimum = 255
    
    temp, final_y = y_shift(image, background, mask_orig, minimum, rangey)
    image1 = ndimage.shift(image , shift = [0 , final_y] )
    mask_orig1 = ndimage.shift(mask_orig , shift = [0,final_y])
    
    temp, final_x = x_shift(image1, background, mask_orig1, temp, rangex) 
    image1 = ndimage.shift(image1 , shift = [final_x , 0] )
    mask_orig1 = ndimage.shift(mask_orig1 , shift = [final_x,0])
    
    temp, final_theta = theta_rotate(image1, background, mask_orig1, temp, range_deg)
    
    if temp<MIN:
        MIN = temp
        X = final_x
        Y = final_y
        THETA = final_theta
    
    ################################# case3 #######################################
    #theta,y,x
    print("CASE 3")
    minimum = 255
    
    temp, final_theta = theta_rotate(image, background, mask_orig, minimum, range_deg)
    image1 = ndimage.rotate(image, angle = final_theta , reshape = False)
    mask_orig1 = ndimage.rotate(mask_orig , angle = final_theta, reshape = False)
    
    temp, final_y = y_shift(image1, background, mask_orig1, temp, rangey) 
    image1 = ndimage.shift(image1 , shift = [0 , final_y] )
    mask_orig1 = ndimage.shift(mask_orig1 , shift = [0,final_y])
    
    temp, final_x = x_shift(image1, background, mask_orig1, temp, rangex) 
    
    if temp<MIN:
        MIN = temp
        X = final_x
        Y = final_y
        THETA = final_theta
    
    ################################# case4 #######################################
    #x,theta,y
    print("CASE 4")
    minimum = 255
    temp, final_x = x_shift(image, background, mask_orig, minimum, rangex)
    image1 = ndimage.shift(image , shift = [final_x , 0] )
    mask_orig1 = ndimage.shift(mask_orig , shift = [final_x, 0])
    
    temp, final_theta = theta_rotate(image1, background, mask_orig1, temp, range_deg)
    image1 = ndimage.rotate(image1, angle = final_theta , reshape = False)
    mask_orig1 = ndimage.rotate(mask_orig1 , angle = final_theta, reshape = False)
    
    temp, final_y = y_shift(image1, background, mask_orig1, temp, rangey)
    
    if temp<MIN:
        MIN = temp
        X = final_x
        Y = final_y
        THETA = final_theta
    
    ################################# case5 #######################################
    #theta, x, y
    print("CASE 5")
    minimum = 255
    temp, final_theta = theta_rotate(image, background, mask_orig, minimum, range_deg)
    image1 = ndimage.rotate(image, angle = final_theta , reshape = False)
    mask_orig1 = ndimage.rotate(mask_orig , angle = final_theta, reshape = False)
    
    temp, final_x = x_shift(image1, background, mask_orig1, temp, rangex)
    image1 = ndimage.shift(image1 , shift = [final_x , 0] )
    mask_orig1 = ndimage.shift(mask_orig1 , shift = [final_x, 0])
    
    temp, final_y = y_shift(image1, background, mask_orig1, temp, rangey)
    
    if temp<MIN:
        MIN = temp
        X = final_x
        Y = final_y
        THETA = final_theta
    
    ################################# case6 #######################################
    # y,theta,x
    print("CASE 6")
    minimum = 255
    temp, final_y = y_shift(image, background, mask_orig, minimum, rangey)
    image1 = ndimage.shift(image , shift = [0 , final_y] )
    mask_orig1 = ndimage.shift(mask_orig , shift = [0,final_y])
    
    temp, final_theta = theta_rotate(image1, background, mask_orig1, temp, range_deg)
    image1 = ndimage.rotate(image1, angle = final_theta , reshape = False)
    mask_orig1 = ndimage.rotate(mask_orig1 , angle = final_theta, reshape = False)
    
    temp, final_x = x_shift(image1, background, mask_orig1, temp, rangex) 
    
    if temp<MIN:
        MIN = temp
        X = final_x
        Y = final_y
        THETA = final_theta
        
    ####################################################################################
    
    final_x = X
    final_y = Y
    final_theta = THETA
     
    #shift
    image_temp = ndimage.shift(image , shift = [final_x , final_y] )
    mask_orig_temp = ndimage.shift(mask_orig , shift = [final_x,final_y])
                
    #rotate
    image_temp = ndimage.rotate(image_temp, angle = final_theta , reshape = False)
    mask_orig_temp = ndimage.rotate(mask_orig_temp , angle = final_theta, reshape = False)
    
    _,mask_image = cv2.threshold(image_temp , 1 , 255 , cv2.THRESH_BINARY)
                
    #final mask for calculating difference
    mask = mask_image + mask_orig_temp
                
    #size of the significant area
    size = np.sum(mask)/255      
    background_temp = cv2.bitwise_and(background , mask)
    diff = cv2.absdiff(background_temp , image_temp)
    best_match = diff
    shift_rotate = (final_x,final_y,final_theta)
    return best_match, shift_rotate

bg = cv2.imread("images/bg.jpg")
bg = cv2.resize(bg,(bg.shape[1]//3,bg.shape[0]//3))
img1 = cv2.imread("images/img1.jpg")
img1 = cv2.resize(img1,(bg.shape[1],bg.shape[0]))
diff,shift_rotate = find_diff(img1 , bg)

_ , diff = cv2.threshold(diff, 15 , 255 , cv2.THRESH_BINARY)
cv2.imwrite("test/thresholded.jpg" , diff)

diff = cv2.erode(diff , np.full((3,3),255, np.uint8)  , iterations = 4)
cv2.imwrite("test/eroded.jpg" , diff)

diff = cv2.dilate(diff , np.full((7,7),255, np.uint8)  , iterations = 10)
cv2.imwrite("test/dilated.jpg" , diff)
dilated = diff.copy()

#shift
image_temp = ndimage.shift(img1 , shift = [shift_rotate[0] , shift_rotate[1],0] )
#rotate
image_temp = ndimage.rotate(image_temp, angle = shift_rotate[2] , reshape = False)

background_temp = bg.copy()

background_temp[dilated==255] = image_temp[dilated==255]

cv2.imwrite("test/final.jpg",background_temp)