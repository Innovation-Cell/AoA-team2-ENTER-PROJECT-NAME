#!/usr/bin/env python
import math
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3

def move(distance):
    #Receiveing the user's input
    speed = 1
    print("In Move")

    #Checking if the movement is forward or backwards
    #Since we are moving just in x-axis
    command.linear.y = 0
    command.linear.z = 0
    command.angular.x = 0
    command.angular.y = 0
    command.angular.z = 0

    command.linear.x = abs(speed)


        #Setting the current time for distance calculus
    t0 = rospy.Time.now().to_sec()
    current_distance = 0

        #Loop to move the turtle in an specified distance
    while(current_distance < distance):
            #Publish the velocity
        pub.publish(command)
	#print("Done")
            #Takes actual time to velocity calculus
        t1=rospy.Time.now().to_sec()
            #Calculates distancePoseStamped
        current_distance= speed*(t1-t0)
        #After the loop, stops the robot
    
    command.linear.x = 0
    pub.publish(command)
    

def stop():

    command.linear.y = 0
    command.linear.z = 0
    command.angular.x = 0
    command.angular.y = 0
    command.angular.z = 0

    command.linear.x = 0

    pub.publish(command)
           
def get_rotation(msg):

	global roll,pitch,yaw
	orientation_q = msg.pose.pose.orientation
	orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]

	(roll,pitch,yaw) = euler_from_quaternion(orientation_list)
	#print(yaw)


def rotate(target):
 
	# range of target -180 to 180
	while not rospy.is_shutdown():
		
		odom.child_frame_id = "base_link"
		
		target_rad = target*math.pi/180
		diff = abs(target_rad-yaw) 
		odom.twist.twist = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0.9))

		pub.publish(odom)
		if diff <0.05:
			print("Rotation Complete")
			odom.twist.twist = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))
			pub.publish(odom)
			return
		#print("Target={} Current={}".format(target_rad,yaw))

		r.sleep()

if __name__ == '__main__':

	kP = 5

	roll=0.0
	pitch=0.0
	yaw=0.0

	rospy.init_node('rotate_robot')
	sub = rospy.Subscriber('/odom',Odometry,get_rotation)
	pub = rospy.Publisher('/odom', Odometry,queue_size = 1)
	r = rospy.Rate(10)

	odom_broadcaster = tf.TransformBroadcaster()

	#odom_broadcaster.sendTransform((x, y, 0.), odom_quat,current_time, "base_link", "odom")

    # next, we'll publish the odometry message over ROS
	odom = Odometry()
	#odom.header.stamp = current_time
	odom.header.frame_id = "odom"


	print("1")
	rotate(target =0)
	print("2")
	#move(distance=4)
	print("3")
	rotate(target=90)
	print("4")
	#move(distance=1)
	print("5")
	rotate(target=90)
	print("5")
	#move(distance=1)
	print("6")
	rotate(target=-90)
	print("7")
	#move(distance=30)

	

