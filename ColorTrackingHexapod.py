#----Code Modified by Alfredo Any----------------
#----For Robot project---------------------------
#----ECE 590 - Robot Design and Implementation---
#----Instructor: Dr. Daniel M. Lofaro------------


import numpy as np
import cv2
import cv, math
import time
import serial

cap = cv2.VideoCapture(0)
ser = serial.Serial('/dev/ttyACM0', 9600)
ser1 = serial.Serial('/dev/ttyAMA0', 9600)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    #frame = cv2.flip(frame,1)
    #frame = cv2.resize(frame, (160,120))
    # Display the resulting frame
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([ 95, 50, 50], dtype=np.uint8)
    upper_blue = np.array([130,255,255], dtype=np.uint8)
    lower_green = np.array([52, 50, 50], dtype=np.uint8)
    upper_green = np.array([68,255,255], dtype=np.uint8)
    lower_red1 = np.array([0, 50, 50], dtype=np.uint8)
    upper_red1 = np.array([8,255,255], dtype=np.uint8)
    lower_red2 = np.array([172, 50, 50], dtype=np.uint8)
    upper_red2 = np.array([180,255,255], dtype=np.uint8)
    lower_yellow = np.array([22, 50, 50], dtype=np.uint8)
    upper_yellow = np.array([38,255,255], dtype=np.uint8)
    

    # Threshold the HSV image to get only blue colors
    maskblue = cv2.inRange(hsv, lower_blue, upper_blue)
    maskgreen = cv2.inRange(hsv, lower_green, upper_green)
    maskred1 = cv2.inRange(hsv, lower_red1, upper_red1)
    maskred2 = cv2.inRange(hsv, lower_red2, upper_red2)
    maskred = maskred1 + maskred2
    maskyellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask = maskblue + maskgreen + maskred
    binary_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    binary_green = cv2.inRange(hsv, lower_green, upper_green)
    binary_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    binary_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    binary_red = binary_red1 + binary_red2
    binary_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    binary = binary_green + binary_blue + binary_red
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    maskblue = cv2.dilate(maskblue, None, 18)
    maskblue = cv2.erode(maskblue, None, 10)
    maskgreen = cv2.dilate(maskgreen, None, 18)
    maskgreen = cv2.erode(maskgreen, None, 10)
    maskred = cv2.dilate(maskred, None, 18)
    maskred = cv2.erode(maskred, None, 10)
    maskyellow = cv2.dilate(maskyellow, None, 18)
    maskyellow = cv2.erode(maskyellow, None, 10)
    mask = cv2.dilate(mask, None, 18)
    mask = cv2.erode(mask, None, 10)

