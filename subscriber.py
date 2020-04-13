#!/usr/bin/env python3


import rospy 
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from face_crop.msg import face_crop1


class image():
	
	def __init__(self):	
		self.bridge = CvBridge()
		self.image_sub=rospy.Subscriber("IMAGE",Image,self.image_callback)
		self.rect_sub=rospy.Subscriber("FACE_CROP",face_crop1,self.co_ordinates_callback)
		self.cv_image = None
		self.co_ordinates = None
		self.cropped = None


	def image_callback(self,data):
		
		try:	
			self.cv_image = self.bridge.imgmsg_to_cv2(data,desired_encoding ='passthrough')
		except CvBrigeError as e:
			print(e)
		
	
	def co_ordinates_callback(self,data2):
		
		self.co_ordinates = data2
		self.cropping()
		

	def cropping(self):
		
		if self.cv_image is not None and self.co_ordinates is not None:
	
			start_row = self.co_ordinates.x
			start_col = self.co_ordinates.y
			end_row = self.co_ordinates.h + self.co_ordinates.x
			end_col = self.co_ordinates.w + self.co_ordinates.y

			self.cropped = self.cv_image[start_row:end_row,start_col:end_col]
			self.show_face()


	def show_face(self):
		cv2.imshow("cropped",self.cropped)
		cv2.waitKey(10)


def main():
	img_vid = image()
	rospy.init_node('node_2',anonymous = True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting  down")
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()



