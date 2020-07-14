#install numpy using pip install numpy
#install opencv using sudo apt-get install python-opencv
#import libraries numpy,opencv and time
import numpy as np
import cv2
import time

cap=cv2.VideoCapture(0)

time.sleep(2)

backgound=0

#capturing the backgournd..with 30 iterations to make sure backgorund is captured with all pixels
for i in range(30):
    ret,background=cap.read()

#capturing image of a person
while(cap.isOpened()):
    ret,img=cap.read()
    if not ret:
        break 

    hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  #Hue saturation value 

    #HSV values
    lower_red=np.array([0,120,70])
    upper_red=np.array([10,255,255])
    mask1=cv2.inRange(hsv,lower_red,upper_red)  #Seperating the cloak aprt

    lower_red=np.array([170,120,70])
    upper_red=np.array([180,255,255])
    mask2=cv2.inRange(hsv,lower_red,upper_red)

    mask1=mask1+mask2 #or 1 or X
    # for removing noise from the image
    # making metrix array of 1 of image and removing noise using morphopen 
    mask1=cv2.morphologyEx(mask1, cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    #smoothening the image using morphDilate
    mask1=cv2.morphologyEx(mask1, cv2.MORPH_DILATE,np.ones((3,3),np.uint8))

    mask2=cv2.bitwise_not(mask1) #Excpt the clock mask everything

    res1=cv2.bitwise_and(background,background,mask=mask1) #used for segmentation of the colour
    res2=cv2.bitwise_and(img,img,mask=mask2) #used to substitude the cloak part with background

    finalOutput=cv2.addWeighted(res1,1,res2,1,0)

    cv2.imshow("magic",finalOutput)
    cv2.waitKey(10)
    
cap.release()
cv2.destroyAllWindows()
    

