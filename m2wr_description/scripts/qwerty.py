#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import time
PI = 3.1415926535897

def rotate():

    speed = 100
    angle = 5000

   
    angular_speed = speed*2*PI/360
    relative_angle = angle*2*PI/360

    vel_msg.linear.x=0
    vel_msg.linear.y=3
    vel_msg.linear.z=10
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0

    
    vel_msg.angular.z = abs(angular_speed)
 
    t0 = rospy.Time.now().to_sec()
    current_angle = 0

    while(current_angle < relative_angle):
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed*(t1-t0)
        print(current_angle)


    #Forcing our robot to stop
    vel_msg.angular.z = 0
    vel_msg.linear.y = 0
    velocity_publisher.publish(vel_msg)
    time.sleep(5)
    

def move(distance):
    #Receiveing the user's input
    speed = 5

    #Checking if the movement is forward or backwards
    #Since we are moving just in x-axis
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    vel_msg.linear.x = abs(speed)


        #Setting the current time for distance calculus
    t0 = rospy.Time.now().to_sec()
    current_distance = 0

        #Loop to move the turtle in an specified distance
    while(current_distance < distance):
            #Publish the velocity
        velocity_publisher.publish(vel_msg)
            #Takes actual time to velocity calculus
        t1=rospy.Time.now().to_sec()
            #Calculates distancePoseStamped
        current_distance= speed*(t1-t0)
        #After the loop, stops the robot
    vel_msg.linear.x = 0
    velocity_publisher.publish(vel_msg)
    time.sleep(5)

def stop():
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)


if __name__ == '__main__':
 
        rospy.init_node('robot_cleaner', anonymous=True)
        velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        vel_msg = Twist()
        move(distance=10)
        print("1")
        rotate()
        print("2")
        move(distance=10)
        print("3")
        rotate()
        print("4")
        move(distance=10)
        print("5")
        rotate()
        print("6")
        move(distance=10)
        stop()
   