import cv2 
import numpy as np
import RPi.GPIO as GPIO
from time import sleep

#set GPIO numbering mode and define output pins

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

cap = cv2.VideoCapture(0)
_, frame = cap.read()
row, cols, _ = frame.shape

x_medium = int(cols/2)
center = int(cols / 2)

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    #RED COLOR
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    
    
    #ret, thresh = cv2.threshold(red_mask , 107,205,0)
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   # _, contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    cnt = contours [0]
    area = cv2.contourArea(cnt)
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        #CALCULATE THE AREA
        #area = cv2.contourArea(cnt)
        
        #distinguish the time for robot to start move
        if area <15010:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        #move robot forward
            #GPIO.output(7, True)
            #GPIO.output(11, False)
            #GPIO.output(13, True)
            #GPIO.output(15, False)
            #sleep(0.5)#
        
        else:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        
        cv2.putText(frame, str(area), (x, y), 0, 1, (0, 255, 0))
        
        x_medium = int((x + x + w) / 2)
            
        
        break
    
    cv2.line( frame, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)
    
    cv2.imshow("Frwame" , frame)
    #cv2.imshow("mask", red_mask)
    
    key = cv2. waitKey(1)
    
    if key == 27:
        break
    #if key == ord ("q"):
     #   GPIO.output(7, False)
      #  GPIO.output(11, False)
       # GPIO.output(13, False)
        #GPIO.output(15, False)
   #move Robot
    if x_medium < center -60:
       
            GPIO.output(13, False)
            GPIO.output(15, True)
            GPIO.output(7, False)
            GPIO.output(11, False)
       
    elif x_medium > center +60:
       
            GPIO.output(15, False)
            GPIO.output(13, False)
            GPIO.output(7, False)
            GPIO.output(11, True)
    elif area < 15000 :
        
            GPIO.output(7, False)
            GPIO.output(11, True)
            GPIO.output(13, False)
            GPIO.output(15, True)
        
    else:
            GPIO.output(7, False)
            GPIO.output(11, False)
            GPIO.output(13, False)
            GPIO.output(15, False)    


GPIO.cleanup()    
cap.releas()
cv2.destroyAllwindows()

