import cv2
import numpy as np
from scipy import ndimage
import datetime

def x_shift(image, background, mask_orig, minimum=255, rangex=50):
    final_x = 0
    images = []
    masks = [] 
    
    for x in range(-rangex, rangex+1,1):
        #print("x",x)
         #shift
        image_temp = ndimage.shift(image , shift = [x , 0] )
        mask_temp = ndimage.shift(mask_orig , shift = [x,0])
        
        images.append(image_temp)
        masks.append(mask_temp)

        #final mask for calculating difference
    images = np.array(images , np.uint8)
    masks = np.array(masks , np.uint8)
    
    backgrounds = np.bitwise_and(background ,masks)
    
    diffs = cv2.absdiff(backgrounds , images)
    
    diffs1 = np.reshape(diffs , (diffs.shape[0], -1))
    masks1 = np.reshape(masks , (masks.shape[0], -1))

    sizes = np.sum(masks1, axis=1)/255
    res = np.sum(diffs1 , axis =1)/sizes

    index = np.argmin(res)
    
    if res[index] < minimum : 
        minimum = res[index]
        final_x = -rangex+index
        
    print("X done")
    return minimum, images[index] , masks[index], final_x

def y_shift(image, background, mask_orig, minimum=255, rangey=50):

    final_y = 0
    images = []
    masks = []
    
    for y in range(-rangey, rangey+1,1):
        #print("y",y)
         #shift
        image_temp = ndimage.shift(image , shift = [0 , y] )
        mask_temp = ndimage.shift(mask_orig , shift = [0,y])
        
        images.append(image_temp)
        masks.append(mask_temp)
    
    images = np.array(images , np.uint8)
    masks = np.array(masks , np.uint8)
    
    backgrounds = np.bitwise_and(background ,masks)
    
    diffs = cv2.absdiff(backgrounds ,images)
    
    diffs1 = np.reshape(diffs , (diffs.shape[0], -1))
    masks1 = np.reshape(masks , (masks.shape[0], -1))
    
    sizes = np.sum(masks1, axis=1)/255
    res = np.sum(diffs1 , axis =1)/sizes

    index = np.argmin(res)
    
    if res[index] < minimum : 
        minimum = res[index]
        final_y = -rangey+index
        
    print("Y done")
    return minimum, images[index] , masks[index], final_y
        
def theta_rotate(image, background, mask_orig, minimum=255, range_deg = 7):
    final_theta = 0
    images = []
    masks = []
    for theta in range(-range_deg, range_deg+1,1):
        #print("theta",theta)
         #shift
        image_temp = ndimage.rotate(image, angle = theta , reshape = False)
        mask_temp = ndimage.rotate(mask_orig, angle = theta, reshape = False) 
        
        
        images.append(image_temp)
        masks.append(mask_temp)
    
    images = np.array(images , np.uint8)
    masks = np.array(masks , np.uint8)
    
    backgrounds = np.bitwise_and(background ,masks)
    diffs = cv2.absdiff(backgrounds , images)
    
    diffs1 = np.reshape(diffs , (diffs.shape[0], -1))
    masks1 = np.reshape(masks , (masks.shape[0], -1))
    
    sizes = np.sum(masks1, axis=1)/255
    
    res = np.sum(diffs1 , axis =1)/sizes
    
    index = np.argmin(res)
    
    if res[index] < minimum : 
        minimum = res[index]
        final_theta = -range_deg+index
        
    print("theta done")
    return minimum, images[index] , masks[index], final_theta

