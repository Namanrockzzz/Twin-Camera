## changed version
import cv2
import numpy as np
from PIL import Image, ImageChops, ImageOps
from .image_transformer import ImageTransformer
from django.conf import settings
from TwinCamera.models import Image as instance
import os
import time

def get_progress(path):
    f = open(path+"/progress.txt","r")
    temp = f.readline()
    f.close()
    return float(temp)

def update_progress(value,path):
    f = open(path+"/progress.txt","w")
    f.write(str(value))
    f.close()

def x_shift(image, background, mask_orig, minimum, x_min, x_max,path, change):
    
    final_x = 0
    images = []
    masks = [] 
    width, height = image.size
    
    for x in range(x_min, x_max+1,1):
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
    update_progress(int(get_progress(path))+change, path)
    return minimum, images[index] , masks[index], final_x

def y_shift(image, background, mask_orig, minimum, y_min, y_max,path, change):

    final_y = 0
    images = []
    masks = []
    width, height = image.size
    
    for y in range(y_min, y_max+1,1):
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
    update_progress(int(get_progress(path))+change, path)
    return minimum, images[index] , masks[index], final_y

def theta_rotate_along_x(image, background, mask_orig, minimum, deg_min, deg_max,path, change):
    final_theta = 0
    images = []
    masks = []
    it1 = ImageTransformer(image)
    it2 = ImageTransformer(mask_orig)
    for theta in range(deg_min, deg_max+1,1):
         #shift
        image_temp = it1.rotate_along_axis(phi=theta)
        mask_temp = it2.rotate_along_axis(phi=theta) 
        
        
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
    update_progress(int(get_progress(path))+change,path)
    return minimum, images[index] , masks[index], final_theta

def theta_rotate_along_y(image, background, mask_orig, minimum, deg_min, deg_max,path, change):
    final_theta = 0
    images = []
    masks = []
    it1 = ImageTransformer(image)
    it2 = ImageTransformer(mask_orig)
    for theta in range(deg_min, deg_max+1,1):
         #shift
        image_temp = it1.rotate_along_axis(theta=theta)
        mask_temp = it2.rotate_along_axis(theta=theta) 
        
        
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
    update_progress(int(get_progress(path))+change,path)
    return minimum, images[index] , masks[index], final_theta

def theta_rotate_along_z(image, background, mask_orig, minimum, deg_min , deg_max ,path, change):
    final_theta = 0
    images = []
    masks = []
    for theta in range(deg_min, deg_max+1,1):
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
    update_progress(int(get_progress(path))+change,path)
    return minimum, images[index] , masks[index], final_theta