#--------------------------Editing Starts Here-----------------------------
#-------------------For Multiple Color Tracking Code-----------------------
    
    
    #def thresh_callback(thresh):
    #edges = cv2.Canny(blur,thresh,thresh*2)
    drawing = np.zeros(frame.shape,np.uint8)
    #Contours for tracking
    contours_blue, hierarchy = cv2.findContours(maskblue, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, hierarchy = cv2.findContours(maskgreen, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours_red, hierarchy = cv2.findContours(maskred, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow, hierarchy = cv2.findContours(maskyellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #contours, hierarchy = cv2.findContours(frame, 1, 2)

    points = []

    for cnt in contours_green:
	moments = cv2.moments(cnt)
	area = cv2.contourArea(cnt)
	perimeter = cv2.arcLength(cnt,True)
	epsilon = 0.1*perimeter
	approx = cv2.approxPolyDP(cnt,epsilon,True)
	if moments['m00'] != 0 and area>1000:
		x1 = int(moments['m10']/moments['m00'])         # cx = M10/M00
	       	y1 = int(moments['m01']/moments['m00'])         # cy = M01/M00
		moments_area = moments['m00']
		contour_area = cv2.contourArea(cnt)

		bound_rect = cv2.boundingRect(cnt)
	
		pt1 = (bound_rect[0], bound_rect[1])
		pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
		points.append(pt1)
		points.append(pt2)
		#cv2.rectangle(frame, pt1, pt2, (0,255,0),2)

		xn = x1/640.0 * 2 -1
	  	yn = y1/480.0 * 2 -1

		xb = math.fabs(xn) * 127
		yb = math.fabs(yn) * 127
		if xn > 0 and xn < 256:
		   xb = xb + 127
		if yn > 0 and yn < 256:
		   yb = yb + 127
		#x2 = int(round(x2))
		#y2 = int(round(y2))
		xb = int(round(xb))
		yb = int(round(yb))
		ser.write(chr(xb))
		ser1.write(chr(yb))

		cv2.drawContours(frame,[cnt], 0, (0,255,0),2)
		cv2.circle(frame,(x1,y1),5,(0,0,255),-1)      # draw centroids in red color
		cv2.putText(frame,"green"+"="+str(x1)+","+str(y1), (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
		

    for cnt in contours_blue:
	moments = cv2.moments(cnt)
	area = cv2.contourArea(cnt)
	perimeter = cv2.arcLength(cnt,True)
	epsilon = 0.1*perimeter
	approx = cv2.approxPolyDP(cnt,epsilon,True)
	if moments['m00'] != 0 and area > 1000:
		x2 = int(moments['m10']/moments['m00'])         # cx = M10/M00
	       	y2 = int(moments['m01']/moments['m00'])         # cy = M01/M00
		moments_area = moments['m00']
		contour_area = cv2.contourArea(cnt)

		bound_rect = cv2.boundingRect(cnt)
	
		pt1 = (bound_rect[0], bound_rect[1])
		pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
		points.append(pt1)
		points.append(pt2)
		#cv2.rectangle(frame, pt1, pt2, (0,255,0),2)

		
		
		xn = x2/640.0 * 2 -1
	  	yn = y2/480.0 * 2 -1

		xb = math.fabs(xn) * 127
		yb = math.fabs(yn) * 127
		if xn > 0 and xn < 256:
		   xb = xb + 127
		if yn > 0 and yn < 256:
		   yb = yb + 127
		#x2 = int(round(x2))
		#y2 = int(round(y2))
		xb = int(round(xb))
		yb = int(round(yb))
		ser.write(chr(xb))
		ser1.write(chr(yb))

		cv2.drawContours(frame,[cnt], 0, (0,255,0),2)
		cv2.circle(frame,(x2,y2),5,(0,0,255),-1)      # draw centroids in red color
		cv2.putText(frame,"blue"+"="+str(xb)+","+str(yb), (xb,yb), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)


    for cnt in contours_red:
	moments = cv2.moments(cnt)
	area = cv2.contourArea(cnt)
	perimeter = cv2.arcLength(cnt,True)
	epsilon = 0.1*perimeter
	approx = cv2.approxPolyDP(cnt,epsilon,True)
	if moments['m00'] != 0  and area > 1000:
		x3 = int(moments['m10']/moments['m00'])         # cx = M10/M00
	       	y3 = int(moments['m01']/moments['m00'])         # cy = M01/M00
		moments_area = moments['m00']
		contour_area = cv2.contourArea(cnt)

		bound_rect = cv2.boundingRect(cnt)
	
		pt1 = (bound_rect[0], bound_rect[1])
		pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
		points.append(pt1)
		points.append(pt2)
		#cv2.rectangle(frame, pt1, pt2, (0,255,0),2)

		xn = x3/640.0 * 2 -1
	  	yn = y3/480.0 * 2 -1

		xb = math.fabs(xn) * 127
		yb = math.fabs(yn) * 127
		if xn > 0 and xn < 256:
		   xb = xb + 127
		if yn > 0 and yn < 256:
		   yb = yb + 127
		#x2 = int(round(x2))
		#y2 = int(round(y2))
		xb = int(round(xb))
		yb = int(round(yb))
		ser.write(chr(xb))
		ser1.write(chr(yb))

		cv2.drawContours(frame,[cnt], 0, (0,255,0),2)
		cv2.circle(frame,(x3,y3),5,(0,0,255),-1)      # draw centroids in red color
		cv2.putText(frame,"red"+"="+str(x3)+","+str(y3), (x3,y3), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)



    cv2.imshow('input',frame)
    #cv2.imshow('yellow_mask',binary_yellow)
    #cv2.imshow('green_mask', binary_green)
    #cv2.imshow('red_mask', binary_red)
    #cv2.imshow('output', drawing)
    cv2.imshow('All Masks', binary)
    #cv2.imshow('res',res)    
   
  
  #  cv2.createTrackbar('canny thresh:','input',thresh,max_thresh,thresh_callback)
   # thresh_callback(200)
    if cv2.waitKey(10) == 27:
    	break
