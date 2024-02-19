#!/usr/bin/env python3

from coppeliasim_zmqremoteapi_client import RemoteAPIClient

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose2D

client = RemoteAPIClient()
sim = client.require('sim')

print("program started")

rospy.init_node("pioneer_talker", anonymous=True)
pub = rospy.Publisher("/pioneer_loc",Pose2D,queue_size = 10)


sim.startSimulation()
print("simulation started")

rate = rospy.Rate(10)

right_motor = sim.getObject("./rightMotor")
left_motor = sim.getObject("./leftMotor")
pioneer_robot = sim.getObjectHandle("car")


while not rospy.is_shutdown():
    sim.setJointTargetVelocity(right_motor, 2)
    sim.setJointTargetVelocity(left_motor, 4)

    pos = sim.getObjectPosition(pioneer_robot, 0)
    angles = sim.getObjectOrientation(pioneer_robot, 0)
    alpha, beta, gamma = sim.yawPitchRollToAlphaBetaGamma(angles[0], angles[1], angles[2])
    
    msg = Pose2D()
    msg.x = pos[1]
    msg.y = pos[2]
    #rotation around z-axis
    msg.theta = alpha 
    pub.publish(msg)

    rate.sleep()