#! /usr/bin/env python

import rospy
from session_two.msg import ListInt
from geometry_msgs.msg import TransformStamped
import tf2_ros
from std_srvs.srv import Empty, EmptyResponse
count = 0
f = 0
way_points = []

def input_callback(data):
    global f
    global way_points
    way_points = data.data
    if f == 0:
        f = 1
        service_server = rospy.Service('/call_next',Empty,service_callback) # pylint: disable=unused-variable

def service_callback(data):
    global count 
    global way_points
    #rospy.loginfo(data)
    if len(way_points) >=1:
        if count+1 <= len(way_points):
            flag_broadcaster(way_points[count],way_points[count+1])
            count += 2
        else:
            count = 0
            service_callback(0)
        return EmptyResponse()

def flag_broadcaster(x_g,y_g):
    rospy.loginfo("x: ",x_g," y: ",y_g)
    br = tf2_ros.StaticTransformBroadcaster()
    t = TransformStamped()
    t.header.frame_id = 'odom'
    t.header.stamp = rospy.Time.now()
    t.child_frame_id = 'flag'
    t.transform.translation.x=x_g
    t.transform.translation.y=y_g
    t.transform.rotation.w=1
    br.sendTransform(t)

rospy.Subscriber('/set_waypoint',ListInt,input_callback)
rospy.init_node('flag_bear')
#r = rospy.Rate(5)

#r.sleep()
rospy.spin()