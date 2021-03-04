import cv2
import numpy as np
from PIL import Image, ImageChops, ImageOps
import datetime

def x_shift(image, background, mask_orig, minimum=255, x_min=-50, x_max=50):
    
    final_x = 0
    images = []
    masks = [] 
    width, height = image.size
    
    for x in range(x_min, x_max+1,1):
        #print("x",x)
        #shift
        if x>0:
            image_temp = ImageChops.offset(image, x, 0)
            image_temp.paste(0, (0, 0, x, height))
            mask_temp = ImageChops.offset(mask_orig, x, 0)
            mask_temp.paste(0, (0, 0, x, height))
        elif x<0:
            image_temp = ImageChops.offset(image, x, 0)
            image_temp.paste(0, (width+x, 0, width, height))
            mask_temp = ImageChops.offset(mask_orig, x, 0)
            mask_temp.paste(0, (width+x, 0, width, height))
        else:
            image_temp = image.copy()
            mask_temp = mask_orig.copy()
        
        images.append(np.array(image_temp))
        masks.append(np.array(mask_temp))

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
        final_x = x_min+index
        
    print("X done")
    return minimum, images[index] , masks[index], final_x

def y_shift(image, background, mask_orig, minimum=255, y_min=-50, y_max=50):

    final_y = 0
    images = []
    masks = []
    width, height = image.size
    
    for y in range(y_min, y_max+1,1):
        #print("y",y)
        #shift
        if y>0:
            image_temp = ImageChops.offset(image, 0, y)
            image_temp.paste(0, (0, 0, width, y))
            mask_temp = ImageChops.offset(mask_orig, 0, y)
            mask_temp.paste(0, (0, 0, width, y))
        elif y<0:
            image_temp = ImageChops.offset(image, 0, y)
            image_temp.paste(0, (0, height+y, width, height))
            mask_temp = ImageChops.offset(mask_orig, 0, y)
            mask_temp.paste(0, (0, height+y, width, height))
        else:
            image_temp = image.copy()
            mask_temp = mask_orig.copy()
            
            
        images.append(np.array(image_temp))
        masks.append(np.array(mask_temp))
    
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
        final_y = y_min+index
        
    print("Y done")
    return minimum, images[index] , masks[index], final_y
        
def theta_rotate(image, background, mask_orig, minimum=255, deg_min = -7, deg_max=7):
    final_theta = 0
    images = []
    masks = []
    for theta in range(deg_min, deg_max+1,1):
        #print("theta",theta)
         #shift
        image_temp = image.rotate(angle = theta)
        mask_temp = mask_orig.rotate(angle = theta) 
        
        
        images.append(np.array(image_temp))
        masks.append(np.array(mask_temp))
    
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
        final_theta = deg_min+index
        
    print("theta done")
    return minimum, images[index] , masks[index], final_theta