def merge(bg_orig , imgs_orig, path, change):
    update_progress(int(get_progress(path))+change,path)
    width, height = bg_orig.size
    scale = max(width, height)//1000
    if scale==0:
        scale=1
    bg = bg_orig.copy()
    bg = bg.resize((bg.size[0]//scale, bg.size[1]//scale))
    imgs = []
    for img in imgs_orig:
        img1 = img.copy()
        img1 = img1.resize((bg.size[0],bg.size[1]))
        imgs.append(img1)
    update_progress(int(get_progress(path))+change,path)
    diffs = find_diff_helper(bg , imgs, path, change)
    
    zipped_diffs_imgs = zip(diffs,imgs_orig)
    sorted_diffs_imgs = sorted(zipped_diffs_imgs, key = lambda x: np.count_nonzero(x[0][0]>=27))
    tuples = zip(*sorted_diffs_imgs)
    diffs, imgs_orig = [list(t) for t in tuples]
    
    background_temp = bg_orig.copy()
    background_temp = np.array(background_temp)
    change2 = (100-get_progress(path))/len(imgs)
    print(change2)
    for j,img in enumerate(imgs):
        diff = diffs[j][0]
        _ , diff = cv2.threshold(diff, 27, 255, cv2.THRESH_BINARY)
        diff = cv2.erode(diff , np.full((3,3),255, np.uint8)  , iterations = 4)
        diff = cv2.dilate(diff , np.full((5,5),255, np.uint8)  , iterations = 23)
        diff = cv2.resize(diff, bg_orig.size)
        dilated = diff.copy()
        image_temp = imgs_orig[j].copy()
        width, height = img.size
        mask = cv2.resize(diffs[j][2] , imgs_orig[j].size)
        for i in diffs:
            print(i[1])

        for i in diffs[j][1]:
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

            elif i[0]=='r':
                image_temp.rotate(i[1])
            elif i[0]=='ax':
                it = ImageTransformer(image_temp)
                image_temp = it.rotate_along_axis(phi=i[1])
                image_temp = Image.fromarray(image_temp)
            else:
                it = ImageTransformer(image_temp)
                image_temp = it.rotate_along_axis(theta=i[1])
                image_temp = Image.fromarray(image_temp)
        image_temp = np.array(image_temp)
        dilated[mask==0] = 0
        background_temp[dilated>0] = image_temp[dilated>0]
        update_progress(int(get_progress(path))+change2,path)

    Image.fromarray(background_temp).save(path + "final.jpg")
    update_progress(0,path)

def find_diff_helper(background, image_list, path, change):
    diff = []
    for i,image in enumerate(image_list):
        diff.append(find_diff(image, background, path, change))
    return diff

def find_diff(image, background, path, change):
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
    
    temp, image1 , mask_orig1 , x = x_shift(image, background, mask_orig, minimum,-50, 50, path, change)
    
    temp, image1 , mask_orig1 , y= y_shift(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, -50, 50, path, change) 
    
    temp, image1  ,mask_orig1 , theta= theta_rotate_along_z(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, -7 , 7, path, change)
    
    temp, image1, mask_orig1, theta_x = theta_rotate_along_x(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, -7 , 7, path, change)
    
    temp, image1, mask_orig1, theta_y = theta_rotate_along_y(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, -7 , 7, path, change)
    print("Case1: ",end=" ")
    print(x,y,theta)
    if temp<MIN:
        MIN = temp
        MASK = mask_orig1
        IMAGE = image1
        temp_x = x
        temp_y = y
        shift_rotate = [('x',x) ,('y' ,y) ,('r', theta),('ax',theta_x),('ay',theta_y)]
        
    ################################# case2 #######################################
    #y,x,theta
    print("CASE 2")
    minimum = 255
    
    temp, image1  ,mask_orig1 , y = y_shift(image, background, mask_orig, minimum, temp_y-15, temp_y+15, path, change)
    
    temp, image1 , mask_orig1 , x = x_shift(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, temp_x-15, temp_x+15, path, change) 
    
    temp, image1 , mask_orig1 ,theta= theta_rotate_along_z(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, -7 , 7, path, change)
    
    temp, image1, mask_orig1, theta_x = theta_rotate_along_x(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, -7 , 7, path, change)
    
    temp, image1, mask_orig1, theta_y = theta_rotate_along_y(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, -7 , 7, path, change)
    print("Case2: ",end=" ")
    print(x,y,theta)
    if temp<MIN:
        MIN = temp
        MASK = mask_orig1
        IMAGE = image1
        temp_x = x
        temp_y = y
        shift_rotate = [('y',y) ,('x' ,x) ,('r', theta),('ax',theta_x),('ay',theta_y)]
    ################################# case3 #######################################
    #theta,y,x
    print("CASE 3")
    minimum = 255
    
    temp, image1 , mask_orig1 , theta= theta_rotate_along_z(image, background, mask_orig, minimum, -7 , 7, path, change)
    
    temp, image1 , mask_orig1 , y= y_shift(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, temp_y-15, temp_y+15, path, change) 
    
    temp, image1 , mask_orig1 , x= x_shift(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, temp_x-15, temp_x+15, path, change)
    
    temp, image1, mask_orig1, theta_x = theta_rotate_along_x(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, -7 , 7, path, change)
    
    temp, image1, mask_orig1, theta_y = theta_rotate_along_y(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, -7 , 7, path, change)
    print("Case3: ",end=" ")
    print(x,y,theta)
    if temp<MIN:
        MIN = temp
        MASK = mask_orig1
        IMAGE = image1
        temp_x = x
        temp_y = y
        shift_rotate = [('r', theta) ,('y',y) ,('x' ,x),('ax',theta_x),('ay',theta_y) ]
    
    ################################# case4 #######################################
    #x,theta,y
    print("CASE 4")
    minimum = 255
    temp, image1 , mask_orig1 , x = x_shift(image, background, mask_orig, minimum, temp_x-15, temp_x+15, path, change)

    temp, image1 , mask_orig1 , theta= theta_rotate_along_z(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, -7 , 7, path, change)
    
    temp, image1 , mask_orig1, y = y_shift(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, temp_y-15, temp_y+15, path, change)
    
    temp, image1, mask_orig1, theta_x = theta_rotate_along_x(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, -7 , 7, path, change)
    
    temp, image1, mask_orig1, theta_y = theta_rotate_along_y(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, -7 , 7, path, change)
    print("Case4: ",end=" ")
    print(x,y,theta)
    if temp<MIN:
        MIN = temp
        MASK = mask_orig1
        IMAGE = image1
        temp_x = x
        temp_y = y
        shift_rotate = [('x' ,x) , ('r', theta) ,('y',y),('ax',theta_x),('ay',theta_y)]
    
    ################################# case5 #######################################
    #theta, x, y
    print("CASE 5")
    minimum = 255
    temp, image1 , mask_orig1 ,theta = theta_rotate_along_z(image, background, mask_orig, minimum, -7 , 7, path, change)
    
    temp, image1 , mask_orig1 ,x= x_shift(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, temp_x-15, temp_x+15, path, change)
    
    temp, image1 , mask_orig1 ,y= y_shift(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, temp_y-15, temp_y+15, path, change)
    
    temp, image1, mask_orig1, theta_x = theta_rotate_along_x(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, -7 , 7, path, change)
    
    temp, image1, mask_orig1, theta_y = theta_rotate_along_y(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, -7 , 7, path, change)
    print("Case5: ",end=" ")
    print(x,y,theta)
    if temp<MIN:
        MIN = temp
        MASK = mask_orig1
        IMAGE = image1
        temp_x = x
        temp_y = y
        shift_rotate = [ ('r', theta) ,('x' ,x) ,('y',y),('ax',theta_x),('ay',theta_y)]
    
    ################################# case6 #######################################
    # y,theta,x
    print("CASE 6")
    minimum = 255
    temp, image1 , mask_orig1 ,y = y_shift(image, background, mask_orig, minimum, temp_y-15, temp_y+15, path, change)
    
    temp, image1 , mask_orig1 ,theta= theta_rotate_along_z(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, -7 , 7, path, change)
    
    temp, image1 , mask_orig1 ,x= x_shift(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, temp_x-15, temp_x+15, path, change) 
    
    temp, image1, mask_orig1, theta_x = theta_rotate_along_x(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, -7 , 7, path, change)
    
    temp, image1, mask_orig1, theta_y = theta_rotate_along_y(Image.fromarray(image1), background, Image.fromarray(mask_orig1), temp, -7 , 7, path, change)
    print("Case6: ",end=" ")
    print(x,y,theta)
    if temp<MIN:
        MIN = temp
        MASK = mask_orig1
        IMAGE = image1
        temp_x = x
        temp_y = y
        shift_rotate = [('y',y), ('r', theta) ,('x' ,x),('ax',theta_x),('ay',theta_y) ]

    ####################################################################################
                
    background_temp = np.bitwise_and(background , MASK)
    best_match = cv2.absdiff(background_temp , IMAGE)
    return best_match, shift_rotate, MASK

def start(name):
    Name = name
    path = str(settings.MEDIA_ROOT)+"/images/"+str(name)+"/"
    update_progress(0,path)
    img1_original = None
    img2_original = None
    img3_original = None
    img4_original = None
    img5_original = None
    img6_original = None
    for i in os.listdir(path):
        if path+i and 'bg.' in i:
            bg_original = Image.open(path+i)
        elif path+i and 'img1.' in i:
            img1_original = Image.open(path+i)
        elif path+i and 'img2.' in i:
            img2_original = Image.open(path+i)
        elif path+i and 'img3.' in i:
            img3_original = Image.open(path+i)
        elif path+i and 'img4.' in i:
            img4_original = Image.open(path+i)
        elif path+i and 'img5.' in i:
            img5_original = Image.open(path+i)
        elif path+i and 'img6.' in i:
            img6_original = Image.open(path+i)
        else:
            pass
    
    l = []
    if img1_original:
        l.append(img1_original)
    if img2_original:
        l.append(img2_original)
    if img3_original:
        l.append(img3_original)
    if img4_original:
        l.append(img4_original)
    if img5_original:
        l.append(img5_original)
    if img6_original:
        l.append(img6_original)
    change = 100/(34*len(l))
    merge(bg_original, l, path, change)
    update_progress(100,path)
    return 
