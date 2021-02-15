import cv2
import numpy as np
bg = cv2.imread("images/bg.jpg")
bg = cv2.resize(bg,(bg.shape[1]//4,bg.shape[0]//4))
cv2.imshow("bg",bg)
img1 = cv2.imread("images/img1.jpg")
img2 = cv2.imread("images/img2.jpg")
img1 = cv2.resize(img1,(bg.shape[1],bg.shape[0]))
img2 = cv2.resize(img2,(bg.shape[1],bg.shape[0]))
cv2.imshow("img1", img1)
cv2.imshow("img2", img2)
cv2.waitKey(0)
print(bg.shape)