def find_diff(image, background):
    if image.mode=="L":
        pass
    else:
        image = ImageOps.grayscale(image)
        background = ImageOps.grayscale(background)
    
        
    mask_orig = Image.fromarray(np.full((image.size[1],image.size[0]) , 255 , np.uint8))
    
    MIN = 255
    IMAGE = None
    MASK = None
    shift_rotate = []
    
    
    ################################# case1  #######################################
    #x,y,theta
    print("CASE 1")
    minimum = 255
    
    temp, image1 , mask_orig1 , x = x_shift(image, background, mask_orig, minimum)
    image_ = image1
    temp, image1 , mask_orig1 , y= y_shift(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp) 
    
    temp, image1  ,mask_orig1 , theta= theta_rotate(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp)
    print("Case1: ",end=" ")
    print(x,y,theta)
    if temp<MIN:
        MIN = temp
        MASK = mask_orig1
        IMAGE = image1
        temp_x = x
        temp_y = y
        temp_theta = theta
        shift_rotate = [('x',x) ,('y' ,y) ,('r', theta)]
        
    ################################# case2 #######################################
    #y,x,theta
    print("CASE 2")
    minimum = 255
    
    temp, image1  ,mask_orig1 , y = y_shift(image, background, mask_orig, minimum, temp_y-15, temp_y+15)
    
    temp, image1 , mask_orig1 , x = x_shift(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, temp_x-15, temp_x+15) 
    
    temp, image1 , mask_orig1 ,theta= theta_rotate(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp)
    print("Case2: ",end=" ")
    print(x,y,theta)
    if temp<MIN:
        MIN = temp
        MASK = mask_orig1
        IMAGE = image1
        temp_x = x
        temp_y = y
        temp_theta = theta
        shift_rotate = [('y',y) ,('x' ,x) ,('r', theta)]
    ################################# case3 #######################################
    #theta,y,x
    print("CASE 3")
    minimum = 255
    
    temp, image1 , mask_orig1 , theta= theta_rotate(image, background, mask_orig, minimum)
    
    temp, image1 , mask_orig1 , y= y_shift(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, temp_y-15, temp_y+15) 
    
    temp, image1 , mask_orig1 , x= x_shift(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, temp_x-15, temp_x+15)
    print("Case3: ",end=" ")
    print(x,y,theta)
    if temp<MIN:
        MIN = temp
        MASK = mask_orig1
        IMAGE = image1
        temp_x = x
        temp_y = y
        temp_theta = theta
        shift_rotate = [('r', theta) ,('y',y) ,('x' ,x) ]
    
    ################################# case4 #######################################
    #x,theta,y
    print("CASE 4")
    minimum = 255
    temp, image1 , mask_orig1 , x = x_shift(image, background, mask_orig, minimum, temp_x-15, temp_x+15)

    temp, image1 , mask_orig1 , theta= theta_rotate(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp)
    
    temp, image1 , mask_orig1, y = y_shift(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, temp_y-15, temp_y+15)
    print("Case4: ",end=" ")
    print(x,y,theta)
    if temp<MIN:
        MIN = temp
        MASK = mask_orig1
        IMAGE = image1
        temp_x = x
        temp_y = y
        temp_theta = theta
        shift_rotate = [('x' ,x) , ('r', theta) ,('y',y)]
    
    ################################# case5 #######################################
    #theta, x, y
    print("CASE 5")
    minimum = 255
    temp, image1 , mask_orig1 ,theta = theta_rotate(image, background, mask_orig, minimum)
    
    temp, image1 , mask_orig1 ,x= x_shift(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, temp_x-15, temp_x+15)
    
    temp, image1 , mask_orig1 ,y= y_shift(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, temp_y-15, temp_y+15)
    print("Case5: ",end=" ")
    print(x,y,theta)
    if temp<MIN:
        MIN = temp
        MASK = mask_orig1
        IMAGE = image1
        temp_x = x
        temp_y = y
        temp_theta = theta
        shift_rotate = [ ('r', theta) ,('x' ,x) ,('y',y)]
    
    ################################# case6 #######################################
    # y,theta,x
    print("CASE 6")
    minimum = 255
    temp, image1 , mask_orig1 ,y = y_shift(image, background, mask_orig, minimum, temp_y-15, temp_y+15)
    
    temp, image1 , mask_orig1 ,theta= theta_rotate(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp)
    
    temp, image1 , mask_orig1 ,x= x_shift(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, temp_x-15, temp_x+15) 
    print("Case6: ",end=" ")
    print(x,y,theta)
    if temp<MIN:
        MIN = temp
        MASK = mask_orig1
        IMAGE = image1
        temp_x = x
        temp_y = y
        temp_theta = theta
        shift_rotate = [('y',y), ('r', theta) ,('x' ,x) ]

    ####################################################################################
                
    background_temp = np.bitwise_and(background , MASK)
    best_match = cv2.absdiff(background_temp , IMAGE)
    return best_match, shift_rotate


# import datetime
bg_original = Image.open("images/bg2.jpg")
img1_original = Image.open("images/img2.jpg")
scale = 7
# time_temp = datetime.datetime.now()
bg = bg_original.copy()
bg = bg.resize((bg.size[0]//scale, bg.size[1]//scale))
img1 = img1_original.copy()
img1 = img1.resize((bg.size[0],bg.size[1]))
diff,shift_rotate = find_diff(img1 , bg)
#diff , image_temp = find_diff(img1 , bg )
# print(datetime.datetime.now() - time_temp)

print(shift_rotate)

#cv2.imwrite("diff.jpg" , diff)

_ , diff = cv2.threshold(diff, 15 , 255 , cv2.THRESH_BINARY)
#cv2.imwrite("thresholded.jpg" , diff)

diff = cv2.erode(diff , np.full((3,3),255, np.uint8)  , iterations = 4)
#cv2.imwrite("eroded.jpg" , diff)

diff = cv2.dilate(diff , np.full((7,7),255, np.uint8)  , iterations = 10)
#cv2.imwrite("dilated.jpg" , diff)
dilated = diff.copy()

image_temp = img1_original.copy()
width, height = img1.size
# time_temp = datetime.datetime.now()
for i in shift_rotate:
    if i[0]=='x':
        x = i[1]*scale
        if x>0:
            image_temp = ImageChops.offset(image_temp, x, 0)
            image_temp.paste((0,0,0), (0, 0, x, height))
        elif x<0:
            image_temp = ImageChops.offset(image_temp, x, 0)
            image_temp.paste((0,0,0), (width+x, 0, width, height))
            
    elif i[0]=='y':
        y = i[1]*scale
        if y>0:
            image_temp = ImageChops.offset(image_temp, 0, y)
            image_temp.paste((0,0,0), (0, 0, width, y))
        elif y<0:
            image_temp = ImageChops.offset(image_temp, 0, y)
            image_temp.paste((0,0,0), ( 0, height+y, width, height))
            
    else:
        image_temp.rotate(i[1])
# print(datetime.datetime.now() - time_temp)

background_temp = bg_original.copy()
image_temp = np.array(image_temp)
background_temp = np.array(background_temp)
background_temp[dilated==255] = image_temp[dilated==255]
Image.fromarray(background_temp).save("final.jpg")


# np.save("test/diff.npy", diff)
# open("test/shift_rotate.txt","w").write(str(shift_rotate))
