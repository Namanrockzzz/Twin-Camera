import cv2
import numpy as np
from scipy import ndimage

def shadow_remove(img):
    rgb_planes = cv2.split(img)
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_norm_planes.append(norm_img)
    shadowremov = cv2.merge(result_norm_planes)
    return shadowremov

def find_diff(image, background, rangex=50, rangey=50 , range_deg = 7 ):
    #image = shadow_remove(image)
    #background = shadow_remove(background)
    
    if len(image.shape)==3 :
        image = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
    if len(background.shape)==3 :
        background = cv2.cvtColor(background , cv2.COLOR_BGR2GRAY)
    
    #mask to not loose black pixels of background while applying mask after shifting background
    _,mask_orig = cv2.threshold(background , 1, 255 ,cv2.THRESH_BINARY_INV)
    
    minimum = 255
    best_match = None
    for x in range(-rangex , rangex+1,3):
        print(x)
        for y in range(-rangey , rangey+1,3):
            for theta in range(-range_deg , range_deg+1, 2):
                #shift
                background_temp = ndimage.shift(background , shift = [x , y] )
                mask_orig_temp = ndimage.shift(mask_orig , shift = [x,y])
                
                #rotate
                background_temp = ndimage.rotate(background_temp, angle = theta , reshape = False)
                mask_orig_temp = ndimage.rotate(mask_orig_temp , angle = theta, reshape = False)
                
                _,mask_background = cv2.threshold(background_temp , 1 , 255 , cv2.THRESH_BINARY)
                
                #final mask for calculating difference
                mask = mask_background + mask_orig_temp
                
                #size of the significant area
                size = np.sum(mask)/255
                
                image_temp = cv2.bitwise_and(image , mask)
                diff = cv2.absdiff(background_temp , image_temp )
            
                res = np.sum(diff)/size
                if minimum  > res:
                    minimum = res
                    best_match = diff
                    print(x ,y ,theta)
    return best_match

def Left_index(points): 
	
	''' 
	Finding the left most point 
	'''
	minn = 0
	for i in range(1,len(points)): 
		if points[i][0] < points[minn][0]: 
			minn = i 
		elif points[i][0] == points[minn][0]: 
			if points[i][1] > points[minn][1]: 
				minn = i 
	return minn 

def orientation(p, q, r): 
	''' 
	To find orientation of ordered triplet (p, q, r). 
	The function returns following values 
	0 --> p, q and r are colinear 
	1 --> Clockwise 
	2 --> Counterclockwise 
	'''
	val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1]) 

	if val == 0: 
		return 0
	elif val > 0: 
		return 1
	else: 
		return 2

def convexHull(points, n): 
    pts = []
	# There must be at least 3 points 
    if n < 3:
        return

	# Find the leftmost point 
    l = Left_index(points) 

    hull = [] 
	
    ''' Start from leftmost point, keep moving counterclockwise 
    until reach the start point again. This loop runs O(h) 
	times where h is number of points in result or output. '''
    p = l 
    q = 0
    while(True): 
		
		# Add current point to result 
        hull.append(p) 

        ''' 
		Search for a point 'q' such that orientation(p, [1], 
		q) is counterclockwise for all points 'x'. The idea 
		is to keep track of last visited most counterclock- 
		wise point in q. If any point 'i' is more counterclock- 
		wise than q, then update q. 
        '''
        q = (p + 1) % n 

        for i in range(n): 
            
			
			# If i is more counterclockwise 
			# than current q, then update q 
            if(orientation(points[p], points[i], points[q]) == 2): 
            	q = i 

        ''' 
		Now q is the most counterclockwise with respect to p 
		Set p as q for next iteration, so that q is added to 
		result 'hull' 
        '''
        p = q 

		# While we don't come to first point 
        if(p == l): 
        	break
	# Print Result 
    for each in hull: 
    	pts.append([points[each][0] , points[each][1]])
    return pts 

