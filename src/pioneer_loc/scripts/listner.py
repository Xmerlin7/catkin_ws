#!/usr/bin/env python3
"""import libraries"""
import rospy
from geometry_msgs.msg import Pose2D
import matplotlib.pyplot as plt
import numpy as np
import time


def get_pos(data):
    """get repot position"""
    rospy.loginfo('I heard x:{} y:{} theta:{}'.format(
        data.x,
        data.y,
        (data.theta * 180 / np.pi)
    ))
    """plot data"""
    plt.plot(data.x, data.y, marker=(3, 0, (data.theta * (180 / np.pi) - 90)))
    plt.axis('equal')
    plt.draw()
    plt.pause(0.01)

def listner():
    """node that listen on topic pioneer_loc"""
    rospy.init_node('pioneer_control', anonymous=True)
    rospy.Subscriber('pioneer_loc', Pose2D, get_pos)

    rospy.spin()

if __name__ == '__main__':
    try:
        listner()
    except Exception:
        pass