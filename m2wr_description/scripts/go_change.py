#!/usr/bin/env python

import numpy as np
import time
from numpy import ones,vstack
from numpy.linalg import lstsq
from statistics import mean
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pyplot as plt
import cv2
from cv_bridge import CvBridge
import rospy
from sensor_msgs.msg import Image
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point,Twist
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from math import atan2


def roi(img, vertices):
    
    #blank mask:
    mask = np.zeros_like(img)   
    
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, 255)
    
    #returning the image only where mask pixels are nonzero
    masked = cv2.bitwise_and(img, mask)
    return masked
def draw_lanes(img, lines, color=[255, 0, 0], thickness=3):

    # if this fails, go with some default line
    try:

        # finds the maximum y value for a lane marker 
        # (since we cannot assume the horizon will always be at the same point.)

        ys = []  
        for i in lines:
            for ii in i:
                ys += [ii[1],ii[3]]
        min_y = min(ys)
        max_y = 400
        #600
        new_lines = []
        line_dict = {}

        for idx,i in enumerate(lines):
            for xyxy in i:
                # These four lines:
                # modified from http://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points
                # Used to calculate the definition of a line, given two sets of coords.
                x_coords = (xyxy[0],xyxy[2])
                y_coords = (xyxy[1],xyxy[3])
                A = vstack([x_coords,ones(len(x_coords))]).T
                m, b = lstsq(A, y_coords)[0]

                # Calculating our new, and improved, xs
                x1 = (min_y-b) / m
                x2 = (max_y-b) / m

                line_dict[idx] = [m,b,[int(x1), min_y, int(x2), max_y]]
                new_lines.append([int(x1), min_y, int(x2), max_y])

        final_lanes = {}

        for idx in line_dict:
            final_lanes_copy = final_lanes.copy()
            m = line_dict[idx][0]
            b = line_dict[idx][1]
            line = line_dict[idx][2]
            
            if len(final_lanes) == 0:
                final_lanes[m] = [ [m,b,line] ]
                
            else:
                found_copy = False

                for other_ms in final_lanes_copy:

                    if not found_copy: #1.2 and 0.8
                        if abs(other_ms*1.2) > abs(m) > abs(other_ms*0.8):
                            if abs(final_lanes_copy[other_ms][0][1]*1.2) > abs(b) > abs(final_lanes_copy[other_ms][0][1]*0.8):
                                final_lanes[other_ms].append([m,b,line])
                                found_copy = True
                                break
                        else:
                            final_lanes[m] = [ [m,b,line] ]

        line_counter = {}

        for lanes in final_lanes:
            line_counter[lanes] = len(final_lanes[lanes])

        top_lanes = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]

        lane1_id = top_lanes[0][0]
        lane2_id = top_lanes[1][0]

        def average_lane(lane_data):
            x1s = []
            y1s = []
            x2s = []
            y2s = []
            for data in lane_data:
                x1s.append(data[2][0])
                y1s.append(data[2][1])
                x2s.append(data[2][2])
                y2s.append(data[2][3])
            return int(mean(x1s)), int(mean(y1s)), int(mean(x2s)), int(mean(y2s)) 

        l1_x1, l1_y1, l1_x2, l1_y2 = average_lane(final_lanes[lane1_id])
        l2_x1, l2_y1, l2_x2, l2_y2 = average_lane(final_lanes[lane2_id])

        return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], lane1_id, lane2_id
    except Exception as e:
        print(str(e))
def process_img(image):
    original_image = image
    height = image.shape[0]
    width = image.shape[1]
    #vertices = np.array([[0, height],[width / 2, height / 2],[width, height]],np.int32)
    #vertices = np.array([[0,0],[0, height],[width, height],[width,0]],np.int32)
    #vertices = np.array([[0,height/2],[0,0,height],[width,height],[width,height/2]],np.int32)
    vertices = np.array([[0,(3*height)/4],[width / 2, height / 2],[width,(3*height)/4],[width,height],[0, height]],np.int32)
    #vertices = np.array([[0,(5*height)/8],[width / 2, height / 2],[width,(5*height)/8],[width,height],[0, height]],np.int32)

    # convert to gray
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # edge detection
    processed_img =  cv2.Canny(processed_img, threshold1= 60, threshold2= 255)
    #keep threshold 100,200 or 50,220
    processed_img = cv2.GaussianBlur(processed_img,(5,5),0)
    processed_img = roi(processed_img, [vertices])

    # more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
    #                                     rho=1 or 25  theta   thresh  min length=40,30,*45 max gap=25,20,*30:
    # 21, ,180,50,35
    lines = cv2.HoughLinesP(processed_img, 21, np.pi/180, 190,      10,       60)
    m1 = 0
    m2 = 0
    try:
        l1, l2, m1,m2 = draw_lanes(original_image,lines)
        '''
        if abs(l1[2]-l2[2])<60:
            if m1>0 and m2>0:
                  l2[2] = 400-l1[2]
                  l2[0] = 400 -l1[0]
            if m2<0 and m1<0:
                  l1[2] = 400-l2[2]
                  l1[0] = 400 -l2[0]
        '''
        cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0,255,0], 10)
        cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0,255,0], 10)
        # pixel 30width
    except Exception as e:
        print(str(e))
        pass
    try:
        for coords in lines:
            coords = coords[0]
            try:
                cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), [255,0,0], 3)
                
                
            except Exception as e:
                print(str(e))
    except Exception as e:
        pass

    try:

        return processed_img,original_image, m1, m2, l1[0],l1[2],l2[0],l2[2]

    except Exception as e:

        return processed_img,original_image, m1, m2, 0,0,400,400
        
def detect(data):
    
    
    bridge = CvBridge()
    image = bridge.imgmsg_to_cv2(data, "bgr8")
    print("3")
    #cv2.imshow("Image",image)
    ret,thresh1 = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
    newimage,original_image, m1, m2, x1,x2,x3,x4 = process_img(thresh1)
    print(x1)
    print(x2)
    print(x3)
    print(x4)
    
    mid = (x1 + x2 + x3 +x4)/4
    print(mid)
   
    print("In Move")
    diff = mid -200

    if mid < 170:
        msg.linear.x = 0.2
        msg.angular.z = -0.2

    elif mid > 230:
        msg.linear.x = 0.2
        msg.angular.z = 0.2

    else:
        msg.linear.x = 0.5
        msg.angular.z = 0.0

    pub.publish(msg)

    cv2.imshow("Image2",original_image)
    k = cv2.waitKey(5) & 0xFF

    r.sleep()

if __name__ == '__main__':

    rospy.init_node('image_gazebo', anonymous=True)
    rospy.Subscriber("/mybot/camera1/image_raw", Image, detect)
    pub = rospy.Publisher("/cmd_vel",Twist,queue_size=1)
    msg = Twist()
    r = rospy.Rate(4)
    rospy.spin()
