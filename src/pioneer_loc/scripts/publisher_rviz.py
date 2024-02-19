#!/usr/bin/env python3

from coppeliasim_zmqremoteapi_client import RemoteAPIClient

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose2D, TransformStamped
import tf2_ros
import tf


client = RemoteAPIClient()
sim = client.require('sim')

print("program started")

rospy.init_node("pioneer_talker", anonymous=True)
pub = rospy.Publisher("/pioneer_loc",Pose2D,queue_size = 10)

# Initialize TF broadcaster
tf_broadcaster = tf2_ros.TransformBroadcaster()

sim.startSimulation()
print("simulation started")

rate = rospy.Rate(10)

right_motor = sim.getObject("/base_link/rightMotor")
left_motor = sim.getObject("/base_link/leftMotor")
right_wheel = sim.getObject("/base_link/rightWheel")
left_wheel = sim.getObject("/base_link/leftWheel")
pioneer_robot = sim.getObject("/base_link")
# floor = sim.getObject("/Floor")
laser = sim.getObject("/base_link/fastHokuyo_ROS")


def get_transformer_stamped(object_handle, name, rel_to, rel_name):
    pos = sim.getObjectPosition(object_handle, rel_to)
    angles = sim.getObjectOrientation(object_handle, rel_to)

    # Publish the transformation between world frame and car frame
    transformStamped = TransformStamped()
    transformStamped.header.stamp = rospy.Time.now()
    transformStamped.header.frame_id = rel_name
    transformStamped.child_frame_id = name
    transformStamped.transform.translation.x = pos[0]
    transformStamped.transform.translation.y = pos[1]
    transformStamped.transform.translation.z = pos[2]

    quat = tf.transformations.quaternion_from_euler(angles[0], angles[1], angles[2])
    transformStamped.transform.rotation.x = quat[0]
    transformStamped.transform.rotation.y = quat[1]
    transformStamped.transform.rotation.z = quat[2]
    transformStamped.transform.rotation.w = quat[3]

    tf_broadcaster.sendTransform(transformStamped)


while not rospy.is_shutdown():
    sim.setJointTargetVelocity(right_motor, 2)
    sim.setJointTargetVelocity(left_motor, 4)

    # pos = sim.getObjectPosition(pioneer_robot, floor)
    # angles = sim.getObjectOrientation(pioneer_robot, floor)

    pos = sim.getObjectPosition(pioneer_robot)
    angles = sim.getObjectOrientation(pioneer_robot)

    # values are reversed
   # quat_2 = sim.getObjectQuaternion(pioneer_robot, floor)

    alpha, beta, gamma = sim.yawPitchRollToAlphaBetaGamma(angles[0], angles[1], angles[2])
    
    msg = Pose2D()
    msg.x = pos[1]
    msg.y = pos[2]
    #rotation around z-axis
    msg.theta = alpha
    pub.publish(msg)

    get_transformer_stamped(
        right_wheel, "/base_link/rightWheel", right_motor, "/base_link/rightMotor")
    get_transformer_stamped(
        right_motor, "/base_link/rightMotor", pioneer_robot, "/base_link")
    get_transformer_stamped(
        left_wheel, "/base_link/leftWheel", left_motor, "/base_link/leftMotor")
    get_transformer_stamped(
        left_motor, "/base_link/leftMotor", pioneer_robot, "/base_link")
    get_transformer_stamped(
        laser, "/mrt/laser", pioneer_robot, "/base_link")
    # get_transformer_stamped(
    #      pioneer_robot, "/base_link", floor, "/Floor")
    

    rate.sleep()