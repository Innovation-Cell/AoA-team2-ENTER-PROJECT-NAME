#! /usr/bin/env python
import numpy as np   
import imutils 
import cv2
from cv_bridge import CvBridge
import rospy
from sensor_msgs.msg import Image
import rospy

from geometry_msgs.msg import Twist
from math import atan2

# This drives the program into an infinite loop. 
def blue(img): 
    lower_blue = np.array([80,0,0]) 
    upper_blue = np.array([255,40,40]) 
    img = cv2.resize(img,(400,300)) 
    mask = cv2.inRange(img, lower_blue, upper_blue) 
    res = cv2.bitwise_and(img,img, mask= mask) 
    #edges = cv2.Canny(res,100,200) 
    gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0,255, cv2.THRESH_BINARY)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    areas = [cv2.contourArea(c) for c in cnts]
    max_index = np.argmax(areas)
    c=cnts[max_index]
    M = cv2.moments(c)
    area = areas[max_index]
    #cv2.imshow('color',thresh) 
    try:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return cX-200,area
    except:
        return 0,area
def move(angle, area):

    
    diff = angle
    if area < 1000 and area > 10:
            
        if diff < -15:
            speed.linear.x = 0.5
            speed.angular.z = 0.5

        elif diff > 15:
            speed.linear.x = 0.5
            speed.angular.z = -0.5

        else:
            speed.linear.x = 0.5
            speed.angular.z = 0.0
    elif area > 30000:
        speed.linear.x = -0.1
        speed.angular.z = 0

    else:
	speed.linear.x = 0.0
	speed.angular.z = 0.0

    pub.publish(speed)

    r.sleep()

def detect(data):
    
    bridge = CvBridge()
    image = bridge.imgmsg_to_cv2(data, "bgr8")
    print("3")
    px_dist, area = blue(image)
    wide_angle = 180
    angle = (px_dist*wide_angle)/400 
    print(px_dist)
    print(" ")
    print(angle)
    print(" ")
    print(area)
    move(angle, area)
    k = cv2.waitKey(5) & 0xFF

if __name__ == '__main__':
    rospy.init_node('image_gazebo', anonymous=True)
    rospy.Subscriber("/mybot/camera2/image_raw", Image, detect)
    pub = rospy.Publisher("/cmd_vel1",Twist,queue_size=1)
    speed = Twist()
    r = rospy.Rate(4)
    rospy.spin()