def find_diff(image, background, rangex=50, rangey=50 , range_deg = 7 ):
    if len(image.shape)==3 :
        image = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
    if len(background.shape)==3 :
        background = cv2.cvtColor(background , cv2.COLOR_BGR2GRAY)
        
    mask_orig = np.full(image.shape , 255 , np.uint8)
    
    MIN = 255
    IMAGE = None
    MASK = None
    shift_rotate = []
    
    
    ################################# case1  #######################################
    #x,y,theta
    print("CASE 1")
    minimum = 255
    
    temp, image1 , mask_orig1 , x = x_shift(image, background, mask_orig, minimum, rangex)
    
    temp, image1 , mask_orig1 , y= y_shift(image1, background, mask_orig1, temp, rangey) 
    
    temp, image1  ,mask_orig1 , theta= theta_rotate(image1, background, mask_orig1, temp, range_deg)
    
    if temp<MIN:
        MIN = temp
        MASK = mask_orig1
        IMAGE = image1
        shift_rotate = [('x',x) ,('y' ,y) ,('r', theta)]
        
    ################################# case2 #######################################
    #y,x,theta
    print("CASE 2")
    minimum = 255
    
    temp, image1  ,mask_orig1 , y = y_shift(image, background, mask_orig, minimum, rangey)
    
    temp, image1 , mask_orig1 , x = x_shift(image1, background, mask_orig1, temp, rangex) 
    
    temp, image1 , mask_orig1 ,theta= theta_rotate(image1, background, mask_orig1, temp, range_deg)
    
    if temp<MIN:
        MIN = temp
        MASK = mask_orig1
        IMAGE = image1
        shift_rotate = [('y',y) ,('x' ,x) ,('r', theta)]
    ################################# case3 #######################################
    #theta,y,x
    print("CASE 3")
    minimum = 255
    
    temp, image1 , mask_orig1 , theta= theta_rotate(image, background, mask_orig, minimum, range_deg)
    
    temp, image1 , mask_orig1 , y= y_shift(image1, background, mask_orig1, temp, rangey) 
    
    temp, image1 , mask_orig1 , x= x_shift(image1, background, mask_orig1, temp, rangex) 
    
    if temp<MIN:
        MIN = temp
        MASK = mask_orig1
        IMAGE = image1
        shift_rotate = [('r', theta) ,('y',y) ,('x' ,x) ]
    
    ################################# case4 #######################################
    #x,theta,y
    print("CASE 4")
    minimum = 255
    temp, image1 , mask_orig1 , x = x_shift(image, background, mask_orig, minimum, rangex)

    temp, image1 , mask_orig1 , theta= theta_rotate(image1, background, mask_orig1, temp, range_deg)
    
    temp, image1 , mask_orig1, y = y_shift(image1, background, mask_orig1, temp, rangey)
    
    if temp<MIN:
        MIN = temp
        MASK = mask_orig1
        IMAGE = image1
        shift_rotate = [('x' ,x) , ('r', theta) ,('y',y)]
    
    ################################# case5 #######################################
    #theta, x, y
    print("CASE 5")
    minimum = 255
    temp, image1 , mask_orig1 ,theta = theta_rotate(image, background, mask_orig, minimum, range_deg)
    
    temp, image1 , mask_orig1 ,x= x_shift(image1, background, mask_orig1, temp, rangex)
    
    temp, image1 , mask_orig1 ,y= y_shift(image1, background, mask_orig1, temp, rangey)
    
    if temp<MIN:
        MIN = temp
        MASK = mask_orig1
        IMAGE = image1
        shift_rotate = [ ('r', theta) ,('x' ,x) ,('y',y)]
    
    ################################# case6 #######################################
    # y,theta,x
    print("CASE 6")
    minimum = 255
    temp, image1 , mask_orig1 ,y = y_shift(image, background, mask_orig, minimum, rangey)
    
    temp, image1 , mask_orig1 ,theta= theta_rotate(image1, background, mask_orig1, temp, range_deg)
    
    temp, image1 , mask_orig1 ,x= x_shift(image1, background, mask_orig1, temp, rangex) 
    
    if temp<MIN:
        MIN = temp
        MASK = mask_orig1
        IMAGE = image1
        shift_rotate = [('y',y), ('r', theta) ,('x' ,x) ]

    ####################################################################################
                
    background_temp = cv2.bitwise_and(background , MASK)
    best_match = cv2.absdiff(background_temp , IMAGE)
    return best_match, shift_rotate

time_temp = datetime.datetime.now()
bg = cv2.imread("background5.jpg")
bg = cv2.resize(bg,(bg.shape[1]//3,bg.shape[0]//3))
img1 = cv2.imread("image5.jpg")
img1 = cv2.resize(img1,(bg.shape[1],bg.shape[0]))
diff,shift_rotate = find_diff(img1 , bg)
print(datetime.datetime.now() - time_temp)

print(shift_rotate)

#cv2.imwrite("diff.jpg" , diff)

_ , diff = cv2.threshold(diff, 15 , 255 , cv2.THRESH_BINARY)
#cv2.imwrite("thresholded.jpg" , diff)

diff = cv2.erode(diff , np.full((3,3),255, np.uint8)  , iterations = 4)
#cv2.imwrite("eroded.jpg" , diff)

diff = cv2.dilate(diff , np.full((7,7),255, np.uint8)  , iterations = 10)
#cv2.imwrite("dilated.jpg" , diff)
dilated = diff.copy()

image_temp = img1.copy()
for i in shift_rotate:
    if i[0]=='x':
        image_temp = ndimage.shift(image_temp , shift = [i[1] , 0,0] )
    elif i[0]=='y':
        image_temp = ndimage.shift(image_temp , shift = [0,i[1],0] )
    else:
        ndimage.rotate(image_temp, angle = i[1] , reshape = False)

background_temp = bg.copy()
background_temp[dilated==255] = image_temp[dilated==255]
#cv2.imwrite("final.jpg",background_temp)

#np.save("new_code_test/diff.npy", diff)
#open("new_code_test/shift_rotate.txt","w").write(str(shift_rotate))
