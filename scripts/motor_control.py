#!/usr/bin/python

import rospy
import RPi.GPIO as GPIO
import PiMotor
from geometry_msgs.msg import Twist

#Name of Individual MOTORS
m1 = PiMotor.Motor("MOTOR1",1)
m2 = PiMotor.Motor("MOTOR2",1)
m3 = PiMotor.Motor("MOTOR3",1)
m4 = PiMotor.Motor("MOTOR4",1)

def vel_callback(data):
	if abs(data.linear.x) >= abs(data.angular.z)  or abs(data.linear.y) >= abs(data.angular.z): #If linear movement is greater than angular movement, go forward, backward, or diagonally  .
		#are we moving forward/back or side to side
		if abs(data.linear.x) > abs(data.linear.y):
			vel = abs(data.linear.x) * 10
			if data.linear.x > 0:
				#vel = data.linear.x * 10
				#Go forward
				m1.reverse(vel + (data.angular.z * 10))
				m2.forward(vel + (data.angular.z * 10))
				m3.forward(vel)
				m4.reverse(vel)
			elif data.linear.x < 0:
				#vel = data.linear.x * 10
				#Go backward
				m1.forward(vel)
				m2.reverse(vel)
				m3.reverse(vel + (data.angular.z * 10))
				m4.forward(vel + (data.angular.z * 10))
		elif abs(data.linear.x) < abs(data.linear.y):
			vel = abs(data.linear.y) * 10
			if data.linear.y > 0:
				#Go Left
				m1.forward(vel + (data.angular.z * 10))
				m2.forward(vel + (data.angular.z * 10))
				m3.forward(vel)
				m4.forward(vel)
			elif data.linear.y < 0:
				#vel = data.linear.y * 10
				#Go Right
				m1.reverse(vel)
				m2.reverse(vel)
				m3.reverse(vel + (data.angular.z * 10))
				m4.reverse(vel + (data.angular.z * 10))
		else: #Move diagonally
			vel = abs(data.linear.x) * 10
			if  data.linear.y > 0 and data.linear.x > 0: # Move left and forward
				m2.forward(vel) 
				m3.forward(vel) 
			elif  data.linear.y < 0 and data.linear.x > 0: # Move right and forward
				m1.forward(vel) 
				m4.forward(vel) 
			elif  data.linear.y > 0 and data.linear.x < 0: # Move right and backward
				m2.reverse(vel) 
				m3.reverse(vel)
			elif  data.linear.y < 0 and data.linear.x < 0: # Move right and forward
				m1.reverse(vel) 
				m4.reverse(vel) 
	else:
		if data.angular.z > 0:
			vel = data.angular.z * 10
			#Go left
			m1.forward(vel)
			m2.reverse(vel)
			m3.forward(vel)
			m4.reverse(vel)
		if data.angular.z > 0:
			vel = data.angular.z * 10
			#Go right
			m1.reverse(vel)
			m2.forward(vel)
			m3.reverse(vel)
			m4.forward(vel)

def listener():
	#create a subscriber node
	rospy.init_node('motor_control', anonymous=True)
	
	#Initialize the node to subscribe the "robot/cmd_vel" topic
	rospy.Subscriber("robot/cmd_vel", Twist, vel_callback)
	rospy.spin()

if __name__ == '__main__':
	listener()
	
vel_callback()
