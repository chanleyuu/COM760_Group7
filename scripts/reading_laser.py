#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

def clbk_laser(msg):
    regions = [
        min(msg.ranges[0:143]),
        min(msg.ranges[144:287]),
        min(msg.ranges[288:431]),
        min(msg.ranges[432:575]),
        min(msg.ranges[576:713]),
        ]
    close = False
    for region in regions:
        if region <= 10:
            close = True
            
    pub = rospy.Publisher('/week7bot/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)
    vel_msg = Twist()
    i = 10
    if close == True:
        #Turn left
        
	vel_msg.linear.x = -0.1
	vel_msg.angular.z = -0.1
	
	
	while i > 0:
                i = i - 1
		#rospy.loginfo(vel_msg)
		pub.publish(vel_msg)
		rate.sleep()
    else:
        vel_msg.linear.x = 0.3
	vel_msg.angular.z = 0.1
	
	while i > 0:
                i = i - 1
		#rospy.loginfo(vel_msg)
		pub.publish(vel_msg)
		rate.sleep()
    
    rospy.loginfo(regions)
    
def main():
    rospy.init_node('reading_laser')
    sub = rospy.Subscriber("/week7bot/laser/scan", LaserScan, clbk_laser)
    
    rospy.spin()
    
if __name__ == '__main__':
	main()
