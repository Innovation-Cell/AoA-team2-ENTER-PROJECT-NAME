def orient_along(px, py):
    #rospy.init_node("speed_controller")
    sub = rospy.Subscriber("odom", Odometry, newOdom)
    #sub = rospy.Subscriber("/mybot/mobile_base_controller/odom", Odometry, newOdom)
    pub = rospy.Publisher("/mybot/mobile_base_controller/cmd_vel", Twist, queue_size=1)
    speed = Twist()
    r = rospy.Rate(4)
    goal = Point()
    ##r = rospy.Rate(1000)
    goal.x = px
    goal.y = py
    #print(goal.x)
    #print(goal.y)
    while not rospy.is_shutdown():
        inc_x = goal.x - x
        inc_y = goal.y - y
        #print(x,y)
        #print(inc_x,inc_y)
        angle_to_goal = atan2(inc_y, inc_x)
        #angle_to_goal_rad = angle_to_goal * (math.pi/180)
        #print(angle_to_goal)
        #print(theta)
        #print(abs(angle_to_goal - theta))
        if abs(angle_to_goal - theta) > 0.05:
            speed.angular.z =0.9
            #speed.angular.z =  ((90*math.pi/180)- theta)
        else:
        #    speed.linear.x = 0.0
            speed.angular.z = 0.0
            pub.publish(speed)
            break
        pub.publish(speed)
        print("Target={}  Current:{}".format(angle_to_goal,theta))
        r.sleep()
        print("not stopping")