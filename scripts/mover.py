#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import tf2_ros
import tf
import math
from std_srvs.srv import Empty,EmptyRequest
emp = EmptyRequest()
client = rospy.ServiceProxy('/call_next',Empty)
rospy.init_node('mover')
tf_buffer = tf2_ros.Buffer()
tf2_ros.TransformListener(tf_buffer)
r = rospy.Rate(10)

var = Twist()
pub = rospy.Publisher('cmd_vel',Twist,queue_size=1)

#call service here once to start it 
rospy.wait_for_service('/call_next')
client(emp)


while not rospy.is_shutdown():
    try:
        trans = tf_buffer.lookup_transform("base_footprint","flag",rospy.Time())
    except(tf.LookupException,tf.ConnectivityException,tf.ExtrapolationException):
        r.sleep()
        continue
    if math.sqrt(trans.transform.translation.x ** 2 + trans.transform.translation.y ** 2) > 0.05:

        
        if abs(0.4 * math.atan2(trans.transform.translation.y, trans.transform.translation.x)) < 0.25:
            var.linear.x = min(0.4 * math.sqrt(trans.transform.translation.x ** 2 + trans.transform.translation.y ** 2),0.5)
            var.angular.z = min(0.4 * math.atan2(trans.transform.translation.y, trans.transform.translation.x),0.3)
            pub.publish(var)
        else:
            var.angular.z = min(0.4 * math.atan2(trans.transform.translation.y, trans.transform.translation.x),0.5)
            var.linear.x = 0
            pub.publish(var)

    elif abs(0.4 * math.atan2(trans.transform.translation.y, trans.transform.translation.x)) > 0.05:
        var.angular.z = min(0.4 * math.atan2(trans.transform.translation.y, trans.transform.translation.x),0.4)
        var.linear.x = 0
        pub.publish(var)
    else :
        var.linear.x = 0
        var.angular.z = 0
        pub.publish(var)
        rospy.sleep(2)
        #call goal changing service here
        rospy.wait_for_service('/call_next')
        client(emp)

    r.sleep()
    

    