roi = 50
def boundFill(img, contours):
    
    #replqce points of every contour by their bounding rectangle
    for i in range(len(contours)):
        x ,y ,w,h= cv2.boundingRect(contours[i])
        contours[i] = [[x,y] ,[x+w,y+h]]
        
    pts = []
    max_area = 0
    
    j= 0
    while j < len(contours):
        (min_x , min_y) = img.shape
        max_x = max_y = 0
        cnt_included = []
        pts_tmp = []
        cnt = contours[j]
        
        for i,cnt2 in enumerate(contours):
            # if cnt2 lies in roi around cnt
            if cnt[1][0]+roi>=cnt2[0][0] and cnt[0][0]-roi<=cnt2[1][0] and cnt[1][1]+roi>=cnt2[0][1] and cnt[0][1]-roi<=cnt2[1][1]:
                max_x = max([max_x ,cnt[1][0] , cnt2[1][0]])
                min_x = min([min_x ,cnt[0][0] , cnt2[0][0]])
                max_y = max([max_y ,cnt[1][1] , cnt2[1][1]])
                min_y = min([min_y ,cnt[0][1] , cnt2[0][1]])
                cnt_included.append(i)
                pts_tmp = pts_tmp + [contours[i]]
        i=0 
        N =n= len(pts_tmp)
        while i < n :
            pt = pts_tmp[i]
            
            #remove the contours included in roi of cnt
            contours.remove(pt)
            
            #pt includes more than one contours
            if len(pt) > 2 :
                
                #add all contours included in pt
                pts_tmp = pts_tmp + pts_tmp[i][2:]
                pts_tmp.pop(i)
                
                i = i-1 
                n =  n-1
            
            if cnt_included[i]<=j:
                j = j-1
            
            i=i+1
        
        area = (max_x-min_x)*(max_y-min_y)
        if area > max_area:
            max_area = area
            pts = pts_tmp
        
        if N>1:
            #add the contours and bounding rectangle of the roi around cnt
            contours.append([[min_x , min_y] , [max_x ,max_y]]+pts_tmp)
            
        j = j+1
        
    #add other two points of bounding rectangle of all the other contours    
    for i in range(len(pts)):
        x1 = pts[i][0][0]
        x2 = pts[i][1][0]
        y1 = pts[i][0][1]
        y2 = pts[i][1][1]
        pts[i] = pts[i]+[[x1,y2],[x2,y1]]
    
    pts = np.array(pts , np.int32).reshape((-1,2))
    pts = convexHull(pts, len(pts))
    pts =  np.array([pts] , np.int32)
    pts = pts.reshape((-1,1, 2)) 
    
    res = cv2.fillPoly(np.zeros(img.shape , np.uint8), [pts], (255,255,255))
    
    return res

bg = cv2.imread("images/bg.jpg")
bg = cv2.resize(bg,(bg.shape[1]//4,bg.shape[0]//4))
cv2.imshow("bg",bg)
img1 = cv2.imread("images/img1.jpg")
img2 = cv2.imread("images/img2.jpg")
img1 = cv2.resize(img1,(bg.shape[1],bg.shape[0]))
img2 = cv2.resize(img2,(bg.shape[1],bg.shape[0]))
cv2.imshow("img1", img1)
cv2.imshow("img2", img2)

diff = find_diff(img1 , bg)
_ , diff = cv2.threshold(diff, 30 , 255 , cv2.THRESH_BINARY)
cv2.imshow("thresholded" , diff)
diff = cv2.erode(diff , np.ones((3,3), np.uint8)  , iterations = 3)

canny = cv2.Canny(diff , 90 ,100)
contours , hierarchy = cv2.findContours(canny , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_NONE)

finalmask = boundFill(diff , contours)
detected = cv2.bitwise_and(finalmask , img1 )
cv2.imshow("detected" , detected)


cv2.waitKey(0)
print(bg.shape)