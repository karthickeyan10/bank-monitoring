import numpy as np
import time
import imutils
import cv2

avg = None
video = cv2.VideoCapture("people-capture.mp4")
xvalues = list()
motion = list()
count1 = 0
count2 = 0
def find_majority(k):
    myMap = {}
    maximum = ( '', 0 ) # (occurring element, occurrences)
    for n in k:
        if n in myMap: myMap[n] += 1
        else: myMap[n] = 1
        if myMap[n] > maximum[1]: maximum = (n,myMap[n])

    return maximum

while 1:
    ret, frame = video.read() #iterate each frame
    flag = True
    text=""

    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
    gray = cv2.GaussianBlur(gray, (21, 21), 0) #its reduces the noise and smoothean the image 
    
    if avg is None:
        print("[INFO] starting background model...")
        avg = gray.copy().astype("float") #none is override to store the value of fram(rep gray)
        #stored in float data type to the avg variable 
        continue

    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg)) #diff bw prev and curr image dist
    thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)# reduce noise & improve img qual
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        if cv2.contourArea(c) < 5000:  #5000 pixels it will negelect the small size of the object(only calculated human )
           continue
        (x, y, w, h) = cv2.boundingRect(c)
        xvalues.append(x)
        flag = False
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    no_x = len(xvalues) #no of elements 
    
    if (no_x > 2): #atleast two elements that means last two elements diff
        difference = xvalues[no_x - 1] - xvalues[no_x - 2]
        if(difference > 0):
            motion.append(1)
        else:
            motion.append(0)

    if flag is True:
        if (no_x > 5): # atleast 5 elements 
            val, times = find_majority(motion)
            if val == 1 and times >= 15: #threshole(15)
                count1 += 1
            else:
                count2 += 1
                
        xvalues = list()
        motion = list()

    cv2.line(frame, (260, 0), (260,480), (0,255,0), 2)
    cv2.line(frame, (420, 0), (420,480), (0,255,0), 2)	
    cv2.putText(frame, "In: {}".format(count1), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
     #(10,20 means left x axis(10) and height yaxis(20) )
     # font style, font scale, color, and thickness 
    cv2.putText(frame, "Out: {}".format(count2), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow("Frame",frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    
video.release()
cv2.destroyAllWindows()
