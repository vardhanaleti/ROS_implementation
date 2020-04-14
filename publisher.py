#!/usr/bin/env python3

import cv2 
import numpy as np
import sys
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge,CvBridgeError
from face_crop.msg import face_crop1

face_cascade = cv2.CascadeClassifier('/home/aleti/catkin_ws/src/opencv/scripts/haarcascade_frontalface_default.xml')

pub = rospy.Publisher("IMAGE",Image,queue_size = 10)
pub2 = rospy.Publisher("FACE_CROP",face_crop1,queue_size =10)
msg  = face_crop1()

rospy.init_node('FEED',anonymous = True)
rate = rospy.Rate(100)
bridge = CvBridge()



def get_resource():	
	
	resource = sys.argv[1]
	if len(resource) < 3:
		resource_name = "/dev/video" + resource   #prompting to use the webcam
		resource = int(resource)
	else:
		resource_name = resource
	return resource,resource_name



def  FEED():
	
	
	resource1,resource_name1 = get_resource()	
	cap = cv2.VideoCapture(resource1)

	ret,frame = cap.read()
	
	while ret:
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray,1.3,5)
		for (x,y,w,h) in faces:
			cv2.rectangle(frame, (x,y), (x+w,y+h),(255,0,0),2)
			msg.x = x
			msg.y = y
			msg.w = w
			msg.h = h

		
		pub.publish(bridge.cv2_to_imgmsg(frame,"bgr8"))
		pub2.publish(msg)
		cv2.imshow("Stream: " + resource_name1, frame)
		ret,frame = cap.read()
		rate.sleep()
		if cv2.waitKey(1) == ord('q'):
			break;

	cap.release()
	cv2.destroyAllWindows()
	
if __name__== '__main__':
	FEED()
	
